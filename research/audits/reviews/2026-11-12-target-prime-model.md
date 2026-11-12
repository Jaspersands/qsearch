# The prescribed target prime: finite-algebra bypass of curve coordinates

2026-11-12. Focused independent review. Read current `STATE.md`, the stable
native-normalization review, and the actual newly supplied primary sources
`audits/sources/surface_module_2026/buchmann_lenstra_orders.txt`, especially
Theorem 1.2, Sections 5.7--5.9, Algorithm 6.1 and Proposition 6.2, and
`lenstra_polynomial_algorithms.txt`, Lemma 5.24 with its hypotheses.
No Git, network, API, archive search, new code or numerical control.
Interpreter if needed: `/opt/anaconda3/bin/python`.

The parent redirected the highest-priority part of the task from a
prescribed-prime curve-model construction to the finite Galois-orbit
algebra after certified rational reconstruction. That bypass is valid
and has a primary-source polynomial BIT algorithm. It should replace
the stronger target-coordinate requirement where only Frobenius and
the finite module/operation data are required.

## Exact result and its input boundary

Supply a finite reduced commutative `Q`-algebra `A_Q`, with complete
multiplication tables and unit, of rank `D` and total bit size `H`.
Supply the relevant base-label algebra and the actual operation/deck
maps as explicit rational algebra maps. Assume this is the CERTIFIED
complete orbit algebra of the intended objects, and that its factors
are unramified at the prescribed rational prime `p`.

Then one can compute deterministically in `poly(D,H,log p)`:

* its `p`-maximal order, represented by a rational basis in the original
  coordinates;
* the faithful finite etale reduction `A_p` over `F_p`;
* the induced operation/deck maps and the Frobenius automorphism
  `a -> a^p` of `A_p`.

No integer factorization, maximal-order oracle, `p`-sized search,
or hypothesis `p>D` is required. The order's discriminant being a
`p`-unit is an explicit certificate of the final finite etale claim.

For the surface application this pays the target-prime operation
after a complete polynomial-size algebra for pairs `(b,E)` has been
certifiably reconstructed. One must retain `D=ell^{O(1)}` and
polynomial bit size as actual input bounds. The theorem does not
permit enumerating all torsion of a growing-genus Jacobian if that
would make `D` exponential. It also does not prove the upstream
reconstruction precision or supply a missing genuine arithmetic
linearization from a merely geometric action.

## 1. Why the auxiliary-prime result does not settle the original question

The stable trace-normalization note computes an integer `M` and
proves compatibility at primes outside its support. It cannot
declare a PRESCRIBED `p` acceptable when `p` divides `M`. An exact
characteristic-zero integral basis or RR basis may have bad
reduction at a prime where the underlying smooth object has good
reduction.

For example, replace the coordinate `y` in a good hyperelliptic
model by `Y=p^k*y`. The displayed equation becomes
`Y^2=p^(2k)*f(x)` and its reduction is nonreduced. Neither abstract
good reduction nor the existence of a rational characteristic-zero
normalization identifies a faithful integral basis in these
coordinates. A matrix pivot chosen over `Q` can likewise be
divisible by the prescribed `p`.

For a full curve model, normalization over `Z_(p)[x]` is a
two-dimensional problem. The earlier `Q[x]` trace lattice does
not automatically become a finite-dimensional `Z_(p)` lattice
that resolves every vertical condition. Merely saying "saturate
at p" is not a completed algorithm for that task. This review
does not promote a general prescribed-prime two-chart curve-model
theorem from the auxiliary-prime note.

There is an even smaller finite-algebra collision example. Take

```
A_Q=Q x Q,       gamma=(0,p).
```

The primitive polynomial is `T(T-p)`. Reducing the monogenic
order gives `F_p[T]/(T^2)`, collapsing the two points. But the
algebra is everywhere unramified; its correct order is `Z x Z`,
with idempotent `gamma/p=(0,1)`, and its correct reduction is
`F_p x F_p`. Thus the primitive polynomial alone is not a faithful
target-prime orbit presentation. The known-prime order algorithm
repairs exactly this failure.

## 2. Why the genuine orbit algebra is unramified in the native setting

This is a geometric INPUT VERIFICATION, not a claim that an arbitrary
small rational equation automatically has good reduction.

Let the native Lefschetz family be defined over `Z_p`, smooth off
the stated disjoint nodal sections, with `ell!=p`. The genuine
relative Jacobian `ell`-torsion and its full frame scheme are finite
etale over the smooth open base. The compact cover must be the
one defined by this native frame construction, with the asserted
tame local inertia at the horizontal branch sections. A rational
cover with similar branch counts alone is not this hypothesis.

