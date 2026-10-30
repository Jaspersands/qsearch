# Compact Residues And Conductor Principality Decisions

Date: 2026-10-30. Constructive arithmetic interface, with independent
automated adversarial review; not an external human peer review.
This closes a specific representation obligation; it is not a new quantum
primitive, a new hardness result, or an implementation of quantum S-units.

## Question And Input Contract

Can a nonmaximal-order principality decision consume enormous units without
expanding them? Yes, for the specified compact power-product representation
and finite-modulus interface below. This does not automatically extend to
arbitrary arithmetic circuits, expanded matrix witnesses, or division orders.

Let O=O_K be given by an integral basis, coordinates of 1, and an exact
multiplication table. Let m be a nonzero integral ideal with explicit HNF
basis and a verified factorization `m=product_p p^a_p`. Constructing O and
factoring m are separately charged tasks, not hidden free preprocessing.
For nonzero, explicitly represented field elements gamma_j and signed
binary integers e_j, the input is

```
alpha = product_j gamma_j^e_j.
```

Each gamma_j has polynomial-bit rational coordinates; its exponent may
have an exponentially large numerical value. The goal is alpha mod m
when alpha is integral at every p dividing m, or a report identifying a
negative valuation at one such prime. This is local integrality only.

The algorithm below has deterministic bit cost polynomial in the explicit
field, factor, prime-ideal and modulus input sizes and in
`sum_j bit_length(2+abs(e_j))`. In particular the modulus parameter includes
`M=ceil(log2 Norm(m))`. It is NOT enough to charge only bit lengths of
compressed prime-power exponents: over Q, modulus `2^(2^t)` and residue
`2^(2^t-1)` have O(t)-bit power descriptions but exponential expanded output.

## Local Evaluation Without Expanding Exponents

Fix a prime power p^a dividing m.

1. Compute p^2 by ideal multiplication and HNF. Some additive basis element
   pi of p is not in p^2, otherwise p would be contained in p^2. Choose
   one by exact membership tests. Thus v_p(pi)=1, with polynomial-bit
   coordinates. No principal generator of p or approximation search is
   needed; pi may have other prime divisors.
2. Write each gamma_j=c_j/d_j, c_j in O, d_j a positive integer, and compute
   `v_j=v_p(c_j)-v_p(d_j)`. These individual valuations have polynomially
   bounded MAGNITUDE: `v_p(c_j)*log Norm(p)<=log abs(Norm(c_j))` and
   `v_p(d_j)*log Norm(p)<=[K:Q]*log d_j`. The small-coordinate numerator
   norm is a polynomial-bit determinant. Membership in successive ideal
   powers computes the valuations. Norm(gamma_j) alone is not a valid
   bound, since local valuations may cancel in that rational norm.
3. Form `u_j=gamma_j/pi^v_j` explicitly. Invert multiplication by pi over
   Q when needed. Since |v_j| is polynomially bounded and pi has small
   coordinates, u_j has polynomial-bit numerator and denominator. Every
   u_j is a p-unit. Crucially, the potentially huge exponents e_j are
   not used during this normalization.
4. Evaluate each u_j modulo p^a using the division method proved below.
   The results are units in O/p^a. Invert a residue by solving
   `x*O+p^a=O` with HNF preimages, and use binary modular powering for
   negative as well as positive e_j.
5. Compute the integer `w=sum_j e_j*v_j` in binary. If w<0, report failure
   of local integrality. If w>=a, the local residue is zero. Otherwise
   return `pi^w * product_j (u_j mod p^a)^e_j` in O/p^a. All modular
   products are reduced as they are formed; no large exact unit is built.
6. Combine the prime-power residues by ideal CRT, returning a canonical
   HNF representative modulo m.

The exponent sum w has polynomial bit length even when its individual
summands are enormous or nearly cancel. In the only branch needing pi^w,
one has 0<=w<a. The quotient-ring multiplication count for binary powers
is `O(sum_p sum_j bit_length(2+abs(e_j)) + sum_p log(2+a_p))`, in addition
to polynomially many ideal/lattice operations. This is not a gate count
for the upstream quantum number-field algorithms.

