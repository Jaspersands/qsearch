# Native Carry: Output Normalization And A Classical Diagonal Slice

Local constructive derivation / external review pending. This supplies a
stronger actual classical first-carry baseline. It does NOT solve growing-
root preimages or implement uniform coherent normalized fibres.

## Normalize Outputs, Not Away The Hard Part

The vector coefficient matrix of pivot divided cubes is the invertible F3
prefix minor S: c_label-2a==c_label+a modulo3. Left-multiply the n equations
by S^(-1). This preserves their common zero set and gives one divided cube
per output equation. Coupled quadratic terms and shared free variables
remain. The transformed values are NOT the literal native digit residual;
only their zero predicate is equivalent. No rank-one-cubic claim is made.

## Disjoint Kernel Blocks Remove Mixed Cubics

Let B have rows b_i, the n dense affine pivot slopes in k=M-n free trits.
Partition the free coordinates into blocks of at most n+1. In each block
with nonzero nullspace, choose a nonzero kernel vector v_t and extend it
by zero outside the block. Full blocks always yield a vector. The v_t have
disjoint supports, are independent, and B*v_t=0 over F3. They span a slice
u=sum_t v_t*z_t with at least floor(k/(n+1)) parameters.

Every ordinary L_b(u)^2 vanishes on this slice. For the divided cube,

```
D_b(u)=[(sum b_l*u_l)^3-sum b_l^3*u_l^3]/3 (mod3),
```

disjoint supports remove cross-block terms in the subtracted sum. The
integer sums b.v_t are multiples of3, so every mixed term in the first
cube, after dividing by3, also vanishes modulo3. Pure parameter cubes
reduce by z_t^3=z_t over F3. Therefore

```
D_b(sum_t v_t*z_t) = sum_t D_b(v_t)*z_t.
```

This is a genuine degree reduction, not treating a divided cube as an
ordinary cube. After output normalization, the restricted equations are

```
constant_i + sum_t linear_it*z_t + quadratic_it*z_t^2 = 0.
linear_it = normalized_linear_i.v_t + D_(b_i)(v_t).
quadratic_it = normalized_diagonal_i.v_t^2 + b_i.v_t^2.
```

The three choices per column contribute0,linear+quadratic,quadratic-linear.
A standard classical meet-in-the-middle search solves this vector-sum
instance using3^floor(t/2) stored left assignments and at most3^ceil(t/2)
right assignments. Both counts, memory caps, incomplete searches and failed
slices are charged. A result is verified against the original native word
map, not just the restricted equations. The solver uses only public labels.

Verification uses complete parameter enumeration for small slices. For a
larger slice it uses a unisolvent F3 grid for canonical polynomials of total
degree at most3: zero, all one-coordinate trit choices, three two-coordinate
choices, and one all-one point per coordinate triple. The grid separates
every possible coefficient. Together with the degree contract it verifies
the complete function without enumerating3^t points. It does NOT supply an
exhaustive solution count or uniform solution samples; those fields remain
unknown unless separately computed.
External directions can satisfy all kernel/disjointness conditions while
having been selected using higher labels. Their selection provenance remains
UNKNOWN. Only the implemented deterministic low-slope block policy claims
low-only selection, and its choices are independently replayed. Kernel
validity or a metadata flag alone does not prove population independence.

## Mass And Existence Are Separate From Search

The slice has fraction3^(t-k) of the complete low-prefix word domain.
Projecting an existing uniform prefix state onto it must pay that mass.
Preparing the slice directly avoids that projection but changes the input;
it does not implement the original full normalized row. A witness is not
uniform coherent sampling. Failure on one slice is not absence of words.

For fixed low labels, prefix basis and target-low digit, random first higher
original label digits change only the constant and linear coefficients of
the first carry system. Writing d=h_a+h_c, their contribution is
sum(h_a)+sum(d_j*t_j). The prefix free-coordinate identity block gives a
surjective linear map to all k linear coefficients, independently of the
constant. Thus IID uniform higher digits induce uniform independent affine
masks, one per output and cohort. An invertible output normalization
preserves that distribution. The source law is a premise, not measured by
the artifacts; choosing targets or slices using higher-label information
can violate this stated model.

For an injective slice with t parameters, pairwise-independent zero indicators
give mean mu=3^(t-n), variance mu*(1-3^(-n)), and

```
Pr[slice has a solution] >= mu/(mu+1-3^(-n)).
Pr[slice has a solution] <= min(1,mu).
```

For the full prefix with B independent higher-label cohorts, the analogous
no-solution bound is min(1,(3^n-1)/(B*3^k)). These are POPULATION statements.
They do not guarantee a given dataset, independence of repeated slices on
that dataset, an efficient solver, a coherent sampler or higher-root recovery.
The variance statement permits zero-solution examples, unlike an invalid
appeal to underdetermination alone. Proof-fixture label perturbations are
only checks of this distribution map, NOT a chosen-label oracle for a solver.

There is also a useful exact coefficient identity: the restricted quadratic
columns are S^(-1) times the sums of the ORIGINAL low a-label vectors,
weighted by v_t^2 on free sites. This follows from
normalized_diagonal+b=S^(-1)*(c-a)-S^(-1)*(a+c)=S^(-1)*a over F3.
Conditional on all low slopes a+c, IID uniform original low a labels remain
independent. Since the directions use only those slopes and have disjoint
supports, these quadratic columns are independent uniform F3 vectors.
Together with the higher-label affine masks, this identifies the restricted
system with a random three-choice vector sum (choices0,L+Q,Q-L), under the
stated original label law. It is not an ability to choose the given data,
a proof of hardness, or a speedup theorem.

## Research Decision

The actual mixed cubics admit a concrete classical degree-reduced search
baseline. In the current k about n^2 regime it has about n slice parameters
and exponential meet-in-the-middle work, not a Shor-level algorithm.
A claimed first-carry quantum improvement must beat this same-original-label
baseline and preserve the row distribution it actually needs. Other affine
restrictions, better block choices, simultaneous quadratic methods and later
carry representations remain high-upside directions. No general quantum
lower bound or unconditional cryptographic hardness is inferred.

Falsifiers: overlapping supports ignored; a nonkernel vector admitted; a
restricted witness called a full uniform row; omitted failed slices or
memory; fresh-label independence assigned to repeated tries; mod9 witnesses
called full-root preimages; or output normalization treated as solving.

Run `python theorems/native_carry_diagonal_slice.py --write` and its tests.
