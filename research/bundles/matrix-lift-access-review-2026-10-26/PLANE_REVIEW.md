# Independent Review: Consecutive-Pole Plane Adapter

Date: 2026-10-26. Verdict: **ACCEPT CONDITIONALLY**.

Audited `../one-point-plane-adapter-2026-10-26/PLANE.md`, final reread SHA-256
`5193ec2cf4eeb2c6d7599df0a6263eb7a7b5ec64572c195525721fe610fc0154`.
Its only observed mid-review change was a formatting correction in the
opening claim; the mathematical content was unchanged.
I read the compact-module handoff only to identify its required interface;
I did not audit that construction or duplicate its separate review.

## 1. Findings

I found no counterexample to the adapter under its stated smooth-curve,
complete-section-ring and certified compact-module promises. The colon
formulas, exact pole orders, birationality including inseparability,
coefficient bound, one-dimensional kernel and base-field descent all hold.
In fact the resulting polynomial has total degree **exactly** 2g+2.

The Lauder--Wan application is valid: a constant-variable plane equation
is the needed input, even when singular. Conditional on the compact-module
gate, this closes the *theoretical fixed-characteristic exact-order-access*
gap identified in the earlier reviews. It does not compute a native order
in this audit, establish a practical running time, or remove other native
divisor/differential/normalization obligations.

Keep three qualifications explicit:

1. **Degree 4 is sufficient only for choosing the functions.** Recovering
   their relation uses the true ring through degree `4g+4`. A certified
   all-degree representation with polynomially bounded arithmetic is a
   substantive independent premise, not a consequence of dimension counts.
2. **Polynomial in p is not polynomial in log p.** Fixing p = 100003 gives
   a theoretical polynomial bound as g grows, not a claim that this p is
   practically small for the published counter.
3. **The determinism of the counter does not derandomize module setup.**
   Given the certified module, this adapter is deterministic linear algebra.
   If obtaining that module is only Las Vegas expected-polynomial, the
   composed matrix-to-order route inherits that qualifier.

These qualify the conclusion, rather than refute the text's conditional
claim. No new uniform polynomial-system-solving or native-search theorem
is established here.

## 2. Colon Hypotheses And Exact Poles

Write k = F_q, ell = 2g+2, R_j = H^0(X,jH), and
`W_j = H^0(X,2H-jO)`. We use complete section spaces, not a proper subsystem
or values at a finite set of columns. O is a known k-rational smooth point.

For `1 <= j < ell`, the two factors in `W_j W_1` have degrees

```text
deg(2H-jO) >= ell+1 = 2g+3,
deg(2H-O)  = 2ell-1 = 4g+3.
```

Both exceed the `2g+1` multiplication threshold. Their products span
`H^0(4H-(j+1)O)`. Global generation of 2H then gives

```text
{z in R_2 : z R_2 subset H^0(4H-(j+1)O)}
    = H^0(2H-(j+1)O).
```