One explicit size accounting uses n=[K:Q], r factors, s modulus primes,
T bits for the multiplication table and 1, H bits for the c_j,d_j,
P bits for prime-ideal HNFs, M=ceil(log2 Norm(m)), and
L=sum_j ceil(log2(2+abs(e_j))). Hadamard's determinant bound gives

```
V = n*(H+T+2*ceil(log2(n+1))+2),
abs(v_j) <= V,
B = O(H+n*(V+1)*(P+T+log(n+1))).
```

Here B bounds normalized-factor numerator/denominator sizes. All subsequent
ideal precision has log norm at most M+nB, and the total bit cost is
polynomial in (n,r,s,T,H,P,M,L). This accounting includes the integral basis
actually supplied; an ill-conditioned or oversized representation is not
silently charged only by log discriminant.

## Division By A Nonunit Denominator

A normalized u=c/d may have d divisible by the rational prime below p,
even though u is a p-unit. Reducing numerator and denominator separately
and inverting d is therefore invalid. Let t=v_p(d); then v_p(c)=t.
Solve the additive lattice congruence

```
d*x == c (mod p^(a+t)),       x in O.
```

There is a solution, unique modulo p^a, because

```
d*O + p^(a+t) = p^t,
{x in O : d*x in p^(a+t)} = p^a.
```

Both identities follow by comparing ideal valuations. Away from p the
prime-power ideal is the unit ideal. The restriction x in O in the second
identity matters: the unrestricted fractional ideal `d^(-1)*p^(a+t)`
need not equal p^a. HNF with preimages for the generator matrix
`[d*I | basis(p^(a+t))]` supplies x. Its residue is exactly u locally.

There is no exponential precision requirement here. If the denominator of
the normalized factor has B bits, then

```
log Norm(p^(a+t)) <= M + [K:Q]*B.
```

B is polynomial in the original small-factor and field data. It does not
depend on the magnitudes of e_j. This is why one cancels local valuations
BEFORE exponentiating, rather than multiplying huge numerators and
denominators and attempting to cancel afterward.

A split-prime control is u=(3-sqrt(2))/7=1/(3+sqrt(2)) at
p=(7,sqrt(2)-3). This u is a local unit despite its denominator 7.
If r_k lifts sqrt(2) with r_k=3 mod 7 to precision 7^k, its residue is
`(3-r_(a+1))/7 mod 7^a = (3+r_a)^(-1) mod 7^a`. Using only precision
7^a leaves seven possible answers; the extra digit selects the unique
correct answer. Exact tests check the lattice sum and kernel identities,
not just the rational identity. Global integrality is intentionally absent.

Zero factors and undefined negative powers are outside the input contract.
The argument is for products of small factors, not general compact sums:
additive cancellation can introduce different precision obligations.

## Application To A Nonmaximal Order

Let R be an explicit order in O, f=(R:O) its conductor, and let I be a
full integral R-ideal. Check `R*I subset I` and `I+f=R`. These hypotheses
imply invertibility. Set

```
G=(O/f)^*,       V=(R/f)^* subset G,
E=image(O^* -> G).
```

If f=O, then R=O and there is no conductor correction. For proper f the
finite rings are explicit additive-lattice quotients. With h=[O:R], one
has h*O subset f, hence `log |O/f| <= n*log h`; their explicit size is
polynomial in the order input. Factorization and finite unit-group
coordinates remain charged arithmetic tasks.

The known conductor criterion is

```
I principal over R
  iff IO=beta*O for some beta, and (beta mod f) belongs to V*E.
```

Proof: coprimality gives I=IO intersect R. If I=gamma*R, then
gamma=beta*u for an O-unit u, and gamma is a unit modulo f in R/f.
Conversely, membership provides u with beta*u in (R/f)^*. Consequently
gamma=beta*u belongs to R, gamma*R is coprime to f, and
`gamma*R=gamma*O intersect R=IO intersect R=I`.

For the extension-contraction equality, choose 1=i+t with i in I,t in f.
If x belongs to IO intersect R, then xi belongs to I and xt belongs to
f*IO subset I, so x belongs to I. This does not forget conductor data.

A compact maximal-order PIP generator beta and complete compact unit
generators, INCLUDING torsion units, can now be consumed by the local
evaluation lemma. Finite-abelian-group coordinates turn membership in V*E
into ordinary integer lattice membership. The algorithm stops at this
decision: it need not expand a correcting unit or print gamma.

