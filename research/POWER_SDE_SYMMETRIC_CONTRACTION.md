# Quadratic-Arity Symmetric Power SDE

28 October 2026. Local mathematical deduction with one independent automated
adversarial review and exact implementation controls. NOT human review,
established novelty, a Lean theorem, or a quantum speedup.

## Question And Answer

Argon's review suggested exploiting IID central-character labels to reduce
SDE batch size. A stronger route works on **arbitrary public columns**.
For fixed d>=2, a prime p with d dividing p-1, and

```
p >= 16*d^(2*d+2),
M = (r+1)*((d-1)*r+1),
```

any M vectors v_i in F_p^r admit a constructively found nonzero vector s
with `sum_i s_i^d*v_i=0`. The randomized algorithm has expected polynomial
arithmetic complexity in input size and log(p) for FIXED d. Its local
implementation caps uniform scalar draws and exactly verifies the original
equations; it does not enforce a total clock on its arithmetic dependencies.
The bound on p is sufficient, not necessary or optimized.

Update: the optional [finite-randomness implementation](POWER_SDE_RANDOMNESS_BUDGET.md)
now caps root splitting and bit rejection under one failure allowance. The
reference/default implementation and the full receiver clock remain distinct.

This is a CLASSICAL solver used within a proposed quantum receiver. The
input vectors may be dependent, adversarial, repeated, or zero. No oracle,
hidden subgroup, hidden phase, random-label promise, or label resampling is
used. An accepted arithmetic witness is not a quantum algorithm discovery.

## Two-Level Collision Tensor

Let z_0,...,z_(d-1) be distinct representatives of the d nonzero dth-power
cosets. Let W be the kernel of the linear form z on F_p^d, of dimension d-1.

For each block of r+1 original vectors, compute a nonzero ordinary linear
dependence. Multiply the whole dependence by a nonzero scalar to put one
chosen nonzero coefficient in coset 0. Write each nonzero coefficient as
`z_i*b^d`. Group its vector, with root weight b, into cell i. Then the d
cell values T_i satisfy `sum_i z_i*T_i=0`. Their representation supports
are disjoint, and cell 0 has nonempty support with nonzero root weights.

The first d-1 cells determine the last, since z_(d-1) is nonzero. Therefore
`(d-1)*r+1` such blocks have a nonzero dependence using only the first d-1
cell values. Normalize that dependence into coset 0 again, decompose its
coefficients, and multiply the child root weights by their new roots.
This produces d^2 cells T_ij with disjoint representation supports, and

```
sum_i z_i*T_ij = 0 for each j,
sum_j z_j*T_ij = 0 for each i.
```

Both relations follow from the first-level identities and the second-level
dependence. The omitted last coordinate follows by the first relation;
the implementation checks EVERY axis rather than trusting that inference.
Cell T_00 has nonempty support. Its VECTOR VALUE is allowed to be zero.
No division by any cell value is performed.

