# Semi-Elementary Descent: Complete Public Torsion Words

2026-10-22. Local correctness repair, UNDER REVIEW. This is ordinary
integer/finite-field algebra, not a new quantum algorithm, an independent
review, or an implemented black-box HSP reduction.

## 1. The Precise Issue

The small-prime branch of REES_COPY_ONLY_OUTER_REDUCTION.md imports the
semi-elementary reduction in [Imran--Ivanyos, Section 3, Proposition 1](https://link.springer.com/article/10.1007/s11128-023-04228-2).
At one step it needs the full preimage of the order-dividing-p subgroup
of the PUBLIC abelian quotient A=K/(K' H0). Reading its generator-powering
instruction as valid for an arbitrary generating list is insufficient.
The intended preimage is well defined; this note supplies a construction
with explicit input obligations. It does not refute the paper's main theorem.

The counterexample is ALREADY in CLASS_FOUR_PRIME_POWER_INPUT.md, Section 3:
in C_(p^2) x C_p, take g1=(1,0), g2=(1,1). Both have exact order p^2,
and form an irredundant generating list. Their top powers both equal (p,0).
They miss the entire hidden line <(0,1)>. Thus exact generator orders,
irredundancy, and taking each generator's last nontrivial p-power do not
certify A[p]. A genuine direct-sum basis would suffice, but is extra data.

There is a second obligation: keep all generators of B=K' H0 when lifting
the quotient torsion. Quotient representatives alone can omit the kernel.
Neither issue is a defect of the proposed clean Rees central instrument.

## 2. Replacement Without A Smith Basis

Let B be a known normal subgroup of K, with A=K/B an abelian p-group.
Fix original quotient generators g1 B,...,gk B. Require a COMPLETE square,
full-rank integer ROW relation basis R, so A=Z^k/row_Z(R). Rectangular
relations can first be converted to a row Hermite basis; completeness
must come from the public presentation algorithm, not this conversion.

Compute the finite-field space

```
C = {a in F_p^k : a R = 0 mod p}.
```

For each basis vector a, take any integer lift and form the integral row
x=(a R)/p. Evaluate the word g1^x1 ... gk^xk in that fixed order. Together
with ALL known generators of B, these words generate exactly

```
L = preimage_K(A[p]).
```

Proof of completeness: a -> a R/p mod row_Z(R) is a well-defined linear
map C -> A[p]. Changing the lift by p z adds z R, a relation. Conversely,
if p x is a relation, write p x=a R and reduce a modulo p. This proves
surjectivity. If a R/p=z R, invertibility of R over Q gives a=p z, proving
injectivity. The image is therefore all of A[p], with order p^dim(C).
Lifting and adjoining B gives the full group preimage, even when K itself
is nonabelian. Ordering lifts only changes their values inside B.

The preimage lattice S=row_Z(R, x1,...,xd) has exact index

```
[Z^k:S] = abs(det R) / p^dim(C) = [K:L].
```

The implementation independently checks this with integer Hermite form.
L<K exactly when A is not elementary abelian; trivial or elementary A
must not be forced to descend. Here and below elementary includes trivial.

For the mixed-generator example,

```
R = [[p^2, 0], [-p, p]],
torsion words = (p,0), (-1,1),
images = (p,0), (0,1).
```

Do not reduce these integer word exponents modulo p. In C_27 at p=3,
the correct word is g^9; reducing 9 modulo 3 destroys it.

## 3. Why The Hidden Intersection Survives

Maintain H0<=H and H0 normal in K, with H intersect K strictly larger
than H0 whenever H0<H. The normalizer initialization and subsequent
subgroups containing H0 have this normality property. Set B=K' H0.
If (H intersect K)/H0 is nontrivial, Cauchy's theorem supplies a nonidentity
element of order p in this finite p-group. A representative h is not in
H0, and h^p is in H0<=B. Its image in A therefore lies in A[p], including
the possibility of the identity. Consequently h is in H intersect L
but not H0. The required strict hidden-intersection invariant is preserved.

Notice that B need NOT be contained in H. The public quotient K/B here
is used ONLY for arithmetic and constructing the restriction subgroup L.
It is NOT permission to transport the hidden source into K/B using a
forward section. Restrict the source to L; the later legal source quotient
is by known H0<=H. HSMC's central-erasure mechanism is a separate operation.

Repeated non-elementary steps strictly shrink K. If |G|<=2^b there are
at most b strict descents per outer round. This repair adds polynomial
PUBLIC preprocessing, no hidden-source reads and no additional HSMC calls.
It does not change the previous b(b+1) hidden-call ceiling, but its public
presentation cost and failure probability remain part of the whole run.

## 4. Access And Complexity Obligations

Finite-field elimination, determinant and Hermite computation, integer
division, and binary group powering are polynomial in the supplied
relation bit length. The routine accepts p=2 and arbitrary-size primes;
it enumerates neither the group nor the field, and does not factor p-1.
The tests include the 127-bit Mersenne prime. This is not a timing claim.

Obtaining the COMPLETE relation lattice of the public abelian quotient
is still a paid presentation/kernel-learning task. The existing imported
abelian decomposition machinery can supply it; that quantum acquisition
is not implemented here. A supplied square lattice with p-power determinant
is not certified to describe the actual quotient merely because every
relation evaluates correctly. For example diag(9,3) consists of valid
relations in C_3^2 but gives an incomplete lattice and misses a torsion
direction after evaluation. The report explicitly leaves completeness false.

In an adaptive outer algorithm, amplify canonical public relation output,
charge its error to public preprocessing, impose clocks also on erroneous
histories, and use the existing first-error union bound. Never charge those
public group calls as zero runtime merely because hidden-source reads are zero.

## 5. Implementation And Falsifiers

- `theorems/abelian_quotient_torsion.py`: relation-kernel construction,
  exact lattice-index check, original-generator word lifts, report CLI.
- `tests/test_abelian_quotient_torsion.py`: mixed-generator loss, exhaustive
  small abelian torsion and hidden intersections, nonabelian UT3(Z/p^2)
  preimages, omission of the central kernel, redundant generators, arbitrary
  unimodular row-basis changes, incomplete relation input, and invalid inputs.
- `research/reductions/abelian_quotient_torsion.json`: standalone diagnostic
  from `python -m theorems.abelian_quotient_torsion --write`.

In the nonabelian control, B is the full center, A=C_(p^2)^2, and L consists
of (x,y,z) with x,y divisible by p and arbitrary z. Keeping only lifted
torsion words loses a hidden central cyclic subgroup. The implemented
preimage retains it, and exhaustive controls check every cyclic hidden
subgroup for p=2,3. These enumerations are tests, not the algorithm.
With nontrivial H0=<Z^p> and H=<X^p Z>, retaining H0 in place of the
whole B still fails: the insufficient preimage intersects H in just H0,
whereas the correct L contains H. Thus the adaptive invariant is tested
above an already learned hidden subgroup, not only from H0={1}.

Falsification targets are exact: a relation-complete input with wrong
preimage index; a missing order-p quotient element; a nontrivial hidden
intersection erased by the corrected preimage; or an uncharged public
presentation dependency in the claimed composition. Passing the finite
controls alone does not establish the universal argument.

No admission flags change. Full quantum outer implementation, independent
review of the Rees theorem, novelty determination, and a consequential
application remain open. Do not create another family of nearby torsion
benchmarks as a substitute for those obligations.
