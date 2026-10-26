# Bounded-Class Metabelian HSP: Scope Extension Audit

2026-10-21. **Local proposed composition, not an independently reviewed
theorem, executed general algorithm, or novelty claim.**

## Decision

Class three is not the apparent boundary of the existing unknown-support
instrument. The constructive argument below extends the written proposal
to **metabelian groups of any fixed nilpotency class**. The derived
subgroup must be abelian; the class must remain fixed. Neither restriction
can be dropped by this scalar-only argument. A separate matrix-source
extension in QUADRATIC_NONCENTRAL_HSP_SCOPE.md covers the more general
promise [gamma_3(L),L']=0 with possibly nonabelian L'. It still
requires fixed class, higher-degree scalar erasure and the unreviewed
complete receiver dependencies; it does not cover arbitrary nilpotent groups.

Separate boundary work: `UT5_MATRIX_PHASE_ALIGNMENT.md` now proposes a
matrix-source replacement for a restricted transverse-H family in
UT_5(F_p)^r. It does not alter this document's metabelian assumptions or
justify arbitrary nonabelian derived subgroups/normalizer quotients.

The important change is mathematical, not another parameter campaign:
replace the explicit cubic cocycle by a universal section-word potential.
Its degree is bounded by the nilpotency class. Replace class-two
completion, which becomes false, by certified strict class descent until
the ambient group is abelian. The known cyclic-quotient solver on
recovered basis lines remains an alternative, not a required dependency.

This is still an abstract ordinary-oracle HSP proposal. No useful
non-oracle application, classical hardness claim for a concrete encoding,
or Shor-level significance has been established.

## Input And Proposed Conclusion

Fix an integer `c`. Start with an exponent-`p` group of class at most `c`,
where `p>c`, with abelian derived subgroup. For the core derivation assume
a public Lazard Lie algebra `L` over `F_p`, structure constants, and clean
polynomial-cost encoding/decoding between the group and its Lie
coordinates. These operations cannot consult the hidden subgroup.

The input oracle is deterministic, quantum-queryable, and constant and
distinct on the left cosets `gH` of an arbitrary subgroup `H`. It is not
a supplied phase oracle, polynomial-valued oracle, or coset-state
postselection service. The proposed output is generators of `H`.

The proposed cost is polynomial in the public input size, `log p`, and
oracle cost **for each fixed c**. The polynomial's degree and constants
may depend severely on `c`. This is not a uniform polynomial bound for
growing class.

To extend the statement to finite metabelian groups with a supplied
refined polycyclic presentation and collector, use the subgroup/quotient-
closed family reduction in ISS Theorem 2. Handle small primes through
its bounded-exponent branch, before using Lazard coordinates. The
public presentation-to-Lie construction and fixed-class cost are spelled
out below. This is a written interface proof using known Lazard theory,
not an executed general-class compiler; the production implementation
remains class-three only.

## Public Coordinate Cost Audit

2026-10-22 update: UNIVERSAL_LAZARD_WORD_COMPILER.md implements the
universal WORD operations below by exact filtration correction, with
coefficientwise certificates and opaque matrix tests. It does not implement
the rest of the coordinate-acquisition or quantum receiver pipeline; older
pass-specific implementation limits below should be read with this distinction.

### What Is Already Known

The public conversion must not be counted as a new quantum contribution.
In this pass the actual GAP LieRing source and manual were inspected,
not just the 2012 paper's abstract. At commit
`be141828a1997e796c484d34d965c461203e98d1`:

- [lazard.gi](https://github.com/gap-packages/liering/blob/be141828a1997e796c484d34d965c461203e98d1/gap/lazard.gi)
  implements group-word inverse BCH, polycyclic exponent peeling,
  structure constants, and explicit forward/inverse maps in its
  exponent-p branch.
- [The manual](https://github.com/gap-packages/liering/blob/be141828a1997e796c484d34d965c461203e98d1/doc/manual.xml)
  documents that the stored BCH/inverse tables stop at weight 14.
  The inspected package is NOT evidence of execution at arbitrary class.

No GAP installation, copied package code, or general running-time claim
for GAP is introduced here. The polynomial-cost inference below is a
separate argument for a SUPPLIED collector and fixed class. The full
2012 paper was still not available; its unread complexity details are
not being imported.

### Universal Words Cost Only A Class-Dependent Constant

Fix `c`. Over the localized coefficient ring `Z[1/c!]`, truncated BCH
and inverse BCH give two finite rational group words `ADD_c` and
`BRACKET_c` in TWO inputs. In every exponent-p group of class at most c,
`p>c`, these represent

```
ADD_c(g,h)     = exp(log(g)+log(h)),
BRACKET_c(g,h) = exp([log(g),log(h)]).
```

Here is a constructive way to see why no dimension-dependent free-Lie
calculation is hidden in that statement. Work once in the free
nilpotent Lie algebra on TWO formal generators through weight c.
Start the addition word at `gh` and the bracket word at
`g^-1 h^-1 g h`. At the first incorrect homogeneous weight k, express
the logarithmic error in an integral Hall/Lyndon basis. Each basis
bracket has a corresponding iterated GROUP commutator whose logarithm
equals that bracket modulo higher weight. Multiply by rational powers
of those commutators to cancel the error at weight k. Corrections have
weight k and introduce no lower-weight error. Repeat through c.

All denominators stay in `Z[1/c!]`: truncated exp/log introduces only
denominators with prime factors at most c; the integral Hall/Lyndon
change of basis introduces no extra denominators. This is also why the
prime condition is substantive. A rational power `g^(a/b)` becomes the
ordinary integer power `g^(a*b^-1 mod p)`. It is not a root oracle or
a discrete logarithm.

Let `W_c` bound the resulting number of group operations and powering
instructions, and let `B_c` bound their coefficient bit lengths. Both
depend only on c, possibly very badly. They are not functions of the
actual group dimension or p. For each fixed c, evaluating either word
takes `O(W_c log p)` collector calls by repeated squaring, plus modular
arithmetic polynomial in `log p+B_c`. A general implementation must
generate or certify the required tables; truncating a weight-14 table
cannot handle class 15.

### Refined-Flag Coordinates Need No Discrete Logarithms

Suppose the supplied normal form is

```
g_1^e_1 ... g_d^e_d,       0 <= e_i < p,
G_i = <g_i,...,g_d>,      G_(i+1) normal in G_i,
|G_i/G_(i+1)| = p.
```

Lazard correspondence transports this to a flag of Lie subalgebras
`L_i`, with `L_(i+1)` an ideal in `L_i` and codimension one. The
elements `b_i=log(g_i)` form an additive basis adapted to that flag.
The leading normal-word digit of an element in `G_i` is its coefficient
along `b_i` modulo `L_(i+1)`. This digit is already part of the INPUT
ENCODING; no black-box discrete logarithm is being solved.

To convert a normal word u to its additive coordinates, for i=1,...,d:

1. Read its current leading digit a at position i.
2. Record a, then replace u by `ADD_c(u,g_i^(-a))`.
3. The result lies in `G_(i+1)` and its logarithm is the old logarithm
   minus `a*b_i`.

After d steps the residual is the identity. Conversely, iterated
`ADD_c` of `g_i^a_i` represents `exp(sum_i a_i*b_i)`.
Each map uses `O(d W_c log p)` collector calls. Ordinary group
multiplication in step 2 would peel MULTIPLICATIVE exponents rather
than the required additive coefficients and is not interchangeable.
The flag need not be globally central or globally normal; only the
stated successive normality is used.

Compute `[b_i,b_j]` by `BRACKET_c` and the forward coordinate map for
each basis pair. This uses `O(d^3 W_c log p)` collector calls and stores
at most `O(d^3 log p)` bits of structure constants. Derived ideals,
adapted complements, normalizers, and known quotient bases then use
finite-field linear algebra with its arithmetic cost charged. For a
collector of cost `C_col`, multiply the collector counts by `C_col`
and add polynomial coordinate/arithmetic overhead. This bound does not
assert that the local machine-word `nmod_mat` backend handles all primes.

### Normal-First Chart And Clean Quantum Use

Once a public basis adapted to `N=[L,L]` is available, converting
`(n,q)` to an original normal word requires forming `exp(n)`, `exp(q)`
with the inverse map and multiplying. In the other direction, compute
`z=log(g)`, project to obtain q modulo N, and compute

```
n = log(g * exp(-q)).
```

The product is in `exp(N)` and the maps are mutual inverses. This uses
only a constant number of the polynomial-cost maps above. In particular,
the group input is not assumed already expressed in the preferred chart.

Both maps are deterministic bijections on the valid encodings. Compute
one map reversibly into a clean register, erase the original register
with the inverse map, and uncompute temporary work. Invalid bitstrings
can be assigned the identity extension outside the common valid domain.
This gives a permutation of the full encoding space, not a measurement
or a branch-dependent garbage label. Restricting the oracle through a
known public section likewise computes the lift, evaluates the original
hiding function, and UNCOMPUTES the lift.

Loops and repeated squaring are padded to their polynomial caps. Finite
gate approximation and valid-domain state preparation retain their
existing error budgets. No exponential-dimensional matrix needs to be
stored or synthesized. This is a reversible-compilation argument, not
an executed quantum circuit or a black-box presentation-acquisition
algorithm.

### A Concrete Failure And Its Correction At Class Four

The existing class-three inverse-BCH words are not valid unchanged at
class four. Put `[a,b]_G=a^-1 b^-1 a b` and

```
w=[g,h]_G,  u=[g,w]_G,  v=[h,w]_G,
A=[g,u]_G,  B=[h,u]_G,  C=[h,v]_G.

S3 = g h w^(-1/2) u^(-1/12) v^(1/12),
T3 = w u^(1/2) v^(1/2).
```

For `X=log(g), Y=log(h), Z=[X,Y]`, write
`a=[X,[X,Z]], b=[Y,[X,Z]], c0=[Y,[Y,Z]]`. Exact rational calculations in
the truncated free associative algebra give

```
log(S3) - (X+Y) = a/24-c0/24,
log(T3) - Z     = -a/3-b/4-c0/3.
```

All the group words A,B,C are central at class four, so the corrections
are

```
ADD_4(g,h)     = S3 A^(-1/24) C^(1/24),
BRACKET_4(g,h) = T3 A^(1/3) B^(1/4) C^(1/3).
```

The exact free-algebra certificate is not interpolation at sample points.
Separate finite controls evaluate these words using ONLY multiplication
and repeated-squaring powers in `UT_5(F_p)`, including a 127-bit prime.
They compare to independent matrix exp/log afterwards. Further controls
reuse the existing flag-peeling methods with these test-only corrected
words, in both a central flag and a refined flag not globally normal.
They recover the actual matrix logarithm coordinates and inverse map.

This closes a specific written public-access cost gap and falsifies a
literal class-three compiler reuse. It does NOT implement a production
general-class compiler, admit a full HSP result, or make inverse BCH
novel. Future wiring should use the established algebraic algorithms,
not infer correctness from the finite controls alone.

## 1. Remove The Normal Intersection

Set `N=[L,L]`, which is abelian, and `V=L/N`. Choose a public vector-space
section of `V`. Write group elements in normal-first coordinates

```
g(n,q) = exp(n) exp(q),      n in N, q in V.
```

Let `K=H intersect exp(N)`. In the actual mixed coset state, measuring
`q` leaves normal-register differences in `Phi(q)K`, where

```
Phi(q) = exp(ad(q)) restricted to N.
```

Apply the public inverse `Phi(-q)` and use ordinary abelian HSP sampling
to learn `K`. The class-three shortcut `Phi=1+ad(q)` is FALSE in general.
Here the exponential is the full finite sum, with at most `c` terms.

Use a fixed rank batch. With exact Fourier samples the estimate `Khat`
contains `K`, so checking the original hiding label on a basis of
`Khat` verifies equality. Membership alone does not verify completeness
without that inclusion. Approximate-QFT error is separately charged.

Because `K` is normal in `H`, the whole hidden subgroup lies in
`M=N_G(K)`. Restrict to `M`, then quotient by `K` using a clean public
section. This is not the invalid operation of quotienting all of `G`
by a nonnormal subgroup.

The normalizer is still linear:

```
log(M) = { x in L : [x,K] is contained in K }.
```

Proof: `ad(x)` stabilizing `K` implies its truncated exponential does.
Conversely, if `exp(ad(x))` stabilizes `K`, so does every polynomial in
`exp(ad(x))-1`; applying its truncated logarithm recovers `ad(x)`.
Nilpotence and `p>c` justify both finite inverse identities. This proof
does not truncate the action at first order.

Since `N` is abelian, `N <= log(M)`. The quotient is again metabelian,
and `H/K` is transverse to `N/K`, hence also to the quotient's new
derived ideal. Recompute the public derived ideal and section. If the
quotient is abelian, finish directly. Otherwise rename these objects
`G,L,N,V,H`, now with `H intersect exp(N)=1`.

## 2. Construct One Bounded-Degree Potential

Transversality implies `[H,H]=1`. Thus `log(H)` is a linear subspace
with injective projection onto a subspace `U<=V`. Write it as the graph
of a hidden linear map `a:U -> N`, and put

```
h(u) = exp(u+a(u)).
```

Choose a proof-only linear projection `pi:V -> U`. Neither this projection
nor `a` is supplied to the controller. For `u=pi(q)` and `r=q-u`, define

```
Q(q) = log( exp(r) exp(u+a(u)) exp(-q) ).
```

The product projects to zero in `V`, so `Q(q)` lies in `N`. Each of its
three input logarithms is linear in `q`. The truncated BCH expansion
contains only Lie words of length at most `c`. Therefore `Q` is a
polynomial of total degree at most `c`.

In particular the degree is **not c squared**: composing truncated BCH
series can produce written longer terms, but every Lie word of length
greater than `c` vanishes. This is a structural argument over the field,
not interpolation from a finite table. Denominators are invertible
under the standing `p>c` premise.

By construction,

```
exp(Q(q)) exp(q) = exp(r) h(u).
```

For `v in U`, the residual `r` is unchanged at `q+v`, and
`h(u)h(v)=h(u+v)`. Consequently

```
exp(q) h(v) = exp(-Q(q)) exp(Q(q+v)) exp(q+v)
           = exp(Q(q+v)-Q(q)) exp(q+v).
```

The second equality uses abelianness of `N`. Multiplying by `exp(n)`
gives the exact normal-coordinate increment `Q(q+v)-Q(q)`.
No public group splitting, commuting quotient lifts, or explicit
coefficients of the hidden potential are assumed.

This supplies precisely the coordinate-action premise of the existing
group-source Fourier lemma. Every normal character is uniform, including
zero, and its normalized quotient block is

```
rho(U,lambda.Q)[q,q']
  = |V|^-1 * 1_{q'-q in U} * chi_lambda(Q(q)-Q(q')).
```

Fresh ordinary oracle preparations supply independent blocks. The
existing Lean mixed-source theorem can be reused CONDITIONALLY on this
new construction; the general-class construction itself is not formalized.

## 3. Erase Degrees c Through 1

The proved unknown-support Kraus instrument accepts arbitrary unit
phases; it has no cubic restriction. Only its classical cancellation
controller needs to cover higher degrees.

For a conservative cost proof, introduce unknown parameters
`theta[a,alpha]` for all `n` coordinates of `Q` and all nonconstant
monomials `alpha` of total degree at most `c`. Their number is

```
M = n * (binom(m+c,c)-1),       m=dim(V), n=dim(N).
```

Store each packet's phase as a public linear map from these parameters
to its nonconstant monomial coefficients. Initially that map is given
by the observed normal character. Translation/scaling and summation
preserve linearity in the unknown parameters.

At a degree-`j` stage, form one equation for every parameter and every
degree-`j` output monomial. There are at most

```
E_j = M * binom(m+j-1,j)
```

equations. For input packet columns `v_i`, solve
`sum_i s_i^j v_i=0` with some `s_i != 0`. This cancels the leading
degree for every possible hidden potential simultaneously. The solver
uses only public coefficients and may receive adaptive, nonrandom
columns. Compress equation ROWS if useful, not source columns.

The published fixed-degree diagonal-equation theorem supplies a
polynomial arity `A_j(E_j)` and polynomial-time classical solver.
For j=1 use ordinary linear dependence with A_1(E)=E+1, not a
degenerate substitution into the higher-degree theorem's displayed bound.
There are only `c` stages. A disjoint tree uses at most
`product_{j=1}^c A_j(E_j)` fresh sources per erased sample, polynomial
for fixed `c`. All outcome tuples are accepted by the instrument; this
argument does not multiply probabilities of rare postselection events.
Zero-scale inputs are consumed, not recycled.

The smaller moment-rank bounds from the class-three audit may improve
this estimate, but are not needed for the scope conclusion. The
conservative bound already prevents hidden exponential dependence on
the dimensions at FIXED `c`. It says nothing favorable about practical
resources or increasing `c`.

After degree one is removed, Fourier sampling yields `U^perp`.
For exact image recovery use a fixed batch of at least
`m+ceil(log_p(1/delta))` samples; the rank failure bound is at most
`p^(m-t)`. This also supplies the cap for the certified early class-stop
rule below. No hidden-rank or line-only stopping rule is permitted.

## 4. Certified Class Descent To An Abelian Finish

2026-10-21. This is the preferred written completion. It removes the
separate nil-2/HPGP finishing dependency and does not need exact support
recovery at each level. It does NOT implement a general receiver, certify
novelty, or turn the source into a state-only algorithm.

### Why The Class Drops

Let the CURRENT group S have class r>=2, with abelian derived subgroup
N=S', and with H intersect N=1. Then H is abelian. Its full quotient
image has preimage T=HN, so

```
T' = [H,N] <= [S,S'] = gamma_3(S),
gamma_j(T) <= gamma_(j+1)(S) for j>=2.
```

The first equality uses that BOTH H and N are abelian and N is normal.
For the second, induction uses T<=S. Since gamma_(r+1)(S)=1, T has
class at most r-1. Equivalently, in Lie coordinates the public preimage
of the true quotient image is h+n and its first bracket lies in
[L,[L,L]]. This generalizes the previous class-three-to-class-two
observation; it does not incorrectly claim every HN is class two.

There is no new normalizer quotient after the initial one. Every later
ambient is a subgroup of that first quotient S_0, so its derived
subgroup is contained in S_0'. Transversality to S_0' implies
transversality at every subsequent restriction. Metabelianness is
likewise inherited. The same fixed hidden subgroup is retained.

### A Public Stopping Rule, Not An Exact-Support Requirement

In the exact-source model, erased Fourier samples give a subspace
Uhat containing the actual image U of H in S/N. Form its PUBLIC
preimage That. It contains H regardless of whether Uhat=U.
Compute the lower central series of That from public structure constants
and accept this restriction as soon as

```
class(That) < class(S).
```

This is a deterministic finite-field calculation, not a test involving
unknown H generators. Starting from a basis B of That, repeatedly span
[B,C_i], where C_1=That and C_(i+1)=[That,C_i]. At most r levels and
O(r*d^2) public bracket evaluations plus polynomial row reduction suffice,
with d the current Lie dimension. Testing only a decrease in dimension
would not establish this class-based bound.

If the public condition fails, collect another independent erased
Fourier sample, up to the fixed rank budget. Exact support recovery is
a sufficient fallback: once Uhat=U, the preceding lemma guarantees the
test passes. It is not necessary. A strictly larger Uhat may already
have a lower-class preimage and is then completely legitimate.

### Complete Core Control Flow

After the existing verified intersection/normalizer quotient:

1. If the current group S is abelian, go to the terminal step below.
2. Compute S', public coordinates, and the current nilpotency class r.
3. Prepare fresh ordinary-oracle cosets IN S. Use the common-potential
   source and degree-r erasure to accumulate quotient Fourier samples.
4. Form the nullspace Uhat and its preimage That. Recompute the public
   class. On a strict decrease, set S=That and restart step 1 with a
   new chart and new packet parameter basis. Otherwise continue step 3
   within its cap; return ABORT if no decrease is certified.
5. Terminal step: in abelian S, take a fixed batch of abelian Fourier
   samples. Their nullspace Rhat contains H. Check every basis generator
   against f(1) through the current original-oracle lift. On success
   Rhat=H; otherwise ABORT. Lift its generators and include the original K.

At most c-1 nonabelian restrictions occur. This is a finite induction,
not an unbounded recursive promise. At each accepted restriction H<=S,
the class strictly decreases, and H remains transverse. The terminal
membership checks certify completeness because Rhat is an OVERestimate
inside an ambient still containing H. They do not use secret advice.

Do NOT require the final answer's image to equal every intermediate
Uhat: that would reject correct outputs when the early class test used
a strict overestimate. The old projected-span certificate belongs only
to the alternative line-finisher route below.

### Source And Cost Boundaries

This descent uses the ordinary oracle. Prepare a uniform superposition
over each known smaller subgroup and evaluate the lifted original oracle
there. Do not postselect an S-coset from copies in a larger group;
that event can be exponentially unlikely. After the first quotient,
all subsequent inclusions compose inside ONE known quotient, with a
public lift back to its normalizer and then the original group. Their
collection, reversible arithmetic and oracle costs remain charged.

No phase packets carry over between descent levels. Conditional on a
legal controller history, the current subgroup/chart is fixed and its
fresh sources have the same newly defined unknown potential. Matching
dimensions alone still does not permit cross-level combinations.

If C_r(d,log p,eta) bounds one degree-r erased Fourier sample with the
source/controller budget already derived, a conservative core copy bound
is the SUM over at most c-1 levels of

```
(d + ceil(log_p(1/delta_level))) * C_r(d,log p,eta),
```

plus initial intersection and terminal abelian batches. It is not a
product of oracle-source costs across recursion levels: each level
queries a directly restricted ordinary oracle, not the previous level's
erasure routine. Within EACH sample, the product of diagonal arities
still applies. All bounds are polynomial only for fixed c.

Allocate failure across the initial intersection batch, all descent
rank batches, all field-solver aborts, and the terminal abelian batch.
The bounded retries and global approximation argument below apply.
Approximate leaked frequencies can exclude H while the public class
test still passes; terminal membership then need not recover the original
H. The new tests explicitly demonstrate this, so the certificate remains
ideal-model only, not an unconditional noisy-source guarantee.

The matrix reference follows an actual 4 -> 3 -> 2 -> 1 descent, with
ambient dimensions 8,7,4,2, never supplying H to its PUBLIC arithmetic
predicate. Further controls cover a valid strict support overestimate,
a dimension-only false shortcut, invalid frequencies losing H,
nontransversality, and rejection of a nonabelian derived ideal. Truth
generators supply only ideal test data and expected answers; this is
not execution of the full quantum sampling/controller.

### Alternative: Finish On Known Basis Lines

Do NOT reuse the class-three claim that `HN` is class two. It can have
class three already in a class-four group.

Instead, for each recovered nonzero basis vector `v` of `U`, form

```
T_v = exp(N + F_p*v).
```

This is a public subgroup and a split extension of the elementary
abelian `N` by `<exp(v)>`, a cyclic group of order `p`. Its hidden
subgroup `H intersect T_v` has order `p` and is not contained in `N`.
Thus it satisfies the PRECISE promised family in Ivanyos--Santha
Proposition 7 / Corollary 8, not a stronger arbitrary-subgroup reading
of that result. Its nilpotency class is bounded by `c`.

Restrict the original clean quotient hiding oracle to `T_v`. Apply the
published cyclic-complement HSP/HPGP algorithm, then lift the recovered
generator. The recovered generators for a basis of `U`, together with
the earlier `K`, generate the original `H`. If `U=0`, the transverse
hidden subgroup is trivial and there are no line calls.

Allocate the failure allowance across at most `m` calls, intersection
learning, support learning, field/diagonal solvers and gate error.
All subroutines need fixed polynomial caps, including on a bad earlier
rank estimate that violates a later promise. Verify the resulting
generators' hiding labels and projected spans; do not assume successful
rank learning for free. Approximate circuits should be charged in the
unconditional joint-state trace distance, not by dividing by an
exponentially small individual outcome probability.

## Checked Adaptive Composition

This section strengthens the proposed controller. It does not implement
it, and it is not a new novelty claim for subgroup verification or
standard quantum error composition.

### What The Controller Is Allowed To Remember

Fix the actual hidden subgroup H throughout an attempt. At every stage,
condition on the CONTROLLER transcript: observed normal characters,
shear outcomes, public random choices, and the classical data derived
from them. The invariant is that the live packets are a PRODUCT of
`rho(U,P_i)`, with each `P_i` described by its public coefficient map
against one common unknown potential parameter vector.

Fresh, independent ordinary-oracle preparations establish the invariant.
A merge acts only on its selected disjoint packets and a fresh target.
Conditioning on its recorded outcome leaves the other packets untouched
and gives exactly the proved branch kernel on the new target. Updating
the public coefficient map therefore preserves the invariant. A future
choice of scales or batch based on the transcript is legal. No assumption
that the resulting coefficient columns are independent or random is
needed by the diagonal solver.

At an erased root, the remaining constant phase disappears from the
density matrix: the output is exactly `rho(U,0)` for EVERY retained
transcript. It therefore decouples from the classical record. Fresh
completed trees give uniform `U^perp` samples even conditional on earlier
Fourier outcomes. This justifies the fixed-batch rank bound under the
allowed adaptivity, rather than assuming independent samples by name.

Two distinctions are essential:

- Trace out the hiding-function output of each coset preparation. Do
  NOT condition the proof on that unobserved label: doing so generally
  gives a pure coset state, not the mixed kernel used here. Do not feed
  those source labels back into packet selection. Separately, uncomputing
  the hiding output entirely would undo the needed coset dephasing.
  Uncompute the PUBLIC LIFT WORKSPACE, not the hiding-function output.
- All packets in a tree must refer to the same fixed hiding oracle,
  current quotient group, chart and parameter basis. Matching dimensions
  alone does not justify mixing different instances. Never reuse a
  measured source, even if its chosen scale was zero in this instrument.

The earlier correlated-coset and nonparallel-support controls show why
the product/common-support premises cannot be omitted. Bayesian
uncertainty about H is not a physical dependence between fresh sources:
the correctness statement is for each fixed H.

### Check Every Diagonal Witness

Before executing a merge, deterministically verify the proposed scales
in the ORIGINAL public coefficient matrix:

```
some s_i != 0,       sum_i s_i^j v_i = 0 in every equation row.
```

The test uses no unknown phase coefficients or hidden subgroup data.
It costs polynomially many field operations. An incorrect, malformed,
or all-zero witness aborts the attempt; a solver timeout does likewise.
This turns field-solving failures into detected aborts rather than
silent violations of the phase invariant. A valid witness is useful
regardless of how it was obtained. Row compression may accelerate the
solver but is not a reason to skip verification of the original system.

### Certified Descent Uses A Terminal Abelian Certificate

For the preferred class-descent route, the initial K membership check
certifies equality in the ideal model. Each subsequent exact-source
nullspace contains the actual quotient image, so every accepted lower-
class preimage contains ALL of H. This containment is the induction
invariant; exact intermediate image equality is not required.

In the final abelian ambient, the Fourier nullspace Rhat contains H.
Original-oracle membership of its basis gives Rhat<=H, hence Rhat=H.
Lifting and including K gives the original hidden subgroup. An incomplete
rank batch can cause a public class test or terminal membership test to
fail, but cannot cause wrong ACCEPTED output in this ideal computation.
There are no off-promise cyclic-complement calls in this route.

### Alternative Line-Finisher Membership And Image Certificate

In the IDEAL exact-source/exact-Fourier experiment, an intersection
estimate always satisfies `K <= Khat`. The earlier basis membership
check therefore certifies `Khat=K` whenever it passes. After that check,
the special normalizer quotient is legitimate and the hidden subgroup
in it is transverse to its derived ideal.

Exact phase erasure and Fourier sampling similarly imply `U <= Uhat`
for EVERY rank outcome, even when the finite batch has not learned U.
Run the bounded line finishers, then check their returned elements in
the original oracle and check that their quotient projections span
exactly Uhat. Reject malformed/noncanonical outputs before evaluation.
Always include generators of the verified K in the final generating set.

Let R be the subgroup generated by this proposed final set. Passing
oracle checks gives `R<=H`; inclusion of K gives `K<=R`. The image test
gives

```
Uhat = image(R) <= image(H) = U <= Uhat.
```

Hence the images are equal. Every h in H has some r in R with the same
image, so `h*r^-1` is in the kernel intersected with H, which is K.
Thus h is in R, proving `R=H`. This is a general elementary subgroup
argument, not a new theorem specific to the proposed quantum method.

Consequences for the controller:

- An overestimated Uhat can send a line finisher an input outside its
  promise. It still cannot yield a WRONG ACCEPTED output in the ideal
  model: either membership or the projected-span check must fail. The
  call MUST have a fixed time/output-size cap, even off promise.
- An HPGP mistake can also be detected at this final interface. The
  finisher's error bound controls the chance of abort, not the soundness
  of a passing ideal check.
- If Uhat=0, no transverse generator is needed; output the verified K.
  For an abelian current group, use the same checked abelian-Fourier
  nullspace directly, without a phase-erasure or HPGP call.
- Original-oracle membership checks cost O(d) further evaluations plus
  public lifting and finite-field span computation. They do not read
  the secret as verification advice. This check is NOT available from
  arbitrary coset-state-only access.

The inclusion hypotheses are indispensable. If approximate Fourier
leakage makes Uhat a PROPER SUBSPACE of U, membership and the observed
span can both pass for an incomplete subgroup. Omitting K can likewise
make a proper subgroup pass all quotient tests. These are explicit
counterexamples in `tests/test_nil3_arbitrary_subgroup_interface.py`.
Do not advertise this as an unconditional exact certificate under noisy
or approximate sources.

### Bounded Retries And Circuit Error

One ideal bounded attempt has no wrong accepted output under the
premises just proved. For certified descent, give intersection rank
failure, ALL descent rank failures together, ALL field-solver aborts,
and terminal abelian rank failure budgets of at most 1/16 each. Split
the descent allowance across at most c-1 levels; conditional bounds
hold for each public adaptive subgroup. For the alternative line route,
the analogous four categories are intersection rank, one quotient rank,
field solving and all line-finisher failures. On joint success the
chosen route accepts, so
its abort probability is at most 1/4. This union bound does not require
independence of the four events. Each new attempt uses fresh sources and
random choices; conditional on any previous controller history the
same bound applies to the fixed input.

For a target total failure epsilon in (0,1), use at most

```
R = ceil(log_4(2/epsilon))
```

attempts. Return an explicit ABORT if none accepts. The ideal final
abort probability is at most `4^-R <= epsilon/2`.

Compile the WHOLE bounded computation, including its classical record,
controlled branches and absorbing accept/abort outputs, to unconditional
joint trace distance at most epsilon/2 from that ideal computation.
For example, bound each attempt's channel error by epsilon/(2R), using
uniform gate/channel bounds and padding to its worst-case gate cap.
The usual channel hybrid/contractivity argument then bounds the total
variation of the final output distribution by epsilon/2. See
[Watrous, Chapter 3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf) for
the standard state/channel distinguishability framework.

Therefore wrong accepted output OR final ABORT has probability at most
epsilon. Source preparation, Fourier transforms, coherent collection,
and any other approximated quantum operation must all be included.
Exact field arithmetic and classical oracle-label equality are part of
the ideal input model; noisy hiding oracles require their own bound.
This does not claim exact prime-field QFT synthesis over a fixed finite
gate set or a zero-error physical implementation.

There is no division by the probability of a particular shear outcome.
For comparison, a perturbation of total variation eta can put eta mass
on a wrong result while an ideal accepted result has mass alpha. Given
acceptance, the wrong fraction is eta/(alpha+eta), nearly one when
alpha is tiny. An unchecked repeat-until-success or a rare-branch
conditional error estimate cannot replace the bounded joint calculation.

For the general finite-group ISS wrapper, allocate the requested error
over its polynomially bounded core calls and propagate ABORT explicitly.
This section supplies a core composition argument, not an executed
general-group retry budget or a replacement for the earlier ISS audit.

### Stream The Tree Without Reusing Copies

Choose deterministic arity caps `a_j>=2` for degree j, even if a
particular low-rank node could finish with fewer copies. One erased
sample has

```
L = product_(j=1..c) a_j                  fresh leaves,
N_j = product_(k=1..j-1) a_k              degree-j merge calls,
sum_j N_j <= L-1                         total merge calls.
```

The indexing matters: degree one is the root; degree c is closest to
the source leaves. Multiplying arities is the COPY cost, not the number
of quantum registers that must be simultaneously stored.

Generate children depth first, keeping the completed siblings while
building the next child. At a merge, allocate its fresh target BEFORE
measuring/consuming its children. At most

```
2 + sum_(j=1..c) (a_j-1)
```

quotient-sized packet registers are live. Add the normal/source-oracle
workspace and reversible arithmetic scratch separately. This is a
storage schedule, not a reduction in L or a license to recycle measured
sources. Public coefficient maps and the classical record are also
charged; retaining the entire record still costs polynomial space at
fixed c. Source, solver and arithmetic error budgets must be based on
ALL `t*sum_j N_j` merges for t Fourier samples, not only on tree depth.

Tests track every leaf's ancestry, the merge counts and the fresh-target
peak on nonuniform arity trees. Existing physical channel tests cover
the instrument; this scheduling control does not simulate a quantum
processor or substantiate a hardware resource estimate.

## Attempts To Falsify It

`tests/test_metabelian_phase_extension.py` uses ordinary matrix
multiplication in the regular representation of the free associative
algebra on two generators truncated at degree four. The generated
eight-dimensional Lie algebra has basis

```
X,Y,Z=[X,Y],A=[X,Z],B=[Y,Z],
C=[X,A],D=[Y,A]=[X,B],E=[Y,B].
```

Its derived ideal is abelian and its class is exactly four. The tests
reuse no class-three BCH formula. They check:

- Actual matrix exp/log, exponent `p`, and right multiplication by all
  seven elements of a transverse hidden line at all 49 quotient points.
- The section-word potential against that right action, with a nonzero
  normal chart origin. A characteristic-zero symbolic matrix logarithm
  has degree EXACTLY four, and reduces to the finite-field calculation.
- `1+ad(X)` fails on `Z`; the second-order exponential term is necessary.
- The preimage of the hidden line has class three, refuting nil-2
  completion. No abelian index-`p` subgroup exists in the whole fixture,
  so it is not already the published cyclic-complement input family.
- Each known basis-line restriction has the split cyclic interface and
  the expected univariate polynomial graph.
- `UT_5(F_7)` has noncommuting derived elements `E13,E35`, excluding the
  unsupported extension to ALL class-four groups.
- Existing public packet arithmetic correctly cancels a quartic leading
  term using an explicit restricted-prime witness. The production
  controller still REJECTS degree four; this test does not implement the
  general diagonal solver.

These finite controls try to break the extension; they are not its proof
or a new toy-oracle application. The general proof obligation is the
section-word argument plus the costed source/controller composition.

Other boundaries remain:

- **Nonmetabelian:** normal-register scalar Fourier analysis and additive
  potential cancellation fail when `N` is nonabelian. No claim beyond
  this proof's scope, and no general no-go theorem.
- **Growing class:** monomial counts, diagonal arities and tree depth
  lose the fixed-parameter guarantee. In particular this does not solve
  DCP via growing-class dihedral 2-groups.
- **Concrete classical attacks:** explicit low-degree polynomial-valued
  hiding functions remain subject to the derivative reconstruction
  attack. NIL3_POLYNOMIAL_HIDING_ATTACK.md now derives and implements
  it for bounded class c, with a full Bernoulli right-action field and
  explicit degree/characteristic guard, not only class three.
  A polynomial quantum potential does NOT imply such a
  classical-valued input oracle. Supplied solvable graph/code stabilizer
  instances remain subject to their existing polynomial baselines.
- **Transporter reductions:** CLASS_THREE_APPLICATION_AUDIT.md charges
  target-coset preparation at probability 1/|orbit|. Small orbits have
  classical traversal; generic amplification remains superpolynomial
  on superpolynomial orbits. This is not a universal transporter lower
  bound. Swap wreaths leave nilpotence at odd primes; regular p-wreaths
  contain C_p wr C_p, of class p and exponent p^2, so do not repair
  the fixed-class/large-prime interface.
- **Access costs:** no free Lie coordinates, public quotient sections,
  phase oracle, representation acquisition, or quantum state reuse.
- **Novelty:** no search result establishes absence of prior art.
  Independent expert review and a broader theorem-level comparison are
  still required before claiming a new HSP result.

## Prior Art And Next Work

The targeted corpus query found the existing growing-class central-descent
barrier and earlier overbroad no-go records, not an admitted result for
this fixed-class metabelian construction. Those are boundary checks, not
a novelty certificate.

Relevant primary sources:

- [ISS, 2010 author version, Theorem 2](https://www.irif.fr/~santha/Papers/iss12.pdf):
  subgroup/quotient-closed fixed-class reduction. Our proposed finite
  metabelian family is closed under those operations.
- [Ivanyos--Santha, 1503.09016v2](https://arxiv.org/pdf/1503.09016):
  Theorem 3 supplies fixed-degree diagonal solving; Proposition 7 and
  Corollary 8 supply the promised split cyclic completion. Those are
  borrowed results, not local inventions.
- [Imran--Ivanyos, 2304.08376](https://arxiv.org/abs/2304.08376):
  the established constant-class result additionally bounds prime
  divisors. That differs from the proposed large-prime metabelian core.
- [Cicalo--de Graaf--Vaughan-Lee, 2012](https://doi.org/10.1016/j.jalgebra.2011.11.031):
  effective BCH/inverse-BCH conversion is prior art. Only the publisher
  abstract was available in the earlier audit; this note does not import
  an unread detailed complexity proof.

### Theorem-Level Recheck And Simplification

The current pass re-read the SDE and cyclic-complement promises in
Ivanyos--Santha, rather than inferring scope from the title. The supplied
line inputs satisfy the cited promise, but that finisher is now OPTIONAL:
the certified class-descent argument uses only the diagonal solver and
ordinary abelian HSP after the shared group-source reduction.

The restriction principle is already present in the introduction and
algorithm of [Imran--Ivanyos](https://arxiv.org/pdf/2304.08376): learning
the commutative quotient image supports descent to a smaller group.
The local class-drop proof exploits transversality and metabelianness to
bound the number of such restrictions by c-1. Do not claim either
restriction or abelian Fourier sampling as a new primitive. Their
bounded-prime theorem does not by itself supply our large-prime source.

[DISW Theorem 5 / Lemma 6](https://arxiv.org/pdf/1107.2189v2) restricts
a given full polynomial-graph oracle to known domain lines. That does
not directly instantiate the unknown-support source used before
descent. The existing gauge and wrong-line counterexamples remain
relevant; this comparison is not a proof that no other reduction exists.

The recent [Morales preprint](https://arxiv.org/pdf/2608.05321), already
audited elsewhere in this repo, likewise does not cover a nonabelian
exponent-p core merely by its title. A scalar p-power-order action on
an elementary abelian p-group is trivial, since Fp* has order p-1.
For its quasi-Hamiltonian branch, any two cyclic order-p subgroups
permute; their product has order at most p^2 and is abelian. Hence an
exponent-p quasi-Hamiltonian group is abelian. This is a scope deduction
from its stated hypotheses, not a criticism of that algorithm.

Highest-priority review target is now the shared section-word source
and unknown-support phase erasure, plus the bounded ordinary-oracle
composition. The optional HPGP completion is no longer a critical proof
dependency. Independent review and a broader prior-art search remain
required; none of these comparisons certifies novelty. Do not keep
expanding the matrix fixture catalogue or treat the simplification as
a useful external application.

Mechanical follow-up remains separate: general-prime/fixed-degree
diagonal backend, arbitrary-rank controller and clean public
presentation interfaces. Do not start a large class-four simulation
campaign, admit a speedup, or relabel the class-three restricted receiver
as a general metabelian solver.
