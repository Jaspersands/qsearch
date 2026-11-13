# Residual-ideal support normalization — independent proof, 2026-11-13

**Accepted:** a generic residual divisor can be replaced by one of uniformly
small norm, preserving the relative norm squareclass and every original tag.
The proposed conic-content construction is also valid after explicitly
excluding dyadic and target primes. The generic construction is simpler and
is sufficient for the tagged U-only recurrence.

This removes the stated SUPPORT/HEIGHT feedback in the U-only reduction to a
uniform polynomial expanded relative-conic solver. It neither constructs
that solver nor closes the coupled Kutas/form/U algorithm. No API, network,
Git, new implementation, numerical sweep, or in-flight report was used.
The completed paid report's proposed generic reset was independently proved
below; its labels and any recurrence lower-bound prose are not evidence.

## 1. Uniform reduction of any ideal, with an explicit witness

Let F have degree n, maximal-order integral basis Omega, and discriminant
Delta=|disc F|. All field and basis input bits are charged as in the stable
weighted-LLL review. Let R be any nonzero integral ideal, given by an exact
basis. It need not be principal or squarefree. There is a polynomial-bit
algorithm returning w in R^(-1)\{0} and the integral ideal M=(w)R such that
  N(M) <= K_F,
  K_F = 3^(n/2) 2^(n(n-1)/4) sqrt(Delta).                     (1)
The output w is expanded and its size/runtime are polynomial in the supplied
field/basis and ideal input. The norm bound on M is independent of R.
No class group, unit, regulator, or principal generator is computed.

Proof. Use the ordinary Minkowski norm
  q(z)=sum_(real sigma) |sigma(z)|^2
       +2 sum_(complex pairs sigma) |sigma(z)|^2.
The covolume of R^(-1) is sqrt(Delta)/N(R). The paid rational-Gram LLL
construction returns a nonzero w with
  q(w) <= 3*2^((n-1)/2) Delta^(1/n) N(R)^(-2/n).
AM–GM on the n absolute embedding squares gives
  |N(w)| <= (q(w)/n)^(n/2).
Multiplying by N(R) proves the slightly stronger bound
  N(M) <= (3/n)^(n/2) 2^(n(n-1)/4) sqrt(Delta),
and hence (1). Integrality follows from wR subset O_F. This proves the
claim for every ideal class; M is equivalent to R, not necessarily principal.

Finite arithmetic and precision are explicit. Set m=N(R), an integer with
polynomial input bit length. Since m O_F subset R, the ideal
  B=m R^(-1) subset O_F
is integral and N(B)=m^(n-1). Compute B explicitly by the congruences b*r_i=0 mod m O_F for an integral
basis r_i of R: stacked multiplication matrices, followed by integer Smith/HNF
linear algebra, give precisely B={b in O_F: bR subset m O_F}. Their dimensions
and coefficient bits are polynomial in the input; no integer factoring is
needed for this inverse-ideal step. Apply the prescribed Gram approximation
and exact Gram-only LLL from the stable weighted-LLL proof to B, with weight
alpha=1. Its Gram determinant is Delta*N(B)^2>=1, so the same explicit
lambda_min/entry-error bound applies. If w0 is the returned vector, take
w=w0/m. This scaling does not change the preceding LLL approximation factor.
There is no assumption that the unscaled fractional Gram determinant is >=1.

The recorded transformation vector, all exact operations, and w have
polynomial bits. Moreover m*w is integral; the short-vector archimedean bound
and the earlier trace-dual conversion bound its numerators in terms of the
field/basis data and log m. Compute M=wR and put it in HNF. Since its index
is N(M), the HNF entries are bounded by N(M); the resulting ideal encoding
has field-bounded bit size, independent of the original ideal representation.
An exact integer check can use
  N(M)^2 <= 3^n 2^(n(n-1)/2) Delta.

The lattice reset itself requires only ideal arithmetic, not factoring R.
To list the NEW prime support, factor the single integer N(M) and decompose
its prime factors in F. Its bit length is O(n^2+log Delta). Integer factoring
is charged, and finite-field factoring uses the existing bounded-error native
interface. No primes up to the numerical bound K_F are enumerated.
A fractional R is handled identically by first choosing an integer t with
t R^(-1) integral; the same norm cancellation proves (1).

## 2. Generic residual reset for tagged norm lifting

Let L/F be a genuine quadratic extension. Let S contain all dyadic and
ramified F-primes, and let S_L be its inverse image. Suppose a relative
norm preimage beta in L* has already been constructed, with
  N_(L/F)(beta)=a*s^2,
