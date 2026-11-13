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