A Boolean-only maximal-order PIP oracle would not suffice for this route:
one needs beta's residue, or a compact generator from which it is computed.
For general ideals, check invertibility and normalize separately rather
than applying the coprime criterion unchecked. A nonzero principal ideal
is invertible; `I*(R:I)=R` tests invertibility by exact lattice operations.
This note does not replace the general normalization theorem with an
assumption that all ideal lattices are already coprime.

With the published compact PIP and unit-group primitives, factoring and
finite-group algorithms, this yields the expected polynomial quantum
DECISION composition on the stated inputs. No full class group is needed
for this route, so no additional GRH assumption is imported from ray-class
group computation. This is established conductor machinery with an explicit
representation interface, not a new quantum algorithm or proved separation.

## Finite Unit Groups Are Constructed, Not Assumed

The required generators of V and their coordinates in G need not be
supplied as advice. Specialize BHJ v3 Proposition 6.11 (PDF p.16) to base
field Q, algebra K, and order R. It constructs generators of (R/f)^* in
randomized polynomial time relative to factoring f in O and finding
primitive elements in finite residue fields. The bound specializes to
at most `5*n*log2 |O/f|` generators. Theorem 8.4, Steps 8--9 (pp.22--23),
explicitly charges their ambient discrete-log coordinates. This is NOT an
unconditional classical polynomial-time algorithm with those tasks erased.

Concretely, decompose the explicit finite ring R/f into local components.
For a component B with nilpotent maximal ideal J and residue field k, use

```
1 -> 1+J -> B^* -> k^* -> 1,
(1+J^j)/(1+J^(j+1)) = (J^j/J^(j+1), +),   j >= 1.
```

Lift a primitive element of k, and lift additive generators of the radical
layers using exact lattice arithmetic. CRT embeds each component generator
with IDENTITY in every other component. This generates the whole unit
group, including nilpotent units, without enumerating the ring or assuming
that uniform ring elements are units with high probability.

The same construction with R=O generates G. Its canonical quotient-ring
encodings and polynomial multiplication/inversion permit quantum finite
abelian group decomposition and generalized discrete logs. Once
`G = direct_sum_i Z/d_i`, put the V-generator and global-unit-image
coordinate columns into M. The final test is

```
coord(beta mod f) in M*Z^t + diag(d_i)*Z^r.
```