and it has a prescribed upper target/tag T, a parity divisor outside S_L.
Suppose its mismatch with that target is the pullback of a finite parity
ideal R of F outside S:
  parity_(S_L^c)(beta)+T = pullback(parity_(S^c)(R)).            (2)
Choose the canonical integral squarefree representative R of this parity.
The tagged descent already proves that such a pullback exists; this lemma
also applies to any explicitly supplied instance of (2).

Apply section 1, obtaining w and M=(w)R. Replace beta by
  beta_new=w*beta,
and replace its lower residual target by
  R_new=odd_(S^c)(M).
Outside S the ramification index is one. Hence parity(w beta)+T is exactly
the pullback of parity(w)+parity(R), which is parity(M). Also
  N(beta_new)=a*(s*w)^2.
Thus both the original norm SQUARECLASS and the original upper tag are
unchanged. The new residual has
  N(R_new)<=N(M)<=K_F.                                       (3)
It does not matter whether the old target labels are independent, or whether
some labeled first-space basis pair has squareclass 1 and nonzero tag.
Multiplication by a base-field scalar preserves the norm-tag pair in all cases.
The UPPER squareclass of beta generally changes; this is a replacement norm
preimage with a correspondingly replaced residual, not a squareclass-preserving
normalization of beta itself. The subsequent weighted reset does preserve it.

This is a change of representative for the residual IDEAL CLASS. It is not
an assertion that every residual can be made zero. A nonprincipal obstruction
can remain in R_new, and the second tagged U call still has to solve it.

Once beta_new has this residual, its odd support is contained in old S_L,
the existing upper target supports, and the primes above M. Apply the stable
weighted S-squareclass compression IN L to beta_new, using that explicit
exceptional support. The additional multiplier is a square in L, so it
preserves (2), its reset version, and the norm squareclass. This gives a
small expanded beta representative. It is not a free expansion of a compact
conic witness: the initial beta and subsequent arithmetic are expanded and
charged. The exact conic norm identity may be retained with its square factor;
no assertion that the same exact norm value is preserved is needed.

## 3. The content construction, with its precise local scope

For an expanded conic
  x^2-d*y^2=a*c^2,  c!=0,  a,d!=0,
define fractional ideals
  D=product_P P^floor(v_P(d)/2),
  H=product_P P^floor(v_P(a)/2),
  A=(x)+(y)D+(c)H.
The sum is an IDEAL SUM, so valuations take the minimum. Zero x or y is
allowed, with valuation infinity. Assume P is nondyadic and both v_P(a)
and v_P(d) are even. Write
  k=v_P(d)/2, l=v_P(a)/2,
  u=v_P(x), v=v_P(y)+k, z=v_P(c)+l.
The conic identity gives z>=min(u,v), with equality if u!=v. Consequently
  v_P(A)=min(u,v).                                         (4)
All these are integer valuations; negative input valuations cause no change.

The quadratic algebra at such a P is unramified or split. In the inert case,
a normalized square root of d has nonsquare residue, so cancellation between
x and y*sqrt(d) cannot raise their common minimum. Thus the beta valuation
at its unique prime equals (4). In the split case, because 2 is a unit,
  min(v_P(x+y*sqrt(d)),v_P(x-y*sqrt(d)))=min(u,v).
Their sum is 2z, so their parities are equal and each equals min(u,v) mod 2.
This proves that the common outside-exceptional parity J_beta is v_P(A) mod 2.

Apply section 1 to the fractional ideal A. It returns gamma with
C=(gamma)A integral and N(C)<=K_F. For beta'=gamma(x+y*sqrt(d)), the common
parity at every such P is v_P(C) mod 2. Therefore every NEW odd residual
prime outside the exceptional set lies in supp(C), with the same field-only
norm bound (1). A can be computed from ideal products and sums without
factoring the principal ideals of x, y or c; D and H use the coefficients'
ideal valuations. Thus this version can also avoid first factoring the
entire conic witness merely to discover its residual support.

The dyadic exclusion is ESSENTIAL, even for a split unramified prime. For
F=Q, d=17, a=-1 and (x,y,c)=(1,1,4), the point satisfies the conic and A=Z.
In Q_2(sqrt(17))=Q_2 x Q_2, the two values 1+sqrt(17) and 1-sqrt(17) have
valuations 1 and 3 (their sum is 2 and their product is -16). Both parities
are odd although v_2(A)=0. Thus a formulation allowing 2 outside S is false.
The intended tower setup already includes all dyadic primes in S.

