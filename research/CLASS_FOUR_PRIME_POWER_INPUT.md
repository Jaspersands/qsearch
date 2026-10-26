# Class-Four Prime-Power Input And General-Exponent Reduction

2026-10-21. CONDITIONAL INPUT REDUCTION, not a new admitted HSP algorithm.
The proposed exponent-p receiver remains UNDER REVIEW. This note extends
its input transport, not its proof, practical feasibility or application
claims. The implemented component is a public group-word evaluator; the
quantum kernel acquisition and complete reduction are not implemented.

## 1. Replace The Field By The Correct Additive Ring

Assume a unique b-bit encoding of a finite p-group G, p>4 known, class
at most four, identity, s group generators and coherent multiplication.
Let M=p^e annihilate G. Knowing the exact exponent is unnecessary:
M=p^b is a valid loose bound when b>=1, since |G|<=2^b. All costs include
log M, not M. Handle the trivial zero-bit group separately.

Use exactly the ADD_4 and BRACKET_4 words from
[CLASS_FOUR_BLACK_BOX_INPUT.md](CLASS_FOUR_BLACK_BOX_INPUT.md), but invert
their denominators modulo M, NOT p. Their universal rational identities
only invert 2 and 3. The class-four Lazard correspondence gives an
additive Lie ring A with the same elements as G. Scalar multiplication
by an integer is ordinary group powering. A need not be an F_p space.
This applies known inverse BCH, not a new correspondence; see
[Cicalo--de Graaf--Vaughan-Lee](https://doi.org/10.1016/j.jalgebra.2011.11.031).

The original group generators' right-nested Lie brackets of lengths <=4
span A over Z/M: Jacobi gives closure, longer brackets vanish, and BCH
makes this span a subgroup containing all supplied generators. Write the
list as a_1,...,a_t, with t<=s+s^2+s^3+s^4. It need not be a basis.

The public map

```
F:(Z/M)^t -> A,  F(c)=ADD_i(a_i^c_i)
```

is an additive homomorphism. Unique encodings make its fibers exactly
the cosets of its kernel. All outputs are valid group elements constructed
from supplied generators; no recognizer for arbitrary b-bit strings is
needed. Evaluation uses O(t log M) original group multiplications, plus
reversible arithmetic and cleanup, and ZERO hiding-oracle queries.

## 2. Acquire One Genuine Additive Decomposition

Use known abelian HSP for ker F. Lift its generators to integer columns
and append M I_t; call the resulting matrix R. Its integer column lattice
is the full relation lattice and A=Z^t/col_Z(R). Compute Smith normal form
with unimodular transformations

```
P R Q = [D 0],  D=diag(d_1,...,d_t).
b_i = F(P^-1 e_i mod M), for d_i>1.
```

The b_i give a direct sum of cyclic groups of orders d_i, each dividing M.
This is the known kernel/normal-form decomposition method, not new here;
[Cheung--Mosca, Theorems 1 and 7](https://arxiv.org/pdf/cs/0101004) provide
the integer reduction and polynomial transformation bounds. The direction
P^-1 matters: these are lifts of quotient coordinates, not columns of P.

Amplify quantum kernel acquisition using the canonical HERMITE normal
form of the full relation lattice in its fixed original domain. Do not
majority-vote arbitrary Smith bases. Sound relations or exact orders of
reported generators do not certify that the kernel is complete.

The number of Fourier samples does not grow linearly with M. If the
annihilator B of the hidden kernel needs r<=t generators, independent
uniform samples generate B iff their images generate B/pB. For k=t+c
samples the ideal failure is

```
1 - product_(i=0..r-1)(1-p^(i-k)) < p^(-c)/(p-1),  r>0.
```

For r=0 it is zero. Approximate QFT/uniform-preparation errors are added.
Constant base success and logarithmic repetition suffice; integer work,
transforms and clocks remain charged. No exact variable-prime gate set
is assumed.

Acquire the bracket table without a coherent decoder. Given a public
bracket value z, let D_A=direct_sum_i Z/d_i and query the additive map

```
F_z:D_A x Z/M -> A,  F_z(c,u)=ADD(E(c),z^u).
```

For the correct basis its kernel is the cyclic graph
{(-u coord(z),u):u in Z/M}. A generating set must include an element whose
last coordinate u is a unit modulo p, hence modulo M. Invert u and recover
coord(z) modulo each d_i, then verify by forward encoding. Check the
kernel order is M and reject malformed outputs, but retain the probabilistic
completeness guarantee. This costs at most binom(r,2) further abelian-HSP
calls. With the original spanning list, 1+binom(t,2) is a fixed call cap.

The result is one public mixed-order Lie-ring chart. Bracket compatibility
with cyclic orders, alternation, Jacobi and nilpotency are checkable, but
these checks do not certify the chart is the whole group. Use fixed
polynomial clocks and error budgets even after incorrect setup. No
arbitrary encoded element has been coherently logarithmically decoded.

## 3. Extract Order-p Elements Without Erasing Short Factors

For a local Lie ring L with acquired cyclic decomposition (b_i,d_i),

```
L[p] = {x:p*x=0} = direct_sum_i <(d_i/p)*b_i>.
```

These are independent additive order-p generators. Also p[x,y]=[px,y]=0
for x in L[p], so L[p] is an ideal. Under BCH it is the exponent-p group
Omega_1(exp L)={g:g^p=1}, containing every subgroup of order at most p.
Its bracket table follows by module coordinates and integer division of
multiples of d_i/p, NOT division by p in Z/M. This gives a genuine F_p
Lie algebra for the proposed core. It can remain nonabelian.

Two tempting shortcuts fail in C_(p^2) x C_p:

- A common power M/p kills the short C_p factor; with a loose annihilator
  p^4 it kills every factor.
- The irredundant generators (1,0),(1,1) both have exact order p^2, but
  their p-th powers coincide. Correct orders and irredundancy do not imply
  an additive direct-sum decomposition.

The same counterexample matters in the SMALL-prime semi-elementary outer
reduction, where torsion is taken in a public abelian quotient rather than
in a Lazard Lie ring. SEMI_ELEMENTARY_TORSION_REPAIR.md gives a complete
row-relation-lattice alternative and retains the whole quotient kernel.
That quotient-level computation works also at p=2; it does not claim that
order-p elements form a subgroup of an arbitrary small-prime group.

The evaluator's p_torsion_from_decomposition checks individual orders,
not independence or completeness. A false supplied decomposition is not
repaired by those checks. For p=2,3 the order-p set need not be a subgroup;
the existing small-characteristic countercontrols still apply.

## 4. Public Normalizers And Quotients In One Chart

After acquiring the global chart for a p>4 Sylow subgroup, its later public
group computations use mixed-order module coordinates. Known subgroup
generators span a Lie subring after length-four bracket closure. Submodule
membership, intersections and quotients reduce to integer congruences and
Smith/Hermite normal forms. Do not replace these modules by vector spaces
modulo p: real subgroups can vanish under that reduction.

For a known subgroup K with additive Lie subring B, its normalizer is

```
N_A(B)={x:[x,B] subset B}.
```

Proof: for D=ad(x), D^4=0. Conjugation acts as exp(D). If it preserves B,
then exp(D)-I preserves B, hence its finite logarithm D preserves B;
conversely invariance under D implies invariance under exp(D) and exp(-D).
All denominators divide powers of 2 and 3 and are units modulo M. Checking
the condition on additive generators of B gives linear congruences in x.
The quotient N_A(B)/B inherits the bracket because B is an ideal there.
Integer quotient transformations supply public sections, not necessarily
group homomorphisms.

A prime-index chain in a quotient L follows by refining
P_0=L, P_(j+1)=p P_j+[L,P_j]. Iteration produces sums of
p^(j-i)*gamma_(i+1)(L), 0<=i<=min(j,3), which vanish for j>=e+3. Every strict step
loses an order factor at least p. Each P_j/P_(j+1) is central elementary
abelian, so refining a vector-space basis gives a central composition
series of length log_p|exp L|. Its reverse is the ascending chain needed
by the published hidden-subgroup reduction.

Keep the ORIGINAL Sylow chart throughout the normalizer recursion. The
logic and clean quotient-oracle proof are already in
[CLASS_THREE_HSP_THEOREM_DRAFT.md](CLASS_THREE_HSP_THEOREM_DRAFT.md),
section "Why The Published Recursion Calls A Legal Solver". This uses the
known [ISS Theorem 2 reduction](https://arxiv.org/pdf/0707.1260), not a new
recursion theorem. Each local first-nontrivial chain intersection has
order p; extract L[p] only for that local solver. Never restrict the
entire unknown H to Omega_1 once and declare it recovered.

Store public embeddings and quotient lifts into the original chart,
flattening maps rather than exponentially nesting oracle wrappers. A
local query computes its public lift, encodes it in G, queries f ONCE,
and reverses the public computation retaining input and hiding output.
No inverse encoding oracle is needed. Returned generators have known
coordinates in this chart and can be encoded into G.

## 5. Conditional General Class-Four Corollary And Costs

Conditional on the proposed exponent-p receiver, the preceding construction
handles all p>4 exponents in a unique-encoding class-four p-group. For a
general finite nilpotent class-four group, known quantum order finding and
factoring on supplied generators reveal its occurring primes. Project each
generator into a Sylow factor by powering with the Chinese-remainder
idempotent for its order. Nilpotence makes these direct-product projections;
projected generators generate each Sylow subgroup. These are paid quantum
preprocessing operations, not free classical inputs or new factoring.

For the p=2,3 Sylow groups use the EXISTING bounded-prime, bounded-class
algorithm of [Imran--Ivanyos, Theorem 1](https://arxiv.org/pdf/2304.08376).
Its interface requires a subgroup-state preparation UNITARY and its inverse.
From an ordinary reversible f oracle, these are available using known
solvable-group uniform-state preparation, with computation and inverse
charged. A bag of independently supplied coset states is insufficient.
Their exact-gate model is not silently inherited: for bounded error,
allocate circuit approximation error across all actual calls.

The large-prime setup is polynomial in s,b,log p and log(1/delta): bracket
spanning O(s^4 log M), a constant-error initial kernel
O(t*(t+2)*log M), and bracket-coordinate calls polynomial in t and log M.
Add integer normal forms, Fourier precision, reversible cleanup and
logarithmic amplification. These scales are not complete gate counts.
Only one global chart per large-prime Sylow is needed; subsequent module
operations and local Omega_1 extraction are classical public arithmetic.

There are at most b*(b+1) local large-prime handler calls across Sylows,
using the existing original-ambient recursion bound. Allocate total error,
for example, in four quarters to order/factor discovery, all chart setup,
all large-prime handlers and the at most two small-prime handlers. Use
a first-error union bound for adaptive calls and fixed polynomial clocks
on all histories. Gate approximation is included within each category.
Add this preprocessing/recursion to the existing receiver budget;
class_four_complete_budget.json still covers only its stated image calls.

This broadens a CONDITIONAL input corollary, not a proved core. It does
not cover growing class, nonunique encodings, state-only input or a useful
application. In particular it gives no general dihedral hidden-shift
algorithm. Polynomial overhead does not make the receiver's very high
existing exponents practical.

## 6. Implementation, Falsifiers And Next Work

ClassFourGroupWords now accepts a known annihilating prime power; inverses,
rational powers and operation caps use its bit length. It extracts order-p
generators from a PROVIDED genuine cyclic decomposition. Controls include
UT5 over prime-power rings with a 127-bit prime, loose annihilators, mixed
orders, a nonabelian Omega_1, incorrect order claims and failure of field
reduction for a torsion normalizer.

NOT implemented: quantum decomposition, module-normalizer backend,
coherent compiler, general recursion or complete receiver. Finite controls
do not prove these components exist or establish a speedup. The written
reductions give their interfaces and mathematical costs.

Falsifiers include a valid class-four/p>4 group violating the universal
words, missing additive directions after bracket closure, nonpolynomial
bit growth in the charged integer transformations, a required unavailable
coherent inverse, or failure of the proposed core. Explicit-action and
algebraic classical attacks still apply where their input promises hold;
opaque labels do not make an artificial instance a useful application.

Next main-model work: challenge the whole receiver or find a meaningful
external family surviving classical filters. Do not spend another pass
reproducing these input controls or wiring a claimed general solver.