The column count is `(r+1)*((d-1)*r+1)`. This uses the first two levels of
the [Ivanyos--Santha collision scaffold, Lemma 12](https://arxiv.org/html/1503.09016v2),
with the constrained dimension replacing the ambient d*r bound.

## Symmetric Contraction

Find distinct nonzero t_i such that every

```
C_ij = z_i*z_j*(t_i+t_j)
```

is a nonzero dth power, including the diagonals. Fix
`t_0=(2*z_0^2)^(-1)`, so C_00=1. The contraction vanishes because

```
sum_ij C_ij*T_ij
 = sum_i z_i*t_i * (sum_j z_j*T_ij)
 + sum_j z_j*t_j * (sum_i z_i*T_ij)
 = 0.
```

This is an ORDERED-pair sum. Equivalently it has diagonal terms C_ii*T_ii
and off-diagonal terms C_ij*(T_ij+T_ji), i<j. There is no extra factor 2 on
the off-diagonal coefficient. The diagonal IS `2*z_i^2*t_i`.

Take a dth root of each C_ij and multiply every stored root in that cell by
it. Disjoint supports give a well-defined original-coordinate witness.
All represented weights remain nonzero; in particular C_00=1 protects the
distinguished support. Both even and odd d work. Neither -1 nor 2 needs to
be a dth power: the entire expression C_ij is tested and rooted.

## Constructing The Scalars

Given distinct nonzero t_0,...,t_(j-1), a uniform proposed t=t_j must satisfy
k=j+1 prescribed multiplicative-coset conditions:

```
2*z_j^2*t in (F_p^*)^d,
z_i*z_j*(t+t_i) in (F_p^*)^d,  0<=i<j.
```

The k affine roots `{0,-t_0,...,-t_(j-1)}` are distinct. Also exclude the
at most j previously chosen values, to preserve distinctness for later
stages. These exclusions are charged even if some coincide with affine roots.

Here is the prescribed-coset count, including zero corrections. On the
complement D of the k affine roots, expand each power indicator using a
character chi of order d. The all-zero exponent tuple contributes p-k.
For a nonzero tuple e in `{0,...,d-1}^k`, let s be its support size. The
associated polynomial has s distinct roots, with at least one multiplicity
not divisible by d, so it is not a constant times a dth power, including
for COMPOSITE d. The affine multipliers contribute unit-modulus factors.
[The standard Weil bound, stated in Martin--Yip Lemma 2.2](https://arxiv.org/html/2403.04312v2#S2),
bounds the complete sum by `(s-1)*sqrt(p)`. Removing the k-s unused affine
roots costs at most k-s. This is at most `(k-1)*sqrt(p)` in total. Thus
the number before the old-value exclusions is at least

```
(p-k)/d^k - (1-d^(-k))*(k-1)*sqrt(p).
```

After exclusions a convenient weaker lower bound is

```
N_k >= p/d^k - k*sqrt(p) - (k-1).
```

For k<=d and p>=16*d^(2*d+2), both subtracted terms are at most
`p/(4*d^k)`. Consequently `N_k/p >= 1/(2*d^k)`, uniformly over EVERY
admissible preceding prefix, not only a typical prefix.

Set `K_j=2*d^(j+1)*B` trials, B>=1. Conditional stage failure is at most
`(1-1/(2*d^(j+1)))^K_j <= exp(-B) <= 2^(-B)`.
The union bound is `(d-1)*2^(-B)`. Independence between completed stage
outputs is unnecessary; each new draw must be conditionally uniform.

The coset-generator sampler tests exact order d of `g^((p-1)/d)`. A uniform
nonzero g succeeds with probability phi(d)/d, so J failed trials have
probability `(1-phi(d)/d)^J`. Total sampling abort is bounded by the sum of
this quantity and `(d-1)*2^(-B)`, clipped at one. These retries depend only
on public data and do not consume or redraw source labels.

## Cost And Prior Art

For fixed d, both the number of constraints and d^d rejection overhead are
constants. Field powering, linear algebra and degree-d root extraction have
polynomial/expected-polynomial algorithms in their ordinary parameters.
There is NO polynomial guarantee uniform in growing d. The field threshold
and rejection constants are large, and the implementation is not a
low-overhead quantum compilation.

The published solver already has quadratic arity for d=2 without this
large-field guard; neither that case nor its asymptotic order is new.
The inspected general construction gives an odd-degree O_d(r^d) collision
bound and a general O_d(r^(d*ceil(log2(d+1)))) bound. These are sufficient
algorithmic bounds, NOT lower bounds. The local all-degree large-field
closure is not stated in those inspected sections; a targeted search and
automated review do not establish priority or novelty.

The earlier cubic method already reaches `(r+1)*(2r+1)` for all relevant
prime fields, so it remains preferred for reduced degree 3. The odd-power
exterior method reaches fewer field regimes than the published general
solver but more than this symmetric method: degree5 at p601 is a retained
fallback, not a quadratic-arity claim. The controller first reduces the
exponent to g=gcd(d,p-1), and checks the ORIGINAL degree after Bezout lifting.

If this arithmetic is inserted into the proposed fixed-class Rees recursion
with all required independent sources and clock/error guarantees supplied,
each of its c-1 erasure stages can use O_c(n^2) labels once p exceeds the
degree-only thresholds. The resulting bookkeeping upper bound is
O_c(n^(2*c-1)) original hiding queries for O(n) terminal samples at constant
failure allowance. This is a CONDITIONAL RESOURCE DEDUCTION, not an executed
general-class receiver or an update of the manuscript's certified schedule.
The original lift factor c is absorbed in O_c. Actual reduced degrees/ranks
can improve the count. Classical retry costs are separate from source count.

## Falsifiers And Unresolved Obligations

### Small-Field Obstruction For The Entire Two-Level Closure

28 October follow-up: the field restriction is not merely a loose sampler
estimate. The following local deduction rules out EVERY universal two-level
coefficient contraction at d=p-1, p>=5, including nonsymmetric choices with
zero entries. It does not rule out other algorithms or prove a quadratic
arity lower bound.

Let z list F_p^* and W=ker(z^T). A coefficient matrix C annihilates every
tensor in W tensor W exactly when

```
C = z*a^T + b*z^T
```

for some a,b. To see completeness, extend a basis of W to the whole space:
the W-by-W block must vanish. Equivalently, the right-hand space has
dimension 2d-1 and is contained in the annihilator, whose dimension is
d^2-(d-1)^2=2d-1. Every such C has rank at most2.

At d=p-1 all dth powers, INCLUDING zero, lie in {0,1}. If a nonzero binary
matrix C above has rank2, its column space contains z. Choose two actual
columns x,y as a basis, so z=alpha*x+beta*y. Its coordinates then belong
to {0,alpha,beta,alpha+beta}, giving at most THREE distinct nonzero values.
But z has p-1>=4 distinct nonzero coordinates, a contradiction. If rank(C)=1,
either a,z or b,z is dependent, so its row space or column space contains z.
A one-dimensional space generated by a nonzero binary row/column cannot
contain z, which has distinct nonzero entries. Thus C=0 is the only choice.

The exact control enumerates every matrix via its first row and column.
Writing u_i=z_i/z_0, all other entries are forced by

```
C_ij = u_j*C_i0 + u_i*C_0j - u_i*u_j*C_00.
```

Only 2^(2d-1) binary borders need checking. At p5,d4 all128 borders and at
p7,d6 all2048 borders leave only C=0. A p3,d2 positive control gives the
four nonzero matrices with three entries equal to1, showing the obstruction
really requires p>=5. A separate exhaustive matrix enumeration verifies
the border formula against direct tensor pairing.

This targets closure from ONLY the two axis identities. A particular
collision tensor may have additional relations allowing a contraction;
the test does not show all such tensors are realized by the recursive
builder, and it does not reject every input at these primes. Do not promote
it to an impossibility result for SDE, the Rees receiver, or all two-level
algorithms that exploit additional information.

### Literature Scope Rechecked

The targeted search and reread of [Ivanyos--Santha, Proposition10 and
Sections2--3](https://arxiv.org/html/1503.09016v2) confirm the inspected
comparator: its cubic construction uses three collision levels. The local
large-field two-level closure remains a candidate arithmetic contribution,
not established priority. [Martin--Yip, Lemmas1.1 and2.2](https://arxiv.org/html/2403.04312v2)
already supply the character-sum ingredients; their standard nature must
not be presented as new. Finding no subsuming result in targeted searches
is not evidence that no such result exists. Independent expert review of
the complete composition remains the next gate before a publication or
novelty claim; no external contact has been made.

### Remaining Boundaries

- A tensor failing either axis identity, overlapping supports, or an empty
  distinguished support invalidates the construction. Tests and runtime
  checks target these, including a nonempty support with zero vector value.
- Dropping diagonal constraints, inserting a second off-diagonal factor 2,
  or absorbing signs as roots for even d invalidates the argument. Controls
  use p=2^128-275, d=4, where neither -1 nor 2 is a fourth power.
- Repeated affine roots can invalidate the character bound. Zero, duplicate
  and opposite offsets are explicitly tested and rejected.
- Small fields are outside the uniform sampling proof, not evidence of
  impossibility. The controller fails closed where no backend is supported.
  Nor does fixed small p justify a rank-constant fallback: syndrome DP has
  p^r states. At p3,d2 the columns e_1,...,e_r,e_1 have no nonzero witness,
  so an arbitrary-input r+1-column small-field claim is actually false.
- Seeded finite controls establish reproducibility and exact witnesses, not
  statistical evidence for the uniform success bound. That bound is the
  character-sum argument above.
- The reference mode does not cap FLINT root extraction or uniform-integer
  internals. The separate bounded mode caps both, but prime validation and
  deterministic arithmetic still have separate dependencies. The current
  Lean receiver assumes TOTAL policies; neither aborting implementation
  instantiates that assumption.
- No hard native application, classical lower bound, practical speedup,
  generic-group cryptanalysis or cryptosystem attack follows. The matched
  classical stabilizer/orbit/semantic filters remain necessary.

## Implementation And Reproduction

`theorems/power_sde.py` implements the scalar sampler, two-level tensor,
support-preserving contraction, and original-equation checks. The weighted
controller selects it in the certified regime. No hidden phase evaluator
is available to either routine.

```
python qsearch.py power-sde --write
python qsearch.py power-sde --bounded-randomness --write
python qsearch.py odd-power-sde --write
python qsearch.py validate
```

Reports are `research/reductions/power_sde.json` and `odd_power_sde.json`.
The new tests cover the symbolic tensor identity, independent exact affine
coset counts, even nonresidue signs, adversarial/zero labels, bounded aborts,
wrong roots, invalid promises, exponent lifting and actual symbolic weighted
phase reduction without hidden evaluation. Final executed checks and the
review disposition are recorded in `research/AGENT_HANDOFF.md`.

## Independent Review

The same focused read-only reviewer first checked the exterior argument,
then independently checked the symmetric extension and finally its source
implementation. No algebraic or implementation defect was found. The
review explicitly verified composite-degree character sums, root exclusions,
the full ordered-pair identity, the diagonal factor 2, nonempty T_00 support,
uniform conditional stage bounds and caps. It also supplied the small-field
counterexample above. The reviewer did not run tests, review concurrent
controller changes, or claim novelty/human validation. The parent owns the
integration checks and retained all scope qualifications.