HNF/SNF decides it classically. There is no need to decompose V separately.
Quantum factoring and group algorithms cover the stated dependencies;
finite-field polynomial factorization is randomized polynomial-time. No
new GRH assumption enters this finite-ring part. This combines the existing
BHJ reduction with the explicit compact-residue interface, not a new
finite-group algorithm. See also
[Cheung--Mosca](https://arxiv.org/abs/cs/0101004).

## Matching YES And NO Controls

For the earlier output-size family, put s=sqrt(2), f=2^m with m>=2,
theta=f*s, R=Z[theta], J=Z*(2+theta)+Z*(2*theta). Let

```
d=1-f^2/2,       beta=1-theta/2,
I'=(d/(2+theta))*J = Z*d + Z*(theta-f^2).
```

d is odd, I' is integral and coprime to f*O, and I'*O=beta*O. These bases
are polynomial-bit inputs. Writing epsilon^k=a_k+b_k*s for epsilon=1+s,

```
beta*epsilon^k=(a_k-f*b_k)+(b_k-(f/2)*a_k)*s.
```

The scalar coefficient is odd. The other coefficient vanishes mod f
exactly when `k == f/2 (mod f)`, by the independently reviewed Pell
valuation proof in INTEGRAL_SIMILARITY_OUTPUT_SIZE.md. Hence
`beta*epsilon^(f/2)` generates I'. Its residue can be checked with O(m)
bounded-modulus multiplications, without expansion. The correcting unit
MULTIPLIES beta; reversing that convention is masked by f/2=-f/2 mod f
in this special family and must not be generalized.

This family is already classically decidable in polynomial time. Its large
expanded witness is NOT evidence for decision hardness or quantum advantage.
In fact every invertible ideal of these dyadic orders is principal:
`|(O/fO)^*|=2^(2m-1)` and `|(R/fO)^*|=2^(m-1)`, so G/V has order f.
The class of epsilon has exactly that order, since
`epsilon^k mod fO in V iff f divides k`. The unit image therefore fills
G/V. The maximal order Z[sqrt(2)] is norm-Euclidean and has trivial class
group, so the conductor exact sequence gives Pic(R)=1. This is why a
different conductor is essential for a genuine negative decision control.

For a matched NO instance, take R=Z[5*s] and I=2*Z+5*s*Z. It is coprime
to the conductor, and IO=s*O is principal. A generator over R would have
norm +/-2, requiring `a^2-50*b^2=+/-2`, impossible modulo 5. Equivalently,
G=(O/5O)^* has order 24, while the subgroup generated by epsilon and scalar
units has order 12. The residue s is outside it: its norm is 3 mod 5,
whereas this subgroup's norms are squares. Thus maximal-order principality
alone accepts a false positive; the conductor membership test rejects it.
Here I^2=2*R, so I is explicitly invertible, and its ideal class has order
two. The NO result is not an artifact of feeding a noninvertible ideal to
an invertible-ideal criterion.

Bounded exact controls are in `tests/test_compact_residue_conductor.py`.
They cover ramification, rational factors, huge multiplicative valuation
cancellation, signed exponents, and the YES/NO ideals. They are not a
general number-field backend or a quantum implementation. The uniform
cost statement is proved above, not fitted from finite examples.

## Sources And Remaining Limits

- Biasse--Song v2, Theorem1, Definition8 and Algorithm4, pp.3,28--29,
  produce compact factors which need NOT be units modulo a later modulus.
  PIP is Algorithm6 on p.31; ray classes are discussed in Section8.5,p.32.
  Do not justify modular evaluation circularly by citing a ray-class
  construction that itself consumes modular unit images.
  [Corrected full version](https://arxiv.org/pdf/2510.02280v2).
- Eisentrager--Hallgren's earlier ray-class treatment explicitly uses compact
  output in Algorithm5 Step7. Lemma6.1 and Theorem7.1 have dependence on
  2^n; they do not alone prove the arbitrary-degree interface stated here.
  [Author manuscript](https://bpb-us-e1.wpmucdn.com/sites.psu.edu/dist/a/166357/files/2023/06/rcg.pdf).
- The conductor criterion is existing prior art: Kluners--Pauli Theorem5.6
  and Sections6--8; equivalently the commutative case of BHJ Proposition4.3
  and Algorithm8.3 Step10. This is the ordinary, not narrow, class-group
  convention: no infinite-place positivity constraints are imposed.
  [Picard groups of orders](https://math.uni-paderborn.de/fileadmin-eim/mathematik/AG-Computeralgebra/Publications-klueners/picard.pdf),
  [BHJ v3](https://arxiv.org/pdf/2202.03526v3).
- Practical arithmetic libraries already support important factored-form
  operations; PARI's nfmodpr accepts factored elements of nonnegative total
  valuation. That implementation claim is not our uniform complexity proof.
  [Official documentation](https://pari.math.u-bordeaux.fr/dochtml/html-stable/General_number_fields.html#nfmodpr).

The strongest matched classical baseline uses the SAME compact/conductor
reduction with classical number-field and finite-group subroutines, not
expanded-unit enumeration. Once generator residues, the complete unit-image
subgroup and group coordinates are supplied, the remaining test is already
classical polynomial time. A new speedup candidate must identify where
those data come from and which hard native task benefits.

This result does not solve short-generator selection, arbitrary compact
matrix normalization, the Amitsur small-splitting question, noncommutative
division-order principality, or the constrained effective-divisor selection
in INVERSE_TRACE_RAY_CLASS_SCOPE.md. It removes one concrete output-access
obligation and prevents that obligation from being inflated into a general
barrier. Novelty of the elementary local-evaluation argument is not claimed.

New primary-source snapshot: `literature_cache/eisentraeger_hallgren_2010_ray_class.pdf`,
19 pages, 247605 bytes, SHA-256
`508765442bca4a815fbbf5bf65538882041068088b7303a132ebd1495d032445`.
It is the SODA 2010 author manuscript; the hosting URL's date is not its
publication year. Biasse--Song and BHJ snapshot hashes are recorded in the
number-field correction and INTEGRAL_SIMILARITY_OUTPUT_SIZE.md.
