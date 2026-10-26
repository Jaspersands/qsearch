# Class-Three HSP: Complete Proposed Composition

**Local theorem draft, not an independently reviewed or novelty-validated
result. The complete algorithm below has NOT been executed.**

The purpose of this draft is to make one mathematical claim inspectable.
It does not turn passing finite controls into proof, or count known
subroutines as new contributions.

**Scope reassessment (2026-10-21):** `BOUNDED_CLASS_METABELIAN_HSP.md`
derives a proposed extension to every FIXED nilpotency class with
abelian derived subgroup. It replaces the explicit cubic expression by
a degree-at-most-class section-word potential. Its preferred completion
now repeatedly certifies a strict class decrease and finishes with
abelian HSP; cyclic-quotient HPGP completion remains an alternative.
Class-four controls refute the two class-three shortcuts before checking
their replacements. This is a written extension, not general-class Lean
certification, execution, novelty admission, or an external application.
Its Checked Adaptive Composition section now gives an ideal-model
subgroup acceptance proof, an explicit approximation counterexample,
bounded retry/error accounting and a disjoint depth-first storage bound.
These also apply to this class-three specialization; they are not an
unconditional noisy-source certificate or an implemented dispatcher.

## Candidate Statement

Let `G` be a finite group of nilpotency class at most three, supplied in a
valid refined polycyclic normal-word presentation with polynomial-time
collection. Let a deterministic quantum-query oracle `f` hide an arbitrary
subgroup `H`: it is constant on each `gH` and distinct on different cosets.

**Proposed conclusion:** generators of `H` can be found by a bounded-error
quantum algorithm in polynomial time in the public presentation size,
`log|G|`, oracle-register size, and the supplied collection cost.
There is no bounded-prime restriction in the written argument.

The possible contribution is the unknown-affine-support phase conversion
and its interface to the non-split class-three group. Even the underlying
fresh-register shear is known phase linearization, not a new primitive.
The group reduction, diagonal-equation solvers, abelian HSP and final
optional univariate HPGP learning are also known tools. Novelty and external
computational significance are NOT established by this statement.

## Dependency Boundary

