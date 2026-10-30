# A Small-Multiplier Bound For The Actual Additive Source

2026-10-26. Written deduction with exact supplied-order controls. This new
extension has NOT been independently reviewed. No native curve algorithm,
PPAV construction, symmetry enumeration or quantum experiment was run.

## Decision And Scope

The dimension16 additive polarization, not just the earlier binary proxy,
has an explicit product isogeny with multiplier n^2. Every automorphism of
any stabilization therefore yields integral endomorphisms of the ORIGINAL
E of degree at most n^4, independent of the size of its query beta.

If beta is nonscalar and alpha is any native nonscalar element of Q(beta),
then

    p > |disc Z[alpha]| * n^4

forces the ENTIRE automorphism group into M(Q(beta)). After the previously
specified native query-quadratic gate has saturated O intersect Q(beta)
inside the known order R, no such automorphism can grow R. This is a
source-wide no-growth region, not a failed finite search.

There is also a complete classical enumeration in time polynomial in the
VALUE n at fixed dimension, with a very large exponent and all native
evaluation/field costs charged. Neither statement gives a polynomial-in-
log(n) algorithm. The hard native family uses n=d=q^3, for which n^4=q^12;
this bound need not eliminate its residual regime. No hitting theorem or
new transverse-symmetry construction was found.

CRITICAL: the small-multiplier pullback does NOT generally preserve
outside-R membership. An exact Pell example below erases all integral-
coset growth. This prevents a false claim of complete dequantization from
the short-map witness alone. The additive HSP theorem itself is not
falsified by these observations.

## 1. Native Input And The Reordering

Let E be supersingular in characteristic p>3 and O=End(E) over an algebraic
closure. Its native curve and evaluators for a known full order R subset O
are input; a basis for O is NOT. Choose an integral query beta in R and
n>=2. The additive application takes n=[O:R]. Let T be the scalar
four-square matrix with T*T^t=T^t*T=(n^4-1)I4. The existing source is

    L = [[n^2, n*beta], [n*beta^dagger, n^2+Norm(beta)]],
    J = adj(L),
    Z = [[I4 tensor L, T tensor I2],
         [T^t tensor I2, I4 tensor J]].

Separate the eight low diagonal coordinates from the eight high ones:

    low  = (0,2,4,6,9,11,13,15),
    high = (1,3,5,7,8,10,12,14).

In these reordered coordinates write

    a=n^2, b=n^2+Norm(beta),
    B = [[n*beta*I4, T], [T^t, -n*beta^dagger*I4]],
    H = [[a*I8, B], [B^dagger, b*I8]].

Scalar T commutes with beta. The off-diagonal products cancel, giving

    B*B^dagger = B^dagger*B = (a*b-1)I8,
    H^-1 = [[b*I8,-B],[-B^dagger,a*I8]].

The Schur complement is (1/a)I8, so H is positive definite as well as
integral and unimodular. This does not require a free factor decomposition.

## 2. A Native Matrix Isogeny With Multiplier n^2

Define integral matrices using only the native query, its dual and scalars:

    C    = [[I8,-B],[0,a*I8]],
    Cbar = [[a*I8,B],[0,I8]].

Direct multiplication proves

    C*Cbar = Cbar*C = a*I16,
    H*C = [[a*I8,0],[B^dagger,I8]],
    C^dagger*H*C = a*I16.

Thus C maps the standard polarized product to (E^16,H) with polarization
multiplier a. Its geometric degree is a^16, not a; multiplier and degree
are different. For g=16s, use block-diagonal s-fold copies of H,C,Cbar.
The multiplier stays a, while the isogeny degree becomes a^g.

The formula does NOT construct a theta model for the nonproduct target
polarization. The kernel is a-primary and may involve a huge input prime.
Using it in a generic quotient routine would cost polynomial in the VALUE
n, not automatically its bit length. It cannot silently replace the old
smooth, coprime converter in a claimed poly(log n) source algorithm.

## 3. All Automorphisms Give Bounded-Degree Maps

For ANY integral automorphism W with W^dagger*H*W=H, put

    U = Cbar*W*C = a*C^-1*W*C.

No condition on the block support of W is imposed; it may mix stabilized
copies. Since (C^-1)^dagger*C^-1=H/a,

    U^dagger*U = a^2*I_g.

Every U_ij is an actual integral endomorphism of E and

    sum_i deg(U_ij)=a^2,  hence  deg(U_ij)<=a^2=n^4.

The reverse rational formula is

    W = C*U*Cbar/a^2.