For generalized tagged inputs, a may have odd valuations at existing target
primes. Add to the exceptional set every BASE PRIME BELOW an upper target
support, not merely the support of its norm PARITY: inert targets and equal
split parities can disappear on taking that parity norm. Outside this set,
(4) and the parity proof apply. At its existing target primes, compute the
mismatch by native local/ideal arithmetic; it may be nonzero but creates no
new prime. Norm-tag compatibility still makes the mismatch a pullback outside
S. Thus the residual's support is contained in existing target primes plus
supp(C). The generic reset in section 2 handles all these primes at once
without needing this extra local case distinction.

## 4. Conditional polynomial U-only basis reduction: the new consequence

Use the previously checked tagged operation U_K(S;J_1,...,J_r), returning
complete pairs ([a],tag). Its two recursive calls are to the immediate lower
field: first on norm-pushed targets, then on residual targets from a norm-
compatible first-space basis. Apply the generic reset to EACH residual
BEFORE the second call, and the weighted squareclass reset to every basis
representative and relevant returned product. Grant, as an explicit external
interface for this paragraph only, a UNIFORM polynomial-bit relative conic
solver producing expanded witnesses on every promised-soluble call.

Let n_j=[F_j:Q] and Delta_j=|disc F_j|. Choose computable integers
  b_j = n_j^2+2*n_j+ceil(log_2 Delta_j),
so log_2 K_(F_j)<=b_j. The following bounds are in ORIGINAL input data.

1. First-child relative norm, followed by parity reduction, cannot increase
   an ideal's absolute norm. Every second-child target now has log norm <=b_j
   by (3). Hence every individual target in the whole U tree has log norm
   at most the maximum of the original target log norms and the b_j.
2. Let a_j=dim F_j(S_j,2). Along a branch the target COUNT increases by at
   most a_j. A polynomial bound needs no computed class group or unread
   class-number estimate: section 1 shows every ideal class has a representative
   of norm <=2^b_j. HNF matrices of index at most that value have entries at
   most 2^b_j, so
     log_2 h_(F_j) <= (b_j+1)*n_j*(n_j+1)/2.
   The units/ideal-class exact sequence gives
     a_j <= n_j+|S_j|+log_2 h_(F_j).
   This is a proof-only dimension bound; no units or ideal classes are enumerated.
   Thus r<=r_initial+sum_j a_j is polynomial in the original native data.
3. Combining the preceding two bounds, the TOTAL target norm bit-mass and
   all target ideal encodings at every node are polynomially bounded. If
   S_j consists of primes over a fixed rational S_Q, then |S_j|<=n_j|S_Q|
   and its radical norm bit-mass is <=n_j sum_(p in S_Q)log_2 p.
4. Weighted compression bounds a class representative in U by that S/target
   bit-mass plus its field/basis data, regardless of ancestry. Products of a
   polynomial number of these representatives have polynomial bits; compress
   them again. Conic inputs are therefore polynomially bounded in the original
   data. A generic UNIFORM polynomial conic output bound is sufficient now:
   normalize its residual, then its squareclass, before passing it onward.
   An affine conic height bound is not necessary for this conditional reduction.
5. There are at most 2N-1 U nodes for a tower of degree N=2^h. Each node has
   polynomially many conic requests and polynomial auxiliary arithmetic.
   Norm compatibility, labels, the kernel ([d],0), and the coordinate maps
   are those of the exact tagged construction; these representative changes
   preserve their classes and tags. They introduce no new U calls.

Consequently the U-only BASIS construction is a polynomial reduction to the
stated uniform expanded conic interface, including its support and coefficient
bit clock. The exact tagged coordinate maps survive algebraically; a uniform
BIT ledger for arbitrary expanded membership/coordinate QUERIES is a separate
composition check, not silently inferred from the basis-size bound here.
Uniform bounded-error subroutines in this basis construction can be assigned
the overall error budget using its polynomial call bound. A failed finite
clock is ABORT. This is stronger than saying each level is polynomial.

It does NOT close the actual implementation of the conic interface: inserting
Kutas descent and general-field four-variable isotropy reintroduces complete
U presentations for multiple forms. Their coupled branching/batching and
auxiliary-prime selection still need a separate polynomial clock. No algorithm
lower bound is inferred from any crude recurrence for that implementation.

## 5. Scope and retained evidence

The generic small residual-ideal reset and the repaired conic-content lemma
are proved. Their dependence on the expanded incoming witness is runtime,
not the new-support norm bound. No principalization, unit computation,
compact-input expansion, conic discovery or full tower admission follows.

Finite-bit details reuse the fully checked proof
`2026-11-13-squareclass-weighted-lll-compression.md`, especially its exact
Gram adaptation and prescribed precision, and the actual LLL page renders
in `audits/sources/2026-11-13-tower-recurrence/` (PDF pages3,7,8,9).
The local content argument and the U-only norm/count/height recurrence above
are independent derivations. Only this scoped review was written.