Under those native hypotheses the normalization at a branch
section has, after etale localization, the standard tame local
form `u=s^e` with `p` prime to `e`, and is smooth over the DVR.
Away from the sections the cover is finite etale. This proves
the needed abstract good reduction of the compact cover. It is
used here to prove UNRAMIFIEDNESS of a finite arithmetic object,
not as a substitute for computing coordinates of a curve model.

Choose a rational fiber `a` whose reduction avoids the native
branch polynomial. Its degree `r` is fixed; among `0,...,r`
there is a suitable value when these residues are distinct.
Additional characteristic-zero presentation denominators can be
avoided by extending the finite grid by their charged degrees;
the assumed sufficiently large `p` allows distinct residues.
This is not enumeration of `F_p`. The frame label `b` over this
fiber is unramified. Over its unramified field, smooth proper
base change makes the genuine prime-to-`p` Jacobian torsion, and
any Galois-stable selected module `E`, unramified. Hence the
complete finite set of pairs `(b,E)` has trivial inertia at `p`.
Its finite orbit algebra is unramified.

The class label `E` and closed-divisor coordinates must be
distinguished from arbitrary individual support roots. Unique
canonical divisor coordinates in characteristic zero can have
poles, collisions, or a bad canonical-divisor chart modulo `p`
without ramifying their field of definition. The intrinsic class
remains unramified. Conversely, adjoining arbitrary individual
support roots can introduce extra ramification and a much larger
algebra; that is not the orbit input being used here.

If the reconstructed algebra fails the final unramified
discriminant test, the bypass does not authorize pretending it
is etale. Either the promised native orbit was not reconstructed,
the geometric unramifiedness premise was not met, or genuine
ramification is present.

## 3. Construct an actual integral starting order

The input may be a rational multiplication table, not a supplied
order or a monogenic field. Change its rational basis to include
`1`, obtaining `1,u2,...,uD`. Let `q` be a common positive integer
denominator of the structure constants. Then

```
O0 = Z*1 + sum_(i=2..D) Z*(q*ui)
```

is closed under multiplication: the nonconstant coefficients of
`(q*ui)(q*uj)` in this basis are `q*c_ij^k`, and its constant
coefficient is `q^2*c_ij^1`. They are integers. It is a full-rank
order in `A_Q`, with polynomial-size multiplication tables and
nonzero discriminant `delta0`.

Every rational basis change, denominator product and trace
determinant above has polynomial bit cost. This works in a
product of number fields without first factoring it into fields.

## 4. The actual known-prime algorithm and its cost

Buchmann--Lenstra Theorem 1.2 permits a supplied squarefree
integer `m`; its prime case is made fully explicit by Algorithm
6.1 and Proposition 6.2. The paper explicitly works with orders
in products of number fields as well (physical lines 293ff).
Its Sections 5.7--5.9 give multiplication-table, fractional-ideal,
and bit-size representations. These are the needed hypotheses.

For a current overorder `O`, choose the least positive `t` with
`p^t>D`. Compute the kernel of the `F_p`-linear map

```
O/pO -> O/pO,       z -> z^(p^t).
```

It is exactly the nilradical: nilpotents in a `D`-dimensional
algebra have nilpotence index at most `D`, while Frobenius is
injective on its finite reduced quotient. Modular binary
powering uses an exponent of bit length at most
`log_2 D+log_2 p+O(1)`. It does not perform `p` operations.
Take the inverse-image ideal `I` of this kernel in `O`; then

```
pO subset I subset O.
```

Replace `O` by its idealizer

```
O'=(I:I)={z in A_Q : z*I subset I}.
```

This is an overorder, and `O subset O' subset p^(-1)O`:
the latter follows by applying `z` to the element `p` of `I`.
The idealizer is computed by the polynomial lattice algorithms
in Proposition 5.8. A particularly concrete calculation here is
to form the action matrices of the basis elements of `O` on a
`Z`-basis of `I`, reduce them modulo `p`, and compute the kernel
of

```
F_p^D -> Mat_D(F_p),
(c_i) -> sum_i c_i*(multiplication by basis_i on I/pI).
```

The lifts of that kernel, divided by `p`, together with `O`,
generate exactly `(I:I)`. The basis is normalized by integer
Hermite form. This is a polynomial-size linear/lattice problem,
not a search for algebraic integers in a box.

If the order changes, its index increases by a positive power
of `p` and the discriminant valuation decreases by at least two.
Thus there are at most

```
floor(v_p(delta0)/2)
    <= log|delta0|/(2 log p)
```

strict steps. When the order stops changing, Proposition 6.2
proves it is maximal at `p`, with `p`-power index over `O0`.
This does not require computing or factoring the global maximal
order's discriminant.