If beta is nonscalar, K=Q(beta) is imaginary quadratic and C,Cbar are
invertible over K. Therefore

    W in M_g(K)  iff  U in M_g(K).

So every symmetry transverse to K supplies at least one noncommuting
native endomorphism of degree <=n^4. This is a witness implication, not a
promise that the witness is outside R, and not a method to find W.

### Extraction From An Actual Represented Output

The old source's smooth converter has native q:E^g->Y, matrices C0,F0 in
M_g(R), and a smooth scalar Q with C0*F0=F0*C0=Q*I. For a returned actual
polarized automorphism b of Y, let L0=q^dagger*b*q. Its proof-only
comparison coordinates W satisfy

    F0*L0*C0 = Q^2*W.

Recover the entries of W by genuine native isogeny division by Q^2,
or compose with Cbar and C first and divide the resulting numerator.
The guaranteed integral quotient is essential. Native zero maps are
treated separately. Charge degree bounds, evaluator size, fields and
compression before reuse. The unknown comparison isomorphism is not used
as an oracle. Efficient division is an imported interface from
[Herledan Le Merdy--Wesolowski, Section 4](https://arxiv.org/html/2309.11912v4#S4).
The present Python code only verifies supplied matrices and does not
implement any of these native operations.

## 4. A Characteristic-Discriminant No-Growth Region

Let alpha be ANY known native nonscalar element of K, not necessarily the
possibly enormous beta. Set Delta=Tr(alpha)^2-4*Norm(alpha)<0. For integral
x in O, put Delta_x=Tr(x)^2-4*Norm(x) and
t=2*Tr(alpha*x)-Tr(alpha)*Tr(x). Then

    Norm([alpha,x]) = (Delta*Delta_x-t^2)/4
                   <= |Delta|*Norm(x).

The identity and divisibility of the commutator norm by p are standard;
see [Colo--Kohel, Lemma 12, arXiv version](https://arxiv.org/pdf/2012.10803),
published as Lemma 3.6. The divisibility follows because the maximal
order modulo its ramified ideal has commutative residue field F_(p^2).
Positive definiteness gives Norm([alpha,x])>=p whenever the commutator
is nonzero. Consequently p>|Delta|*n^4 forces every extracted U_ij to
commute with alpha, hence with beta, and forces every W into M_g(K).

This holds for EVERY s, regardless of g=16s. No union bound over matrices
or probabilistic symmetry sampler is needed. If the native quadratic gate
has established O intersect K subset R, then every such W lies in M_g(R).
Thus the complete unmarked automorphism group yields no new order element.

Use a generator of the saturated quadratic order for alpha where possible;
its discriminant may be much smaller than that of Z[beta]. A large scalar
shift or integer multiple of beta cannot evade the bound by inflating its
query norm. For the supplied p=103, K=Q(i), n=2 control, Delta=-4 and
4*n^4=64<103 even when beta has 40-digit coefficients. These are easy
orientations, not evidence of a hard input. Existing discriminant-dependent
EndRing algorithms must still be compared.

The strict inequality matters. At p=7, alpha=(1+j)/2, x=i in the order
for (-1,-7), Delta=-7, Norm(x)=1 and Norm([alpha,x])=7. Equality permits
noncommutation. If the source inequality fails, conclude NOTHING about
existence, density, native cost or usefulness of transverse symmetries.
Scalar beta is excluded from this particular field-gate corollary.

## 5. A Complete Value-Polynomial Classical Comparator

On the SAME E, enumerate the finite set S of all endomorphisms of degree
at most B0=n^4, including zero. This needs no supplied maximal order.
One exhaustive native route enumerates finite subgroup schemes of all
degrees m<=B0, computes quotient curves, and tests all isomorphisms of
each quotient back to E. For m prime to p, full m-torsion, its finite
subgroups and the necessary fields have polynomial size in the VALUE m.
Treat degrees and fields separately instead of taking a giant common
torsion compositum. If p<=B0, include the bounded Frobenius powers and
separable factors. The value budget pays for these too. All map and
isomorphism computations, not just group-operation counts, are charged.

For fixed g, enumerate matrices U in S^(g*g), test U^dagger*U=a^2*I and
test actual native integrality of every entry of C*U*Cbar/a^2. Each passing
matrix gives an H-automorphism, and Section 3 proves completeness. Native
trace coordinates test whether W lies in M_g(R). This retains useful W
even when the intermediate U lies wholly inside R.

There are polynomially many bounded-norm points in a fixed-rank positive
quaternion lattice: nonzero integral differences have norm at least one,
so elementary four-dimensional packing bounds their count by O(B0^2).
The matrix search therefore has a value-polynomial bound of the form
n^O(g^2), multiplied by polynomial paid native input/evaluator costs.
It is NOT claimed practical, poly(log n), or uniformly polynomial in g.
No complete native enumerator is implemented in this bundle.

## 6. Adversarial Control: Pullback Can Erase ALL Order Growth

The tempting inference "U is in R, so W is in R" is invalid. Recovery
divides by a^2=n^4, which shares the hidden index in the native application.
For a full-order index d and beta in R, the inference WOULD hold if
gcd(n,d)=1: then d*W and a^2*W in M_g(R) imply W in M_g(R) by Bezout.
This is why the old coprime smooth converter has a different guarantee.

Here is an entire-group counterexample when n=d. Let n^2-2*k^2=1 and use
four-square roots (2*k^2,2*k,0,0). The prior exact factorization gives
Z_0=P^dagger*P with scalar integral unimodular P. If R contains all units
of O, every automorphism W0 of Z0 is in M_g(R): after conjugation by P it
is a monomial matrix with entries in O^*. Now take delta in O and
beta=n*delta in R (d*O subset R). The source shear gives

    Z_beta=S_delta^dagger*Z_0*S_delta,
    W_beta=S_delta^-1*W0*S_delta.

In low/high coordinates S_delta=[[I,D],[0,I]], with
D=diag(delta*I4,-delta^dagger*I4), and B_beta=B_0+a*D. Thus

    S_delta*C_beta=C_0,
    Cbar_beta*W_beta*C_beta=Cbar_0*W0*C_0.

The right side is independent of delta and in M_g(R) for EVERY W0. Yet
for odd d the previous signed-permutation argument shows that delta not
in R forces some W_beta outside M_g(R). The full integral-coset signal
has disappeared in the short pullback. It was classical division evidence
already, not an unexplained quantum effect.

The exact control uses p=11, n=d=17, k=12 and

    O basis: (1,i,(1+j)/2,(i+i*j)/2),
    R columns: [[1,0,0,0],[0,1,0,0],[0,0,17,4],[0,0,0,1]],
    delta=(1+j)/2.

R contains all units +/-1,+/-i, but not delta. All sixteen generators of
the product automorphism group are checked, along with the exact shear
identity that proves the entire-group statement. Several nonzero delta
classes give useful W, while every pulled U remains in R. Some U entries
are transverse to Q(delta) but already known in R; noncommutation by
itself is not order growth.

## 7. Attempts To Break The Conclusion

1. Nonfree factors: the proof uses invertible C and all automorphisms, not
   a free rank-one factor basis. The previous factor issue is irrelevant.
2. Copy mixing: the identity holds for arbitrary W on H^s, not merely a
   repeated 16-dimensional automorphism. The test includes copy swaps.
3. Rational unitaries: integrality is necessary; an explicit rational
   H-unitary is rejected even though it passes the norm identity.
4. Enormous beta: its size enters the native evaluator budget but does
   not enter the corner degree bound. Exact large-coefficient tests pass.
5. Outside field versus outside order: the entire-group erasure control
   refutes the stronger claim; only the correctly qualified bound remains.
6. Native input: a plausible characteristic and arithmetic discriminant
   do not authenticate E, alpha or the supplied order. Reports retain
   native execution/authentication flags as false.
7. Large n: no value-polynomial enumerator gives a bit-polynomial result.
   The theorem does not close the hard large-prime residual case.
8. Novelty and impact: completing the square and the commutator inequality
   are not new tools. The contribution here is applying them correctly to
   THIS source and preventing a false positive, not claiming a new solver.

## 8. Research Decision

Freeze further adjacent harvest controls unless a concrete transverse
mechanism survives both the quadratic gate and these bounds. Do not build
the dimension128 geometry backend merely to rediscover small-degree maps.
Do not infer a quantum separation from the remaining gap.

The independent direction comparison also found no ready replacement:
the Rees source still lacks a natural useful native problem; the decoded-
output DQI branch lacks a useful observable escaping its implemented
classical simulations; and the inverse-trace modular-norm branch lacks
public acquisition of its supplied carry data. Record those precise input
gaps, not an undifferentiated list of algorithm families. A subsequent
constructive pass must attack one such gap or produce a concrete new
source, rather than append another neighboring finite-control bundle.