For justification, at every geometric point choose a section of 2H that
does not vanish there; imposing vanishing on its product with z forces
the required local order of z. This includes nonreduced multiples of O.
The multiplication and division primitives are
[Khuri-Makdisi, Lemmas 2.2 and 2.3](https://arxiv.org/html/math/0105182).
All thresholds are safely satisfied at the final iteration as well.

Next choose any nonzero `h in W_ell`, and write E for its zero divisor
as a section of 2H. Then `E >= ell O` and `deg E = 2ell`.
For j = 2g,2g+1,2g+2, the residual line bundle `2H-jO` has degree at
least ell, so W_j has base divisor **exactly** jO, geometrically.
Consequently

```text
z W_j subset h R_2
  iff div(z) + jO >= E
  iff z/h belongs to L(jO).
```

There is no extra constraint in the reverse direction: if f belongs to
L(jO), then `div(hf) >= E-jO >= 0`, so hf really belongs to R_2. Thus the
second colon computes precisely `V_j = h L(jO)`. It is important that h
is chosen to vanish at least ell times at O. Choosing an arbitrary h in
R_2 would truncate these spaces and break the deduction.

Extra zeros of h, including extra vanishing at O, are harmless: the colon
forces their cancellation in z/h. No divisor factorization or local
parameter is needed to enforce this condition.

All three j are greater than 2g-2, hence Riemann--Roch gives
`dim V_j = j+1-g`. Their successive dimensions differ by one **over k**.
Ordinary k-linear basis extension therefore finds

```text
z_x in V_(2g+1) minus V_(2g),
z_y in V_(2g+2) minus V_(2g+1).
```

With m = 2g+1 and n = m+1, the quotients x = z_x/h and y = z_y/h have
pole divisors exactly mO and nO. Strict membership tests supply the exact
orders; merely finding elements in V_m and V_n would be insufficient.
No genericity, large-field argument or extension-field choice is needed.
Storing these sections as quadratic representatives requires the supplied
low-degree presentation/conversion maps, not just their dimensions.

## 3. Birationality And Inseparability

Let L = k(X), K = k(x,y), and let Y be K's smooth projective model over k.
The constant field remains k, since K is a subfield of the geometrically
integral function field L and contains k. The resulting nonconstant map
`pi: X -> Y` is finite and flat. These properties do not require
separability; see [Stacks, Lemma 53.2.4](https://stacks.math.columbia.edu/tag/0CCL)
and [Lemma 53.2.3](https://stacks.math.columbia.edu/tag/0CCK).

Every pole of x on Y has a point above it, which must be a pole of x on
X. Hence x has just one pole Q on Y, and pi's fiber over Q is supported
at O alone. Since O is k-rational, so is Q. Finite flatness makes the
length of this fiber equal to the **total** field degree `[L:K]`.
For its extension of discrete valuation rings, the fiber length is
`e(O/Q) [k(O):k(Q)] = e(O/Q)`. Therefore

```text
[L:K] = e(O/Q),
ord_O(x) = e(O/Q) ord_Q(x),
ord_O(y) = e(O/Q) ord_Q(y).
```

It follows that `[L:K]` divides both m and n and is therefore one.
This is a defect-free finite curve-map argument, not an unjustified use
of a separable-only valuation theorem. It rules out purely inseparable
and mixed inseparable quotients as well.

Applying the same fiber-length argument to x: X -> P^1 gives
`[L:k(x)] = m`, including inseparable multiplicity. At least one of m,n
is prime to p; that coordinate is separating. However, **x itself need
not be separating**, and the relation-recovery algorithm must allow a
minimal polynomial with zero derivative in its V variable.

Rationality of O is used essentially in the displayed degree equality.
With an arbitrary nonrational closed point, a residue-degree factor remains
and the written proof is no longer valid. The recovered rational O meets
this requirement without any assumption about the original H's support.

## 4. Integrality, Valuations And The Unique Relation

The finite morphism defined by x identifies its inverse image of A^1
with X minus O. Its coordinate ring is finite over k[x]. As y is regular
there, it is integral over k[x]. The minimal polynomial of y over k(x)
therefore has coefficients in the integrally closed ring k[x]. Since
`L = k(x)(y)` and `[L:k(x)] = m`, it has the form

```text
F(U,V) = V^m + sum_(j=0..m-1) a_j(U) V^j,   a_j in k[U].
```

Normalize the infinite valuation of k(x) by `v_infty(x) = -1`. It has
only one extension to L, namely `(1/m) ord_O`. For any extension of
v_infty to an algebraic closure, every k(x)-conjugate of y consequently
has valuation `-n/m`. Use m roots counted with inseparable multiplicity,
not just the number of distinct embeddings. Elementary symmetric sums
then give

```text
v_infty(a_j(x)) >= -(m-j)n/m,
deg a_j <= floor((m-j)n/m).
```

Cancellation can improve this bound, never worsen it. The constant term
is, up to sign, the product of all m roots. There is no sum to cancel, so
its valuation is exactly -n and `deg a_0 = n`. This also proves that the
U^n coefficient is nonzero, even when the extension is inseparable.

Thus the weighted degree of F for weights (m,n) is exactly mn. Because
n = m+1, every allowed exponent pair satisfies `i+j <= n`; the term U^n
makes total degree exactly n. An independent geometric check is that
the three sections 1,x,y of O_X(nO) have no common zero: 1 works away
from O and y works at O. They define a birational plane map whose pulled
back hyperplane has degree n, agreeing with this degree computation.

The evaluation homomorphism `k[U,V] -> k(X)` has kernel (F): F is monic,
irreducible over k(U), and primitive over k[U]. A nonzero multiple F*G
has weighted degree `mn + deg_weight(G)`, since weighted leading forms
multiply in a domain. Therefore no nonconstant multiple fits the bound
mn, and the kernel restricted to the displayed monomial set M is exactly
one-dimensional. This justifies both normalization by the V^m coefficient
and the required rank check.

After multiplication by h^n, this polynomial identity is precisely the
linear relation among `z_x^i z_y^j h^(n-i-j)` in R_(2n). Multiplication
by the nonzero h^n cannot create a relation in an integral section ring.
The exponent n-i-j is nonnegative for every element of M. No saturation
or unbounded elimination of the original projective variables is hidden here.

The resulting affine plane curve is geometrically integral. Indeed
`k[x,y]` embeds into the geometrically integral function field k(X), and
this injection remains an injection into a domain on extension of constants.
Its smooth projective normalization is X over **k itself**, not merely an
extension-field twist. Thus the normalization's Jacobian has the required
original-field order. One must not substitute the smooth-plane genus
formula for the genus of this potentially singular model.

## 5. Growing Degree And Descent: Conditional Interface

The high-degree interface required from the separate module audit is:

- A faithful graded-ring isomorphism with the actual recovered section
  ring, not agreement merely through a few tested degrees.
- Known embeddings of the original k sections h,z_x,z_y and compatible
  low-degree multiplication/evaluation maps.
- Homogeneous normal forms and generator actions whose storage and
  multiplication costs remain polynomial through degree `2n = 4g+4`.
- If arithmetic uses k' = F_(q^b), an explicit base-field embedding,
  polynomially bounded b, and charged field arithmetic/conversion costs.

I take this interface as a premise and make no finding on whether the
handoff's proposed construction or certificates establish it.

Under that premise, the resource claim is valid. In the stated shifted
free module over two degree-one variables, homogeneous degree d has
O(gd) scalar coordinates. At d = 2n this is O(g^2), not the number of
monomials of degree d in O(g) independent projective variables. Here

```text
|M| = (m^2+3m+4)/2 = O(g^2),
dim R_(2n) = 2n*ell + 1-g = O(g^2).
```

Each requested column is a product of n factors of degree two. Repeated
application of the known degree-one actions to the stored quadratics,
or precomputed degree-two actions, computes it in polynomial cost with
intermediate degree at most 2n. A straightforward kernel calculation on
the resulting O(g^2)-by-O(g^2) scalar matrix costs O(g^6) field operations;
this is just a coarse bound for that final elimination, not for the whole
adapter or counter. The O(g^2) output coefficients require O(g^2 log q)
bits. There is no exponential dense-monomial expansion in this argument.

For scale only, g = 41 gives 3,571 columns and an ambient R_168 dimension
14,072. These are theoretical dimensions; no such matrix was constructed
or timed here.

For descent, the input monomials are still defined over k even if their
coordinates are stored in a k' basis. Flat base change preserves the
kernel of the k-linear section map. Its dimension remains one, and its
unique vector normalized to have V^m coefficient 1 is fixed by
q-Frobenius. Check each coefficient `c^q = c`, then invert the known
embedding k -> k' by linear algebra. This is polynomial in b and log q.

No Frobenius action on the extension-dependent module basis needs to be
guessed to justify this: the relation coefficients refer to the original
ordered monomials. Choosing x or y only over k' would remove this argument;
the parent's explicit k-linear choices avoid that problem. Counting over
k' and attempting to infer an order over k is neither used nor justified.

## 6. Exact Lauder--Wan Scope

[Lauder--Wan, Corollary 3, pp. 582-583](https://library.slmath.org/books/Book44/files/18lauder.pdf)
gives a deterministic algorithm for the Jacobian order of the smooth
projective curve birational to a geometrically irreducible affine input.
It explicitly includes a "possibly singular plane model". For one equation
in two variables, the bit complexity is polynomial in its degree d, the
characteristic p, and a where q = p^a. The field is supplied by an
irreducible degree-a polynomial over F_p. There is no requirement p > d.

The proof on pp. 610-611 extracts the weight-one polynomial P(T) from
the affine zeta function by removing root-of-unity factors; the desired
Jacobian order is P(1). Thus singularities and missing points do not require
an externally supplied smooth plane equation or prior Jacobian order.

**Application, not a new counting theorem:** here the ambient variable
count is 2, equation count is 1, and d = 2g+2. The source's polynomial
bound therefore becomes polynomial in g,p,a. At fixed p = 100003, this
is polynomial in g and a; for q = 100003, a = 1. With variable p it does
not establish polynomial dependence on log p. No practical bound follows.

This resolves the source-matching issue that would remain if one applied
a fixed-ambient-variable theorem directly to O(g) recovered coordinates.
Intrinsic curve dimension one alone would not justify that application.
The explicit two-variable adapter is doing necessary work.

Unlike the preceding sampling relaxation, this route **computes** zeta
information to obtain h rather than dispensing with it. Provided the
module premise is discharged, h need no longer be an independent oracle
for the fixed-characteristic promised-input family. That is a theoretical
dependency improvement, not a native execution receipt.

## 7. Independent Inseparable Control

To avoid duplicating the parent's elliptic/colon controls, I tested the
smooth projective model of the characteristic-3 curve

```text
v^3 - v = t^5.
```

It has genus 4 and one rational point O at infinity, with pole orders
3 for t and 5 for v. The usual Artin--Schreier genus and pole formulas
apply since 3 does not divide 5; see
[Scholten--Zhu, Section 1 and Lemma 3.1](https://arxiv.org/html/math/0105005).
Set x = t^3 and y = v^2. Their pole orders are exactly 9 and 10, as
required by m = 2g+1 and n = 2g+2, while the x-map is inseparable.

Exact polynomial reduction over F_3 and a separate FLINT kernel calculation
gave:

| Check | Result |
| --- | --- |
| Monomials with `9i+10j <= 90` | 56 |
| Rank of their reductions in the function ring | 55 |
| Kernel dimension | 1 |
| Normalized relation | `V^9 + V^6 + V^3 - U^10` |
| Strict-weight monomials / rank | 54 / 54 |
| Partial derivatives | `F_V = 0`, `F_U != 0` |
| Rational inverse identities | Both verified exactly |

The inverse is

```text
t = y(y-1)^2/x^3,
v = t^5/(y-1).
```

These are function-field identities, with no claim that their displayed
denominators are nonzero at every point. Reduction verified
`v^2(v^2-1)^2=t^10` and `v(v^2-1)=t^5` exactly. It also verified the
displayed relation after substituting x=t^3,y=v^2. Thus a zero derivative
in V does not break birationality or the monic weighted-kernel argument.

This was an inline symbolic control using SymPy 1.14.0 and python-flint
0.9.0 in the existing review environment. It did not use the parent's
tests, compact-module construction, native columns, or any point-count
implementation. The general assertions above rest on proofs, not this test.

**Subsequently added parent controls.** I read `plane_control.py` and
`test_plane_control.py` in the parent directory and ran the latter read-only
with bytecode and pytest cache writes disabled: **10 passed**. Their
product/colon spaces agree with the supplied genus-1/genus-2 pole bases;
their relations are computed in the true R_(2n), not by point fitting.
They specialize to H = ell O and h = 1 as a 2H-section, so they do not
test arbitrary H or off-O zeros of h. The general colon proof handles
those cases. The cases (g,p) = (1,3),(2,5) test characteristic dividing m,
but not an inseparable x-map: their equation has derivative
`2 eta d(eta) = 2 dt`, so x = eta is separating. The genus-4 control above
is complementary. None of these controls is a recovered native backend.

## 8. Status And Sharp Next Step

The geometric ingredients are standard Riemann--Roch, section multiplication
and division, finite curve maps, and valuation/minimal-polynomial arguments.
The counting theorem is Lauder--Wan's existing result. The contribution
here is a source-matched constructive deduction from the particular
recovered-algebra interface. Neither a new general counting theorem nor
a priority claim for one-point plane models is warranted.

The earlier unresolved exact-order gate should now be stated conditionally:

```text
recovered true low-degree algebra and rational O
  + certified polynomial-cost all-degree compact module
  -> original-field birational plane equation of degree 2g+2
  -> Lauder--Wan exact h in polynomial time for fixed characteristic.
```

**Next step:** obtain the independent compact-module verdict and state its
precise faithfulness, degree-growth, extension-field and setup-cost contract
as the adapter's input theorem. If that verdict is positive, the theoretical
fixed-p order objection is resolved; the next distinct task is engineering
and measuring a source-faithful implementation, not searching for another
order oracle. Kernel dimension, leading coefficient, Frobenius-fixed
coefficients and exact ring substitution should be exportable checks, but
they cannot replace the input curve/module promises by themselves.

No native genus-41 adapter, zeta polynomial, or Jacobian order was computed.
No claim is made about effective mod-two auxiliary search, its length
budget, or the final native normalization. Only this new review file was
written; parent files, earlier reviews, Git and UI were left untouched.