Coefficient growth is explicitly paid by source Section 5.9:
every overorder is stored as a fractional ideal of the ORIGINAL
order `O0`. Its index is bounded by, and in the source's statement
divides, the original discriminant. Hermite numerators and
denominators therefore have uniformly polynomial bit size in
the original multiplication-table input. Equivalently, in this
prime-only iteration all denominators divide a bounded power of
`p` whose exponent times `log p` is bounded by `O(log|delta0|)`.
Re-normalizing in the original lattice prevents coefficient
growth from being hidden in an iterated rational change of basis.
Each nilradical, idealizer, Hermite, and multiplication-table
conversion has polynomial bit cost, and the iteration count
above is polynomial. This proves the claimed complexity.

The 2025 lecture Lemma 5.24 is NOT the same prime-only statement:
it computes a global maximal order when its squarefree integer
contains ALL noninvertible primes. It must not be invoked with
`d=p` unless that extra global hypothesis holds. The exact source
for the present task is Buchmann--Lenstra Algorithm 6.1 and
Proposition 6.2.

## 5. Faithful reduction and every supplied operation map

Let `O_p` denote the terminal order localized at `p`. Under the
unramified input hypothesis it is finite etale over `Z_(p)` and
its discriminant is a `p`-unit. Compute this discriminant to
certify the assertion. Set

```
A_p=O_p/pO_p.
```

This is the correct finite etale algebra of reduced orbit
points, even when the original separating scalar had collisions
or denominators at `p`. No p-integral canonical curve/divisor
coordinates have to be supplied or recovered.

Any supplied rational algebra map between such orbit algebras
preserves their `p`-integral closures: images of integral
elements satisfy the same monic equations over `Z_(p)`. Convert
the map to the computed bases by exact rational linear algebra.
Its coefficients have nonnegative `p`-valuation; denominators
prime to `p` are inverted when reducing. Their bit sizes remain
polynomial by the basis and input-map bounds.

Tensor products cause no new normalization oracle. The tensor
product of finite etale `Z_(p)` algebras is finite etale and is
already the `p`-integral closure in its rational algebra. Thus a
group-law comorphism `A_Q -> A_Q tensor A_Q` extends to the
computed orders. For a fiberwise law over a base-label algebra
`B_Q`, use `A_Q tensor_(B_Q) A_Q`. Its integral counterpart is
again finite etale. Explicitly, the diagonal separability
idempotent of the computed base order is obtained from its
invertible trace pairing and realizes this fiber product as a
direct summand of the ordinary tensor product. Its dimension
and linear algebra are polynomial in the charged ranks.

All actual deck actions, zero sections, addition maps and scalar
maps therefore survive in the faithful residue algebras. This
does not manufacture missing arithmetic maps from geometric
matrices: the genuine rational maps are part of the reconstructed
input and are checked as such.

## 6. Frobenius and finite-module extraction

Compute `F(a)=a^p` on a basis of `A_p` by binary powering. This
is an invertible `F_p`-linear map and an algebra automorphism.
On geometric points `phi:A_p->F_pbar`, precomposition gives

```
(phi o F)(a)=phi(a)^p.
```

Thus it encodes arithmetic Frobenius. If the downstream
cohomology convention uses geometric Frobenius, invert this
matrix. All supplied operation maps commute with the appropriate
Frobenius maps because they are now actual maps of finite
`F_p`-algebras.

The core algorithm outputs this intrinsic Frobenius algebra
deterministically; it need not split the algebra or take an
lcm of arbitrary residue degrees. If the existing finite-module
procedure requires geometric labels, its additional finite-field
factorization/point work remains charged. In the fixed-rank
`F_ell` module setting one can use a common extension degree
bounded by the actual base-label orbit degree times

```
ell^ceil(log_ell m) * product_(j=1..m)(ell^j-1),
```

where `m` is the FIXED module dimension. This kills every element
of `GL_m(F_ell)`. It is polynomial in numerical `ell` at fixed
`m`, so bounded randomized finite-field arithmetic/factorization
can perform the prior module extraction in polynomial charged
size and `log p`. This is a structural bound, not the potentially
exponential lcm of arbitrary factor degrees. Genuine transport
between base labels and the coefficient action are still the
previously required input maps.

## Final disposition

The original prescribed-prime curve-coordinate construction is
not proved merely by the auxiliary-prime normalization theorem.
Its naive use is falsified by coordinate rescaling and by the
two-point primitive-scalar collision above.

For the needed final arithmetic output, the new finite-algebra
bypass removes that requirement. Given the certified complete
polynomial-size orbit algebra and maps, and the genuine native
unramifiedness proof, the target-prime maximal order, faithful
reduction and Frobenius are fully paid by an explicit
polynomial-bit known-prime algorithm. No new target-adapted
curve model or canonical divisor representative is needed.

What remains outside this result is the certified construction
and rational reconstruction of that orbit algebra, including
its height/precision bounds and actual arithmetic operation
data. The bypass must not be used to assume those inputs.
No shared notes are changed by this review.