The known reduction is Theorem 2 and Section 3 of
[Ivanyos, Sanselme and Santha, March 2, 2010 author version](https://www.irif.fr/~santha/Papers/iss12.pdf).
It reduces a subgroup/quotient-closed constant-class family to trivial or
order-`p` hidden subgroups in exponent-`p` groups. The small-prime case
uses its cited bounded-exponent algorithm; it must not be passed through
formulas dividing by 2, 3 or 12.

For `p>3`, the public normal-word/Lie conversion is explicitly derived in
`NIL3_NORMAL_WORD_BRIDGE.md`. This begins after the presentation is
available; black-box presentation acquisition is not silently free.
Effective BCH/inverse-BCH conversion is itself prior art:
[Cicalo, de Graaf and Vaughan-Lee, 2012](https://doi.org/10.1016/j.jalgebra.2011.11.031).
The local formulas and their audits are not a new Lazard correspondence.

The general quadratic/cubic diagonal solvers and final HPGP method are
from [Ivanyos and Santha, arXiv:1503.09016v2](https://arxiv.org/pdf/1503.09016).
No general-prime backend or complete recursive solver is implemented in
this repository yet.

## Direct Arbitrary-Subgroup Route At Exponent p

**New written simplification, not an executed dispatcher.** For an
exponent-`p` group with `p>3`, the unknown-support construction does not
need a cyclic promise. The following route handles arbitrary `H` directly.
It does NOT remove the exponent/prime reductions for general finite groups.
It also does not change the novelty or application boundary above.

### Learn The Intersection Before Taking A Quotient

Initially put `N=[L,L]`, and let `K=H intersect exp(N)`. Write `K` also
for its Lie subspace when using additive coordinates. The standard mixed
coset state has entries

```
rho_H(g,g') = |G|^-1 * 1_{g^-1*g' in H}.
```

Measuring the quotient coordinate `q` restricts these edges to elements
of `K`. Their normal differences are `Phi(q)K`. Applying `Phi(-q)` to
the normal register therefore gives, conditional on EVERY observed `q`,

```
rho_K(a,b) = |N|^-1 * 1_{b-a in K}.
```

This proves the source statement for arbitrary `dim(K)`, not just a
line or a classical mixture inferred from one coset. The measured `q`
is uniform. Ordinary abelian Fourier sampling with a fixed batch learns
`K`. On the event of a correct learned intersection:

1. `K` is normal in `H`, since `exp(N)` is normal in `G`.
2. Consequently `H <= M=N_G(K)`.
3. `K` is normal in `M`, so restricting the original oracle to `M`
   and passing through a clean public section defines the HSP for `H/K`
   in `M/K`, without losing ANY part of `H`.

The normalizer is public linear algebra here. On `N`, conjugation is
`1 +/- ad(x)` because `[L,[L,N]]=0`. Thus

```
log(M) = {x in L : [x,K] subset K}.
```

These are homogeneous linear equations in `x`; in particular `N <= log(M)`.
No search over group elements or unknown subgroup membership is needed.
Compute the quotient Lie algebra and a new adapted basis. Its derived
ideal is contained in `N/K`, and
`(H/K) intersect (N/K)=1`, so the new hidden subgroup is transverse to
the new derived ideal as well. If the quotient is abelian, finish with
abelian HSP immediately.

This is a SPECIAL normalizer reduction. For an arbitrary known `K<=H`,
the earlier frozen-normalizer counterexample still applies. The crucial
extra premise is `K=H intersect exp(N)`, hence `K normal in H`. Do not
reuse this step after an arbitrary successful generator discovery.
Do not form `G/K` if `K` is not normal in `G`.

There is a useful verifiable guard: exact Fourier samples give an estimate
`Khat` CONTAINING `K`. Check `f(k_i)=f(1)` on a linear basis of `Khat`.
Since `Khat<=N` and `N` is abelian, all these checks pass if and only if
`Khat=K`. At most `n` original oracle evaluations plus the identity label
are needed. A failed check consumes the batch and must not enter the
normalizer step. The fixed rank bound already bounds its failure rate.
Membership checks alone do NOT certify completeness without the
`K<=Khat` inclusion; approximate-QFT errors remain separately charged.

### A Common Cubic Potential For Any Hidden Rank

Rename the quotient group and its derived Lie ideal `G,L,N`. Now
`H intersect exp(N)=1`. Its image `U` in `V=L/N` can have ANY rank.
Since commutators of `H` lie in both `H` and `exp(N)`, `H` is abelian.
The public group-word Lie operations show that `log(H)` is a linear
subspace: it is the graph of an UNKNOWN linear map `a:U -> N`.
Thus the unique hidden element projecting to `u` has chart coordinates

```
h(u) = (g(u),u),       g(u)=a(u)+[u,a(u)]/2.
```

The subgroup law gives
`g(u+v)=g(u)+Phi(u)g(v)+C(u,v)`. Choose an UNKNOWN proof-only linear
projection `pi:V -> U`. For `u=pi(q)` and `r=q-u`, define

```
Q(q) = Phi(r)g(u)+C(r,u)
     = a(u)+[q,a(u)]-[u,a(u)]/2
       +[q,u]/2+[q,[q,u]]/3-[u,[q,u]]/6.
```

All occurrences of `u` and `a(u)` are linear in `q`; hence `Q` has total
degree at most three. Neither `pi`, `U`, `a` nor coefficients of `Q`
are supplied to the receiver. There is no public splitting assumption.
In particular, the chosen lifts of `U` in `V` need not commute; their
central brackets can be cancelled by the unknown normal components.

For `v in U`, `r` is unchanged when `q` becomes `q+v`. The two products
`(0,r)h(u)h(v)=(0,r)h(u+v)`, evaluated in the public chart, give

```
Q(q+v)-Q(q) = Phi(q)g(v)+C(q,v).
```

This is the same increment relation as in the cyclic construction,
now for every direction in `U`. Changing `pi` changes `Q` only by a
function constant on `U`-cosets, so full `Q` remains unidentifiable and
is not the output of the algorithm.

### Derive The Source From Group Edges

Let `D=|V|`, `B=|N|`, and use the positive-sign normal QFT convention
`|a> -> B^-1/2 sum_lambda chi_lambda(a)|lambda>`. Transversality and
the increment identity imply

```
((q,a)^-1*(q',b) in H)
  iff q'-q in U and b-a=Q(q')-Q(q).
```

For fixed `q,q'` satisfying this relation there are exactly `B`
allowed pairs `(a,b)`. The actual subnormalized Fourier block is

```
sigma_lambda(q,q')
 = (B*|G|)^-1 sum_{a,b} chi_lambda(a-b)
       * 1_{((q,a)^-1*(q',b) in H)}
 = (B*D)^-1 * 1_{q'-q in U}
       * chi_lambda(Q(q)-Q(q')).
```

Thus its trace is exactly `1/B`, independently of `dim(U)` and `lambda`.
After normalization it is `rho(U,lambda.Q)` as required by the erasure
lemma. This includes the zero character; no rare character or rank
postselection is being used. Fresh original oracle preparations provide
independent mixed inputs. This derivation starts from the actual group
source, not an assumed full-domain polynomial-phase oracle.

The Lean theorem `mixed_branch_identity` already quantifies over arbitrary
submodules `U`. The existing symbolic coefficient-rank bounds

```
R_3=n,    R_2=n*(m+1),    R_1=n*binom(m+2,2)
```

and general-prime diagonal solvers are unchanged. They erase the phases
without knowing `rank(U)`. Final Fourier samples are uniform on `U^perp`.
Use a FIXED batch of `t >= m+ceil(log_p(1/delta_U))` samples. If
`d=dim(U^perp)`, the failure probability is at most
`(p^d-1)*p^-t <= p^(m-t)`; it is zero when `d=0`.
The learned nullspace can have any dimension from zero to `m`.
The current receiver's stop-at-nullity-one rule is NOT this algorithm.

### Finish In A Known Class-Two Group

The later Certified Class Descent section of BOUNDED_CLASS_METABELIAN_HSP.md
gives the preferred self-contained completion: after reaching the
class-two preimage below, repeat the same support-learning/class-test
step and reach an abelian ambient. The nil-2 solver and HPGP routes
retained here are valid alternatives, not essential dependencies.

Once `U` is learned, its full public preimage is

```
T = exp(N + lift(U)) = H exp(N).
```

Both `H` and `exp(N)` are abelian, and `[H,exp(N)]` is contained in
`gamma_3(G)`, which is central. Therefore `T` has class at most two.
Restrict the original clean quotient oracle to this public subgroup
and apply the already published nil-2 HSP algorithm, ISS Theorem 1.
Lift its generators and include the learned `K`; this generates the
original `H`.

Exact identification of `U` is sufficient but not necessary. After each
erased Fourier sample, the observed nullspace `Uhat` contains `U`.
Its preimage `That=exp(N+lift(Uhat))` therefore contains `H`.
Test the entirely PUBLIC condition
`[log(That),[log(That),log(That)]]=0` on basis triples. When it holds,
the nil-2 solver is valid already, even if `Uhat` is strictly larger
than `U`. If it does not hold, collect another fresh erased sample,
up to the same fixed cap. Once the rank batch has identified `U`,
the condition must hold by the proof above. This gives a correct
goal-directed stopping rule without knowing hidden rank, support, or
generators. It does not claim fewer copies in the worst-case bound.
The inclusion premise again uses exact Fourier samples; numerical
implementation error is part of the algorithm's failure allowance.

This route uses one intersection, one normalizer quotient, unknown-support
phase erasure, and one known nil-2 completion. It avoids arbitrary-H
cyclic recursion INSIDE the exponent-`p` case. All subgroups, quotient
sections, and the restricted input oracle must still be implemented in
the supplied public presentation with their collection cost charged.
`T` need not be normal in `G`, and restriction does not require normality.

Alternatively, after learning `U`, select each basis line `W<=U` and
measure the quotient register modulo `W`. The existing corrected
`graph_branches` map gives a full univariate quadratic graph with an
unknown normal offset on each branch; learning one generator per line
with the known HPGP learner also suffices. This does not contradict the
wrong-line dephasing counterexample: here `W` is KNOWN to be contained
in `U`. The nil-2 completion above has the simpler published interface;
the line slices connect this derivation to existing local receiver code.

### Error, Implementation, And Falsifier Boundary

Allocate explicit failure budgets to intersection learning, field/solver
setup, quotient-support learning, the final nil-2 solver, and numerical
gate approximation. Their sum must be at most the requested error.
An incorrect intersection estimate can invalidate the normalizer
reduction; no probability argument may condition it away for free.
The old cyclic budget JSON is NOT a recorded execution or exact resource
cap for this alternative controller.

New finite controls in `tests/test_nil3_arbitrary_subgroup_interface.py`
use the genuine class-three Lie algebra
`[X,Y]=Z, [X,Z]=A, [Y,E]=A`. They check a rank-two transverse subgroup
whose quotient lifts do not commute, all actual mixed-source character
blocks, multiple projection gauges, a nonnormal intersection with its
proper normalizer, class-two completion, and known-line graph slices.
They also check the intersection membership guard and a valid class-two
stop BEFORE exact quotient-support recovery.
The group enumeration is a correctness diagnostic, not a scalable
classical baseline or a newly invented oracle application.

Attempted falsifiers include omitting the normal twist, quotienting by
`K` before normalizing it, applying the special normalizer argument to
arbitrary `K`, assuming the quotient lifts commute, retaining the line-only
rank stop, and claiming `HN` is nil-2 without first making `H` transverse.
The last assertion is explicitly false for `H=G` in a class-three group.
The group-relation-to-Fourier-kernel calculation is now Lean-certified
in `formal/Formal/CosetSourceFourier.lean`, CONDITIONAL on the coordinate
action law and the full hidden-subgroup parametrization. It derives the
same-coset relation and evaluates the two Fourier sums; it does not assume
the target phase-kernel formula.

The class-three Lie-algebra mechanism is now separately proved in
`formal/Formal/ClassThreePotential.lean`: the normal-first BCH chart,
the increment for commuting hidden lifts, and the right-action law for
one fixed linear projection/normal section. Its normal space is the
span of actual brackets; abelianness and `[L,[L,N]]=0` are derived from
the class-three hypothesis. No increment identity is assumed there.

The same module represents the potential as a linear map plus diagonal
evaluations of bundled bilinear and trilinear maps. This certifies its
cubic structure without a field-size interpolation assumption. The
right-action theorem explicitly excludes characteristics two and three.
The projected directions themselves need NOT commute.

This is still not one fully instantiated Lean theorem about the original
group oracle. The finite-group/Lazard equivalence, construction of the
coordinate bijection and hidden linear graph, normalizer/completion
reductions, concrete monomial encoding, and computational complexity
remain outside that formal proof. The general-prime backend and complete
arbitrary-H controller remain unexecuted. Independent proof review,
novelty, and a useful external application remain open.

## The Cyclic Promise Handler

It remains to solve one supplied-state problem. Public input is an
adapted class-three Lie algebra

```
L = V direct-sum N,  N=[L,L],  dim(V)=m, dim(N)=n,
```

and independent standard coset states for `|H| in {1,p}`. If `n=0`, use
abelian HSP directly. Otherwise `N` is abelian because `[N,N]` lies in
the fourth lower-central term.

### 1. Decide The Normal Case

In coordinates `exp(n)exp(q)`, measure `q` and apply `Phi(-q)` to the
normal register, where `Phi(q)n=n+[q,n]`.

If `H<=N`, the remaining register is a uniform random coset of `H` in
the abelian group `N`. If a cyclic `H` is transverse to `N`, its quotient
parameter is injective; fixing `q` leaves one normal basis element.
Averaging fresh original cosets makes that element uniform. Trivial `H`
gives the same maximally mixed normal source.

Thus abelian Fourier samples learn `H intersect N`. A nonzero result
is the whole `H` under the cardinality promise. A nullspace larger than
one in this step is an incomplete or invalid-promise run, not a valid
larger hidden subgroup.

### 2. Obtain A Common-Potential Quotient Source

For the remaining cases, `H` is trivial or transverse cyclic.
The chart multiplication is

```
(n,q)(n',r) = (n+Phi(q)n'+C(q,r), q+r),
C(q,r) = [q,r]/2 + [q,[q,r]]/3 + [r,[q,r]]/6.
```

For nontrivial `H`, write its powers as `(g(t),t*v)`. With an UNKNOWN
proof-only functional `ell(v)=1`, let `tau=ell(q)`, `r=q-tau*v`, and

```
Q(q) = Phi(r)g(tau)+C(r,tau*v).
```

The group cocycle identities give
`Q(q+t*v)-Q(q)=Phi(q)g(t)+C(q,t*v)`. This is one fixed cubic vector
polynomial, not a fresh unknown polynomial for every coset.

Here is a direct check independent of the cocycle shortcut. Write the
Lie logarithm of the chosen generator as `v+a`, with `a in N`; `a` is
NOT its normal coordinate in the `exp(n)exp(q)` chart. Then
`g(t)=t*a+t^2*[v,a]/2`. Expanding the displayed potential gives

```
Q(q) = tau*a - tau^2*[v,a]/2 + tau*[q,a]
         + tau*[q,v]/2 + tau*[q,[q,v]]/3
         - tau^2*[v,[q,v]]/6,       tau=ell(q).
```

Indeed `[L,[L,N]]=0` and `[N,N]=0`. Substituting `q+t*v` changes
`tau` to `tau+t`, leaves `[q,v]` fixed, and changes
`[q,[q,v]]` to `[q,[q,v]]+t*[v,[q,v]]`. Subtracting yields

```
Q(q+t*v)-Q(q)
  = t*a + t^2*[v,a]/2 + t*[q,a]
      + t*[q,v]/2 + t*[q,[q,v]]/3 + t^2*[v,[q,v]]/6
  = Phi(q)g(t)+C(q,t*v).
```

This is a universal class-three identity for `p>3`, not an inference
from a prime sweep. The tests separately check its rational scalar
coefficients and its evaluation in the free three-generator Lie algebra.
Any functional with `ell(v)=1` works. Two resulting potentials differ by
a function constant on each coset of `span(v)`; this is a gauge freedom
of the source, not algorithmic knowledge of `ell`.

Partial Fourier measurement of `N` produces a uniform PUBLIC label
`lambda` and the mixed state `rho(span(v),lambda.Q)`, where

```
rho(U,P)_(x,x') = |V|^-1 * 1[x-x' in U] * omega^(P(x)-P(x')).
```

For trivial `H`, the conditional quotient source is `I/|V|`, equal to
`rho({0},P)` for any `P`. Hence the same erasure schedule is valid
without knowing which case holds.

The derivation from actual mixed group edges, rather than an assumed
phase oracle, is in `AFFINE_PHASE_MIXED_CHANNEL_AUDIT.md`.

### 3. Erase The Phase Without Losing The Unknown Support

The public operation below is adapted from Section 2.1, pages 4-5, of
[Decker, Hoyer, Ivanyos and Santha, arXiv:1305.1543v2](https://arxiv.org/pdf/1305.1543v2).
Their phase-linearization construction already adds a uniform register,
shears the old coordinates and measures them. The issue to prove here
is its mixed unknown-support invariant, not inventing that operation.

Given independent `rho(U,P_i)`, append a fresh uniform ambient `x`,
subtract public `c_i*x` from the old coordinate registers, and measure
them as `y_i`. At least one `c_i` must be nonzero. The complete instrument
has the exact branch identity

```
K_y (tensor_i rho(U,P_i)) K_y^dagger
  = |V|^-k * rho(U, sum_i P_i(y_i+c_i*x)).
```

All outcomes are retained and uniform for these mixed inputs. No
unknown origin, support direction or phase coefficient is evaluated.
Classical adaptivity is conditioned on previous transcripts; disjoint
batches remain independent under that conditioning.

The algebraic instrument identity is now kernel-checked in
`formal/Formal/AffineSupportErasure.lean`. Its proof begins with the two
Kraus sums and arbitrary complex phase functions, not the desired output
formula as a hypothesis. It also proves uniform branch trace for unit
phases, Kraus completeness, and the all-zero-scale failure to preserve
proper support. The headline proofs use only the project's three standard
Lean axioms. The separate `CosetSourceFourier` module certifies the source
conversion conditional on its coordinate action law. `ClassThreePotential`
now derives the corresponding Lie-algebra law and cubic decomposition.
Transporting these statements through the concrete group/presentation
equivalence is not yet composed in Lean. Source independence, positivity
representation, polynomial cancellation, the recursive algorithm,
complexity and novelty are not formalized; see `formal/README.md`.

Store public formal coefficient maps into the unknown coefficients of
`Q`. At degree `j`, solve the public diagonal equations cancelling all
degree-`j` coefficients, then update the maps by translation.
The equation-rank bounds are

```
R3=n,  R2=n*(m+1),  R1=n*binom(m+2,2).
```

They follow by factoring coefficients through the translation moments
`sum_i lambda_ia*b_i^j*a_i^gamma`, `|gamma|<=3-j`.
They hold for correlated later coefficient maps and adaptive translations;
they do not assume later packets are independent random columns.

Using the published general solvers, one phase-free quotient output
costs at most

```
S = (9n+1)*(3n+1)*(n+1)
      * (n*(m+1)+1)^2 * (n*binom(m+2,2)+1).
```

This is `O(n^6*m^4)` original coset copies. Zero-weight inputs are
discarded and charged. Intermediate symbolic maps and classical
arithmetic are polynomial-size; this copy exponent is not a gate exponent.

### Solver Interface And Bit Complexity

The cited SDE Propositions 9 and 10 take arbitrary field coefficient
vectors. They do not assume random, independent, nonzero or full-rank
columns. Their output is a NONZERO vector of variable values satisfying
all diagonal equations. Thus they apply after conditioning on any public
history. Their random setup concerns field nonresidues, not a favorable
distribution of our source labels. No ERH assumption is used here.

Here is an exact version of the rank argument. Every packet is, modulo
a constant, a sum over its original leaves
`sum_l lambda_l.Q(a_l+b_l*x)`, with public scalar b_l and vector a_l.
Flattening a later translation `x -> y+c*x` updates
`a_l -> a_l+b_l*y` and `b_l -> b_l*c`. This remains true for adaptive
choices and zero scales. It is a proof representation; an implementation
need not store an expanding expression tree.

Let the independent formal parameters be `beta_(a,alpha)`, the
nonconstant monomial coefficients of Q_a, `|alpha|<=3`. At degree j,
define the moment column of packet i by

```
M_i(a,gamma) = sum_(l in i) lambda_(l,a) b_l^j a_l^gamma,
|gamma| <= 3-j.
```

The coefficient of beta_(a,alpha) in its x^delta term, `|delta|=j`,
is `binom(alpha,delta)*M_i(a,alpha-delta)` if alpha>=delta, and zero
otherwise. Consequently the entire leading-coefficient matrix is
`A_j=T_j M`, for ONE fixed public matrix T_j.

In fact T_j is injective for p>3. For any gamma choose
`delta=(j,0,...,0)` and `alpha=gamma+delta`. That output coordinate
reads only M(a,gamma), with nonzero multiplier `binom(gamma_1+j,j)`.
The upper argument is at most three, so it cannot vanish modulo p.
Thus `rank(A_j)=rank(M) <= n*binom(m+3-j,3-j)` without a randomness
assumption. The exact controls verify this embedding and its composition
through two adaptive translation levels.

Compress EQUATION ROWS, preserving the input columns: if B has the same
row span as A_j then `A_j c^j=0 iff B c^j=0`. Arbitrary column changes
are not equivalent substitutions through a coordinatewise power map.
For example `x^2+2y^2=0` over F_5 and `x^3+2y^3=0` over F_7 have no
nonzero solution, whereas replacing the second coefficient by one does.
The current `independent_columns` routine actually performs the correct
row operation despite its name.

No field-sized search or general discrete logarithm is needed for
square/cube extraction. To see the bit cost, let `ell in {2,3}` and
`p-1=ell^s*t`, with gcd(ell,t)=1. A verified ell-nonresidue zeta gives
`z=zeta^t` of order ell^s. Split an ell-power u using

```
h = u^(t*(t^-1 mod ell^s)),  k=u/h.
```

Here h is in the ell-primary subgroup and k has order dividing t.
Recover `a=log_z(h)` one base-ell digit at a time: after j digits,
raise `h*z^(-a_partial)` to `ell^(s-1-j)` and compare with the ell
powers of `z^(ell^(s-1))`. There are at most three choices per digit,
not ell^s choices. Since u is an ell-power, ell divides a, and a root is
`z^(a/ell)*k^(ell^-1 mod t)` (omit the second factor if t=1).
If s=0, ordinary inverse-exponent powering suffices.
This uses O(log p) modular exponentiations, no factorization of t and
no general discrete-log oracle. It is a known smooth-order technique,
not a new number-theoretic contribution.

Uniform sampling from F_p^* finds a quadratic nonresidue with probability
1/2, and a cubic nonresidue, when needed, with probability 2/3.
At most two reusable field setups, each capped at
`ceil(log2(2/eta))` trials, fail with total probability at most eta.
Returned roots and complete cancellation relations are verified exactly.
The published deterministic conic subroutine or a separately capped,
charged replacement is required; an unbounded search loop is not a
bounded-running-time implementation.

For storage, put `J=binom(m+3,3)-1`. A dense packet has at most n*J^2
field entries, each O(log p) bits. Each original monomial contributes
to at most eight submonomials on translation, since its degree is at
most three. Translation updates, row reduction and fixed-degree SDE
therefore have polynomial classical bit cost with canonical reduction
modulo p. No operation enumerates the p^m ambient points. Across the
three merge levels there are at most 3*S source-register incidences;
each shear uses m public modular multiply-adds per incidence.
The quantum arithmetic and approximate transforms are polynomial in
m,n,log p and log(1/epsilon), separately from classical controller work.

This is a complexity argument for the proposed algorithm, not a
performance claim about the diagnostic backend. That backend still uses
machine-word `nmod_mat`, restricted-prime roots and an uncapped conic
loop. In particular, its row compression rejects p=2^127-1 with an
OverflowError. Arbitrary-precision field matrices and capped general-
prime solvers remain implementation tasks; passing the new test-only
root controls does not complete them.

### 4. Learn The Entire Annihilator

Fourier measurement of the phase-free output is uniform on `U^perp`.
Collect a FIXED sufficient number of samples, allowing rank `m`.
Rank `m` means `U={0}`, hence trivial `H`. Rank `m-1` gives the
nonzero quotient line. Lower rank is failure/incomplete learning.

The existing finite `learn_quotient_line` function assumes nontrivial
`H` and stops at rank `m-1`. It must not be used as this dispatcher.
For trivial `H`, that stopping rule necessarily produces a false line
once enough samples arrive. The exact budget tests exhibit the issue.

### 5. Complete The Nonzero-Line Case

Choose known `v` on the learned line and known `ell(v)=1`. On fresh
original cosets, measure `r=q-ell(q)*v`, retain `t=ell(q)`, and map

```
n -> Phi(-r)(n-C(r,t*v)).
```

This produces the full univariate graph-state ensemble for
`g_v(t)=t*w+(t^2-t)*D_v*w/2`, with public `D_v=[v,.]` and unknown
normal coordinate `w`. The cocycle subtraction is essential.

Apply known quadratic HPGP phase learning. Maintain `w=w0+B*eta`,
remove the known offset phase, and use Fourier labels to obtain public
linear and quadratic coefficient rows. A raw packet has zero formal
coefficient map with probability at most `p^-k` when `k` parameters
remain, because the sum of its two rows is `lambda*B`.

A nonconstant linear packet immediately gives one equation. Otherwise,
combine `(k+1)^2` quadratic packets. After quadratic cancellation the
new linear coefficient is

```
z = sum_i c_i*Y1_i + 2*sum_i c_i*y_i*Y2_i.
```

Some active `c_i*Y2_i` is nonzero. The outcomes `y_i` are independent
uniform field elements, so `Pr(z=0)<=1/p`. A nonzero `z` yields an exact
linear equation by inverse QFT and removes one unknown parameter.

These are the only rejection steps in the final learner. They are
publicly recognizable and all original copies are counted.

## Finite Confidence And Copy Bounds

For a target error `epsilon<=1/2`, put `eta=epsilon/8`.
The exact helper `theorems/nil3_complete_budget.py` computes:

```
t_N = n + ceil(log_p(1/eta)) + 1,
t_V = m + ceil(log_p(1/eta)) + 1,
C = sum_(k=1)^n (k+1)^2,
R = ceil(log_p(n/eta)),
A = ceil(log_p(R*C/eta)).
```

Use `t_N` normal samples and `t_V` phase-free quotient samples.
At each HPGP dimension allow at most `R` equation attempts and at most
`A` raw labels for each required nonconstant packet. Stop with failure,
not an invented answer, if a cap is exhausted.

The total original-copy cap is

```
t_N + t_V*S + R*A*C.
```

Rank failure for `t` samples from a rank-`r` uniform vector space is
exactly `1-product_(i=0)^(r-1)(1-p^(i-t))`, and is bounded by
`p^(r-t)/(p-1)`. Both rank stages therefore fail with probability
at most `eta`. Nonconstant-packet collection fails with probability
at most `R*C*p^-A<=eta`. All equation attempts at some dimension
fail with probability at most `n*p^-R<=eta`.

Reserve another `eta` each for classical SDE setup, bounded random-bit
sampling, and the entire approximate quantum instrument. The total
failure probability is at most `7*eta<epsilon`.

The general solvers require only polynomial classical work. Their
nonresidue choices have constant success probability and can be capped
with logarithmic repetition. Returned diagonal relations are checked
before physical use. Approximate uniform preparation, QFT and reversible
arithmetic errors are allocated across the polynomial number of actual
operations, so their complete-instrument error sums to `eta`.
No rare-branch normalization factor occurs.

This is a uniform mathematical schedule, not the simulator's hardcoded
32 attempts. The artifact computes its exact numerical envelope; it
does not represent actual executed quantum-copy consumption.

## Why The Published Recursion Calls A Legal Solver

### Fix The Original Ambient Group

The reduction remains the published ISS Theorem 2, not a new group
algorithm. Its implementation must retain the original Sylow ambient
group `G` throughout. Write `K` for the currently known subgroup of H.
Each round constructs `N_G(K)/K` AFRESH inside this original G.
Do not recursively restrict all future rounds to the previous normalizer.

The distinction is substantive. In the free class-three exponent-p
group on X,Y (`p>3`), write `Z=[X,Y]`, `A=[X,Z]`, `B=[Y,Z]`.
For `K=<exp X>`, the normalizer tower, in Lie spans, is

```
<X>  ->  <X,A,B>  ->  <X,Z,A,B>  ->  <X,Y,Z,A,B>.
```

The first normalizer has order p^3, while G has order p^5. If H=G,
even an ideal solver confined to that first normalizer misses part
of H. The valid refined chain
`<X> < <X,A> < <X,A,B> < <X,Z,A,B> < G` shows that this initial K
can actually be encountered, not merely chosen after seeing H.
The tower follows directly by conjugating its displayed generators.
Exact p=5 BCH controls verify every normalizer.

Work conditionally on all preceding subroutine answers being correct.
In an ascending refined chain, if the previous intersection with `H`
was trivial and the next factor has order `p`, the next intersection
has order at most `p`. Hence the cyclic handler's promise holds.

More precisely the chain lives in `Q=N_G(K)/K`; its hidden subgroup
is `J=(N_G(K) intersect H)/K`. After finding a nontrivial element of J,
lift it into G, enlarge K, and restart from the original G. If an entire
chain has trivial intersection with J, then `N_H(K)=K`. The normalizer
condition for finite p-groups forces K=H. K need not be normal in G or H.

### Clean Public Quotient Oracle

Choose an efficiently computable public section
`s:Q -> N_G(K)`, so `s(q)K=q`, and define `f_K(q)=f(s(q))`.
The section need not be a homomorphism or a group-theoretic splitting.
For any two representatives of q their ratio lies in K<=H, giving
the same oracle value. Moreover,

```
f_K(q)=f_K(q')  iff  q'^{-1}q in (N_G(K) intersect H)/K.
```

Implement the oracle coherently as

```
|q>|0>|z> -> |q>|s(q)>|z>
           -> |q>|s(q)>|z XOR f(s(q))>
           -> |q>|0>|z XOR f(s(q))>.
```

The last step reverses the PUBLIC lift computation; it does not require
inverting f, solving a hidden subgroup, or receiving hidden advice.
Leaving the lift workspace populated and then discarding it would
dephase distinct q, even when they have equal hiding labels.
The new test explicitly contrasts these two reduced density matrices.
Public embeddings handle restrictions in the same way.

Keep generators of each current subgroup as original normal words.
A quotient normal word lifts by multiplying these public generators
with binary powering and original collection. This avoids exponential
duplication of nested oracle wrappers; there is one original f query
per clean local evaluation plus polynomial public arithmetic.

### Exponent Reduction Before Lie Coordinates

Use the published classical preprocessing, but implement its
abelianization restriction intrinsically:

```
A = L/[L,L],
L_new = preimage in L of ker(p:A -> A).
```

For a local hidden subgroup of order at most p, this restriction retains
every hidden element. If A has exponent larger than p, L_new is proper.
Compute the kernel in invariant-factor coordinates, then lift its
generators and include [L,L]. Repeat until A has exponent at most p.
There are at most `log_p|L|` proper restrictions, none requiring f queries.

Do NOT replace this kernel by high powers of an arbitrary minimal
generating set. In `C_(p^2) x C_p`, the irredundant generators
`x=(1,0), y=(1,1)` both have order p^2, yet
`<x^p,y^p>=<(p,0)>` misses the order-p subgroup `<(0,1)>`.
The correct kernel is `<(p,0),(0,1)>`. This is a counterexample to that
implementation shortcut, not to ISS's reducibility conclusion.
In particular, the generator-power recipe in the first paragraph of
ISS Lemma 3 needs an invariant-factor basis in the abelianization;
irredundancy alone is insufficient. The intrinsic kernel computation
above supplies the required restriction without that extra assumption.

Once the abelianization exponent is at most p, the lower central
factors have exponent at most p, so the local group exponent is at
most p^3. For p<=3 invoke the known bounded-exponent route at THIS
point, not on an arbitrary initial small-prime group. For p>3 use
the published computation of `Omega_1(L)={x:x^p=1}` and restrict to it
before applying the field-valued Lie formulas. In this regime it is
a subgroup containing the local hidden subgroup.

The small-characteristic guard is necessary: order-p elements of
`UT_(p+1)(F_p)` for p=2 or 3 are not closed under multiplication.
The tests give two order-p elements whose product has order p^2.
Thus a generic order-p filter is not a substitute for the small-prime
branch. Presentation and subgroup computations use public group data,
not a list of the unknown hidden elements.

### Calls And Scope

Each successful iteration grows the known subgroup by a factor at
least `p`. For a p-group of order at most `p^d`, at most `d+1` chain
passes of at most `d` calls are needed, including the final unsuccessful
pass. Summed over Sylow factors, `b*(b+1)` is a conservative call cap
when `b>=log2|G|`. Give each handler error at most
`epsilon/[b*(b+1)]`. A first-error union bound applies despite adaptive
subproblems. Small-prime known subroutines receive the same error budget.

Subgroups and quotients remain class at most three, so no new group
family is introduced by this recursion. The exponent-`p` preprocessing
must happen BEFORE invoking the Lie formulas.

`tests/test_nil3_recursive_oracle_interface.py` checks these finite
interfaces and failure modes. It does NOT execute the ISS reduction,
the full cyclic dispatcher, or the general-prime diagonal backend.
The algorithm still requires fresh original oracle queries; these
recursive restrictions are not supplied for free by a bag of coset states.

## Physical Versus Diagnostic Operations

The proposed algorithm uses quantum queries, public reversible
coordinate changes, QFTs, shears, ordinary measurements and classical
linear/diagonal solving. It does not:

- inspect a sparse amplitude dictionary to decide whether a state has
  `p` support points or constant phase;
- read the secret potential or generator to verify a candidate;
- simulate quantum amplitudes in polynomial classical time;
- obtain a clean coherent encoding inverse by assertion;
- run the recursive oracle reduction from supplied states alone.

Amplitude-table assertions in existing tests verify ideal promised
branches. They are not physical membership or promise tests. On an
earlier statistical failure branch, a real bounded-error implementation
may fail or give an incorrect answer; that probability is already
charged. It cannot use an impossible amplitude inspection to repair it.

## Attempts To Refute The Composition

Mixed rather than pure sources, hidden coset origins, discarded
transcripts, non-split cocycles, shared parameters, zero scales,
correlated copies, wrong graph relabeling, unknown coordinates and the
trivial-subgroup stopping rule have all been explicitly examined.
The first eight have exact derivations and independent finite controls;
the complete dispatch and recursive composition remain written only.

The current derivation has not exposed a contradiction in the scoped
oracle theorem. That is not independent verification. A reviewer should
prioritize the common-potential identity, adaptive public coefficient
rank bounds, and the exact restricted/quotient oracle interfaces.
Finding an error in any of those invalidates the theorem, regardless
of numerical test success.

## Novelty And Significance

### Prior-Art Coverage Audit, 2026-10-21

This is a targeted comparison, not a certificate that no prior work
subsumes the draft.

| Prior result | What is already covered | Remaining interface to check |
| --- | --- | --- |
| [DHIS, 1305.1543v2, Theorem 1 and Section 2](https://arxiv.org/pdf/1305.1543v2) | Full univariate polynomial graph states, arbitrary unknown offsets, and phase linearization by the same shear. | Inputs here have an unknown proper affine support, not the full known field domain. |
| [DISW, 1107.2189v2, Theorem 5 and Lemma 6](https://arxiv.org/pdf/1107.2189v2) | Constant-degree multivariate HPGP, using restrictions of an oracle with levels `y-Q(x)`. | No such scalar-output graph oracle or legal known-line restriction has been constructed from the unknown-line coset source. |
| [Ivanyos-Santha, 1503.09016v2, Corollary 6 and Proposition 7/Corollary 8](https://arxiv.org/pdf/1503.09016v2) | Growing vector-output univariate HPGP, diagonal solvers, and bounded-class split groups with cyclic quotient. | The draft permits a higher-dimensional quotient and a non-split extension. Final HPGP completion is already covered and is not new. |
| [FIMSS, Theorem 4.16](https://old.sztaki.hu/~ivanyos/pp/fimss-authorcopy.pdf) | HSP when the commutator subgroup is smoothly solvable. | An abelian commutator subgroup is not automatically smoothly solvable when its prime exponent grows. |
| [Imran-Ivanyos, Theorem 1](https://link.springer.com/article/10.1007/s11128-023-04228-2) | Bounded class with bounded prime factors; an exact state-creation/inverse interface. | Unbounded primes are outside that theorem. Our bounded-error mixed-copy handler is not an implementation of their stronger unitary interface. |
| [Morales, 2608.05321](https://arxiv.org/pdf/2608.05321) | Structured scalar-action semidirect products and quasi-Hamiltonian groups. | In an exponent-p group these conditions force the respective elementary-abelian scalar-action core or quasi-Hamiltonian core to be abelian; they do not cover the nonabelian core here. |
| [Holt-Subramanian, 2609.38085v2, Theorems 7.1 and 7.13](https://arxiv.org/pdf/2609.38085v2) | Normal-core StateHSP and full symmetry learning for poly-near-Hamiltonian groups, subject to their implementation promises. | A nonnormal cyclic subgroup can have trivial normal core. General class-three groups do not satisfy the near-Hamiltonian condition. |

For FIMSS the smoothness condition requires constant-exponent factors
apart from a factor of size polynomial in `log|G|`. For the free
two-generator class-three exponent-`p` group, `G'=F_p^3`. With `p`
unbounded, its nontrivial subgroups cannot have bounded exponent and
`p^3` is not polynomial in `log|G|=5*log(p)`. This is a scope
counterexample, not a lower bound against all solvable-group algorithms.

For the last row, the Baer norm is the intersection of all subgroup
normalizers. In an exponent-`p` class-three group with `p>3`, a Baer
element `exp(X)` must preserve every cyclic subgroup, hence every line
`span(Y)` of the Lie algebra. The operator `exp(ad_X)` is unipotent;
on each preserved line its eigenvalue must therefore be one. It is
the identity, and `log(exp(ad_X))=ad_X=0`. Consequently
`Baer(G)=Z(G)`. The same free group has center dimension two, so
`[G:Baer(G)]=p^3`, not polynomial in `log|G|`. The finite test checks
this example by actual conjugation, not by classifying a theorem from
its title. It does not claim any failure of the published algorithm
within its promised domain.

### Why Full-Polynomial Learning Is Not A Free Subroutine

2026-10-22 follow-up: HPGP_COSET_INTERFACE_AUDIT.md supplies a different,
more general obstruction to a FIXED public fibre-coordinate shortcut.
Its good transverse subgroup parameters lie in an abelian coset, with
tight p^(-m) coverage for an explicit class-three product family. A separate
stability bound handles approximate states within that fixed-chart model.
Neither excludes arbitrary adaptive, collective or oracle-based reductions
to HPGP. The earlier source-identifiability argument below
remains separate and must not be inflated into such a general exclusion.

If `R(x)` is constant on each `U`-coset, then exactly

```
rho(U,P+R) = rho(U,P).
```

Only pairs `x-x' in U` have nonzero density entries, so the added phase
difference vanishes. For example, over `F_5^2` take `U=span((1,0))`,
`P(x,y)=x^3+x*y^2`, and `R(x,y)=y^3`. The two mixed sources are
identical, while the full-domain phase states for `P` and `P+R` differ.
No channel on any number of these identical mixed inputs can faithfully
recover the original full polynomial in both cases. This remains true
with public labels multiplying the phases.

This rules out the naive claim that the mixed source itself supplies
the usual full-polynomial learner. It does NOT rule out learning an
appropriate gauge representative, recovering `U`, using the original
hiding oracle in a different way, or a more sophisticated reduction to
published HPGP machinery. In particular, learning a known line in
`U` would permit a legal restriction, but doing so first is precisely
the unresolved task that the erasure step is meant to solve.

There is also a direct obstruction to replacing oracle restriction with
ordinary measurement. Measuring the affine-coset label modulo a known
subspace `W`, then forgetting that label, multiplies matrix entries by
`1[x-x' in W]`. Consequently this operation takes
`rho(U,P)` to `rho(U intersect W,P)`. For distinct lines `U,W`, the
result is `I/|V|`; even retaining the label leaves only a diagonal
uniform state on its `W`-coset. The labels are uniform and carry no
information about `U`. A random known line agrees with a fixed hidden
line with probability `(p-1)/(p^m-1)`, exponentially small when the
quotient has dimension at least two and `p` grows. This falsifies this
particular measurement-based substitution, not every possible oracle
reduction or collective measurement.

### Falsifiers And Decision

Reject novelty if an existing theorem accepts the same source and gives
the same uniform complexity, or if an efficient public reduction makes
this a direct corollary. Merely recognizing a low-degree polynomial is
not such a reduction. Reject correctness if the all-outcome invariant,
adaptive coefficient ranks, or recursive input promises fail on an
allowed instance. Do not repair an invalid reduction with unknown
support coordinates or postselection of exponentially rare events.

The audit has corrected attribution and narrowed the review target.
It has NOT established novelty, independent correctness, or an external
application. The specific proposal requiring review is:
**known phase linearization preserves unknown parallel affine support,
and the common cubic potential converts general class-three cyclic
coset states into that source with polynomial public coefficient rank.**

[Imran and Ivanyos](https://arxiv.org/abs/2304.08376) already treat bounded
class with bounded prime factors. Small fixed-prime examples are not
novelty evidence. The claimed distinction needing expert verification
is unbounded prime size with a general non-split class-three quotient,
not the known cyclic-quotient HPGP result.

The new classical attack in `NIL3_POLYNOMIAL_HIDING_ATTACK.md` already
solves original polynomial-valued hiding functions of degree `e` when
`p>2(e+1)`. The opaque-label query problem survives that attack, but no
useful external lattice, code, graph or cryptographic reduction has
been established. This theorem, even if correct and new, would not by
itself establish a Shor-level application.

The follow-up CLASS_THREE_APPLICATION_AUDIT.md rules out the natural
graph/code stabilizer applications inside a supplied solvable permutation
group: published classical algorithms already solve them, including
codes with large hull. A hidden nilpotent stabilizer does not supply a
nilpotent ambient group. Also, the usual swap wreath product is not
nilpotent when the base contains an odd-prime-order element.
These reject particular applications/reductions, not this oracle theorem.

Next: independent full-proof/prior-art review. Any proposed external
reduction must first survive the application audit's input-model and
classical-baseline filter. No larger prime sweep or cosmetic integration
substitutes for those tasks.
