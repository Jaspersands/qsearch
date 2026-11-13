# Tagged quadratic towers: conditional expanded-bit composition

2026-11-13. Independent composition of tagged descent, residual-ideal reset,
and weighted squareclass reset. No API, network, Git, compact expansion, or
new finite experiment. The completed Claude report was read in full; its
coordinate-size assertion is proved below rather than imported.

**Result.** For an explicit quadratic tower of degree N, the complete tagged
squareclass presentation, including stored coordinate routines, has a
polynomial reduction to integer factoring and a UNIFORM polynomial-bit
relative-conic primitive returning EXPANDED witnesses. Initial nonzero
targets and their total bit size are charged. This is not an implementation
of that conic primitive, nor an unconditional polynomial tower algorithm.

## 1. Input and the precise conditional primitive

The input is Q=F_0 subset ... subset F_h, with
  F_i=F_(i-1)(theta_i), theta_i^2=d_i,  [F_i:Q]=2^i, N=2^h.
Every step is a genuine quadratic field extension. Explicit maximal-order
integral bases, multiplication tables, embeddings between successive fields,
and expanded d_i, theta_i are supplied and charged. Let B bound the total
bit length of this data. Exact rational linear algebra computes the fixed
relative-coordinate and conjugation maps with polynomial bits.

S_Q is an explicit finite prime list containing 2 and every rational prime
ramified in the tower; S_i contains all primes above it. Real norm conditions
are tested separately. The initial J_1,...,J_(r0) are integral squarefree
ideals of F_h outside S_h, given as factored parity divisors. Zero parity
divisors (the unit ideal) and repeated targets are allowed. Their count AND
encoding size are inputs.
Put
  G_K(S;J) = {([x],c): parity_(outside S)(x)=sum c_j J_j},
with [x] in K*/K*2 and c in F2^r. The requested output is a basis of PAIRS,
expanded representatives, and coordinates of any valid expanded query
(x,c). The ordinary squareclass problem has r0=0.

The extra primitive, Conic, receives the supplied tower data for L/F and
expanded a in F*, promised to be a norm squareclass. It returns expanded
beta in L*, t in F* with N(beta)=a*t^2. Its running time and output bit size
are bounded by one fixed polynomial in the ENTIRE encoded request and the
requested failure bits, uniformly in the degree and level. The exact identity
is verified. A homogeneous conic point also suffices: its z is nonzero since
d is nonsquare, and the charged rational division gives beta=(x+y*theta)/z.
An unspecified compact point or a per-level polynomial with growing exponent
does not satisfy this interface. Integer factoring of polynomial-bit
intermediates is separately charged.

## 2. Exact tagged descent, including its one-dimensional kernel

For L=F(sqrt d), norm a target parity divisor down to F. At an unramified
inert prime its norm parity is zero; at a split prime it is the sum of its
two parities. First construct G_F(S;NJ). Intersect its coefficient space
with all local norm conditions to obtain a basis of PAIRS
  (a_k,c_k), k=1,...,s.
Outside S the local conditions are automatic: at inert primes the norm
parity of every target is zero, so v(a_k) is even; split primes impose no
condition. The quadratic Hasse norm theorem makes these conditions sufficient.

Choose beta_k with norm class a_k. The outside-S mismatch
  parity(beta_k)+sum_j (c_k)_j J_j
is the pullback of a UNIQUE base parity divisor R_k. At split primes the
two mismatch parities agree, by the norm identity; at inert primes the one
parity is unrestricted. Pullback is injective because all these ramification
indices are one. Negative valuations are reduced modulo 2 in exactly the
same way. To find all support, clear an integral-basis denominator c of beta
and factor c*abs(N_(L/Q)(c*beta)); both numerator and denominator primes are
there. Add the prescribed target supports before computing the mismatch.

For any such lifts and corresponding residuals the map
  Phi:G_F(S;R_1,...,R_s) --> G_L(S;J),
  (gamma,u) |--> (gamma*product beta_k^u_k, sum u_k c_k)          (1)
is onto, and its kernel is exactly <([d],0)>.
Indeed a kernel element has square norm and zero final tag, so independence
of the FIRST PAIR basis forces u=0. An element of F becomes square in L
precisely in the two classes 1,d. Moreover [d] belongs to F(S,2), since the
extension is unramified outside S and those primes are nondyadic.

For surjectivity take (x,c) upstairs, express (Nx,c) in the first pair basis,
and put x'=x*product beta_k^u_k. Then Nx'=sigma^2 in F. If x' is in F use
gamma=x'; otherwise use a nonzero gamma=Tr(x')+/-2sigma and
  (x'+/-sigma)^2=x'*gamma.                                  (2)
Its class is [x'] in L and its parity upstairs is the pullback of sum u_kR_k.
Injectivity of parity pullback gives (gamma,u) in the second group. Equation
(1) returns (x,c), since the extra beta product is squared.
This proof retains pairs (1,c!=0). Replacing a pair basis by a basis of its
element projection would make the kernel and completeness claim false.

## 3. The two resets, with their different meanings

The stable 243-line review
`2026-11-13-conic-content-support-normalization.md`, sections 1--2, proves:
for every integral ideal R of a degree-n field K, an expanded w in R^-1 can
be found by prescribed-precision rational-Gram LLL, with
  M=(w)R integral,
  N(M)<=3^(n/2)*2^(n(n-1)/4)*sqrt(abs(disc K)).                 (3)
The computation of w has polynomial cost in the incoming ideal/field input;
the bound on M is independent of that ideal. It explicitly computes the
integral lattice N(R)*R^-1 by congruence HNF, so no fractional Gram determinant
lower bound is assumed. Factoring N(M) lists its small new support.

Apply this to R_k, replace beta_k by w_k*beta_k, and replace R_k by the odd
outside-S part of M_k. Both the first norm CLASS and its original tag stay
unchanged; equation (1) is now used with these NEW lifts and NEW residuals.
The upper squareclass of beta_k generally changes. Calling this a
squareclass-preserving reset would be an error. It does not kill the ideal
class obstruction; the second tagged call still solves that obstruction.

The stable 270-line review
`2026-11-13-squareclass-weighted-lll-compression.md` proves the second reset.
For any expanded z in K*, factor (z), let J be its integral odd-valuation
part, and compute gamma such that z'=z*gamma^2 is integral and
  max_sigma |sigma(z')|
    <=3*2^((n-1)/2)*(abs(disc K)*N(J))^(1/n).                  (4)
Its cost and the exact certificate gamma charge the incoming expanded z;
its OUTPUT bound depends only on the field and the odd support. The review
pays the rational-Gram precision, exact LLL clock and trace-dual coordinate
conversion. Extra even valuations outside the specified support are allowed.

Use (4) on the first norm-compatible products a_k, on every beta_k AFTER
(3), and on every final image in (1). Norm classes, parity targets and tags
are unchanged by this second reset. All stored beta_k and basis elements
can therefore be integral. Retain the finite exact square multipliers and
norm identities if certificates are desired; there is no ancestry expansion.

## 4. Explicit global bounds; arbitrary initial targets are included

Let n_i=2^i, Delta_i=abs(disc F_i), and take the following computable
integer upper bounds (all logarithms in this section are base 2):
  b_i=n_i^2+2n_i+ceil(log Delta_i),       b=max_i b_i,
  T=max(1,b,max_j ceil(log N(J_j))),
  A=max_i { n_i+|S_i|+(b_i+1)*n_i*(n_i+1)/2 },
  r_*=r0+h*A,                           G=A+r_*,
  S_*=N*sum_(p in S_Q) ceil(log p),      D_*=max_i ceil(log Delta_i).
The maximum over an empty initial target list is zero.

Here is an elementary proof of the dimension bound A. By (3), EVERY ideal
class has an integral representative of norm at most 2^b_i. An HNF matrix
of index at most that number has at most n_i(n_i+1)/2 nonzero triangular
entries, each of absolute value at most 2^b_i. Thus
  log |Cl(F_i)| <= (b_i+1)*n_i*(n_i+1)/2.
The units/ideal-class exact sequence gives
  dim F_i(S_i,2) <= n_i+|S_i|+log |Cl(F_i)|.
This is a proof-only count, using no computed class group, regulator bound,
unit basis, or enumeration of ideals. It avoids the report's unread Friedman
citation. Also |S_i|<=n_i|S_Q|.

Projection to tags has kernel F_i(S_i,2), so dim G_i<=A+r. The first child
keeps r targets and cannot increase their individual norms: ideal norm
preserves absolute norm, and parity reduction only removes prime powers.
The second child has s<=A+r targets, each of log norm at most b. Therefore
every node has r<=r_* and individual target log norm at most T. Its total
target norm bit-mass is at most r_*T, including when r0 is nonzero.

The odd support mass of any output representative is at most S_*+r_*T.
For a stored beta after the residual reset it is at most
  S_*+r_*T+2b:
pullback of a lower ideal has absolute norm equal to its norm squared.
Consequently all reset representatives have log maximum embedding at most
  Z_arch=4+N+D_*+S_*+r_*T+2b.                               (5)

For completeness, no ill-conditioned supplied basis is hidden here. Set
  M=N*2^B,  C_Omega=ceil(2N log(max(2,N))+(2N-1)log M)+3.
Multiplication-matrix eigenvalue bounds give |sigma(omega_j)|<=M. The trace
matrix inverse/cofactor bound from the weighted-LLL review gives integer
coordinates of an integral y of maximum absolute value at most
  2^C_Omega * max(1,max_sigma |sigma(y)|).
Thus Z=Z_arch+C_Omega bounds every stored reset coordinate bit length, up
to a harmless final sign bit. All of T,A,r_*,G,Z are polynomial in ORIGINAL
input length and N. The supplied field tables charge skew bases explicitly.

At a node at most G small child representatives are multiplied to form an
a_k, then reset. A conic request has at most B+O(NZ) bits. Its polynomial
expanded output may be larger than Z, but its support extraction, (3), and
(4) have cost polynomial in that output, and return the SAME global bound
(5) before any recursive use. Hence the conic polynomial is not composed
with itself once per tower level. Incoming reset certificates also have
polynomial bits and are charged, rather than being declared free.

## 5. Stored coordinate routines and the missing height argument

At Q use the independent pair basis
  (-1,0), (p,0) for p in S_Q, (n_j,e_j) for every target J_j,
where n_j is the product of its primes, including n_j=1. For a valid query
divide x by product n_j^c_j; its sign and known-S valuation parities give
the remaining coordinates. Rational integer-square tests can check the
residual if membership verification is wanted. No unknown-prime search is
needed at this base step.

At L retain both lower presentations, the matrix of the first norm-compatible
pair basis in the first presentation, the reset beta_k, and the residuals.
Compute once, using the second child's stored routine,
  e_d=Coord_second(d,0).
Choose j0 with (e_d)_j0=1 and omit that second-basis image from (1). The
remaining images, reset by (4), are the output basis. To coordinate (x,c):

1. Coordinate (Nx,c) in the FIRST child and solve for its first-pair basis
   coefficients u by stored binary linear algebra.
2. Form x'=x*product beta_k^u_k, find sigma^2=Nx', and choose gamma by (2).
3. Coordinate (gamma,u) in the SECOND child, obtaining e.
4. Replace e by e+e_d if its j0 coordinate is 1; delete that coordinate.
The returned vector is relative to the actual output basis, because all
subsequent resets multiply representatives by squares. This stores complete
coordinates, not a membership oracle or a character-separation assumption.

Here is the finite-height proof. For x in an integral-basis field let m(x)
be its least positive rational-integer denominator and define
  L(x)=log m(x)+log max(1,max_sigma |sigma(x)|).
This quantity and ordinary expanded coordinate bit height differ by at
most the fixed field/basis bounds above; importantly, no factor n is needed.
Explicitly coordinate height <=L(x)+C_Omega, and L(x)<=coordinate height
+log(NM). Products satisfy L(xy)<=L(x)+L(y), and
  L(N_(L/F)x)<=2L(x).                                       (6)
The latter follows because m(x)^2*Nx is integral and every norm embedding
is the product of TWO embeddings, not all n of them.

All stored beta_k are integral and have embedding log bound Z_arch. Hence
x' has the SAME permissible denominator m=m(x), and maximum embedding
bounded by max(1,max|sigma(x)|)*2^(G*Z_arch). If sigma^2=Nx', then
  (m*sigma)^2=N(m*x') is integral in O_F.
Integral closedness implies m*sigma is integral. Also every embedding of
sigma is bounded by the maximum embedding of x'. Both Tr(x') and 2sigma
therefore have the COMMON denominator m; their sum need not multiply two
independently recovered denominators. It follows that
  L(gamma)<=L(x)+G*Z_arch+2.                                (7)
The special case x' in F has the same bound.

Thus every coordinate-child query satisfies
  L_child<=2L_parent+P,  P=G*Z_arch+2,
and every query in depth h has L<=N*(L_initial+P). Exact rational reduction
and the trace-dual coordinate bound pay the actual input/output bits. A
Weil-height-to-coordinate estimate multiplying by the field degree at every
edge is neither used nor necessary. Intermediate matrix inversions may cost
a degree factor in WORKSPACE, but their reduced algebraic outputs obey
(6)--(7), so that factor is not fed back down the recursive path.

## 6. Exact square roots without an extra global arithmetic oracle

The square root in step 2 can be computed by an elementary recursive routine
on the SUPPLIED tower. This also works as a square test. The rational base
uses numerator/denominator integer-square tests. At a quadratic step write
z=A+B*theta, theta^2=d. Handle z=0 separately.

* If B=0, test roots of z and z/d in the lower field. A root is respectively
  the lower root or theta times the lower root. These are exhaustive, since
  a root u+v*theta has 2uv=0.
* If B!=0, first find a lower root t of A^2-dB^2. If none exists, reject.
  Test the two lower elements (A+t)/2 and (A-t)/2 for a square root u.
  For each successful nonzero u put v=B/(2u) and verify exactly
  (u+v*theta)^2=z. If neither succeeds, reject.
Completeness follows from t=+/- (u^2-dv^2) for any actual root. When B!=0
neither candidate u^2 is zero. Any chosen sign of the first root t is fine.

There are at most THREE lower calls, so at height i there are O(3^i)<=O(N^2)
calls, not a search over 2^[F_i:Q] embedding signs. For the size proof, the
fixed relative-coordinate maps add only a field-data polynomial. The norm
argument doubles L. If its root t exists, m*t is integral and its embedding
size is at most that of z, exactly as above. The subsequent candidate sums
therefore have denominator dividing 4m and size L(z)+O(1). The B=0 quotient
z/d adds only the fixed size of 1/d. Consequently every recursive argument
has L at most N*(L(z)+P_field) for a fixed computable field-data polynomial.
Every successful returned root r also satisfies m(z)*r integral and
max|sigma(r)|=sqrt(max|sigma(z)|), so L(r)<=L(z).

Exact divisions and inverse matrices have polynomial bit cost in those
bounds. They do not cause a recursive degree-factor height loss; the actual
returned roots obey the integrality bound just proved. This establishes
both existence and a finite bit clock for the coordinate step, without
importing a new number-field polynomial-factorization or conic oracle.

## 7. Local conditions, finite arithmetic and total clock

The non-conic local work is polynomial in the same charged data. At odd
primes the quadratic norm character is the usual valuation/residue formula,
computed by finite-field exponentiation. At dyadic primes use the already
checked finite-ring construction in
`2026-11-13-native-local-squareclass-backend.md`, sections 3--8: a uniformizer
and residue lifts give the generators 1+pi^j beta_l for j<2e+1, with at most
2[K:Q_2] displayed principal-unit generators. Triangular square relations
give squareclass coordinates by binary elimination, not unit enumeration.

For a nonsplit local quadratic L_P/F_p, take norms of the uniformizer and
these local squareclass generators and express them in the F_p coordinates.
Their span is EXACTLY the norm subgroup modulo F_p*2; squares already are
norms from the base field. Its annihilator supplies all required linear
norm conditions. A split completion supplies none. The supplied global
maximal orders and prime decomposition give the actual local rings; their
finite quotient computations and the existing refinement guards have
polynomial precision. Query valuations are bounded using the expanded
numerator/denominator norms. Norms of local generator lifts can be evaluated
by the exact relative multiplication matrices. Real signs are obtained by
certified real-root isolation. Thus no further norm-membership oracle is
hidden in the intersection defining H.

Ideal operations use the supplied maximal orders and integer HNF. Prime
support extraction factors numerator/denominator norms of polynomial-bit
expanded elements; finite-field factorization and native prime decomposition
are charged with bounded error. No complete class group or units are used.

Construction has exactly two lower U calls per internal node: at most
2N-1 U nodes and (N-1)G conic calls. Each node has polynomially many
factorizations and field/ideal operations on the GLOBAL bounds of section 4.
There is one kernel-coordinate query per internal node. Counting the two
coordinate children gives O(Nh) coordinate-node visits across construction;
each uses polynomial work, including the explicit square-root routine.
For one external query of expanded bit length ell there are at most 2N-1
coordinate nodes, on data of size polynomial in N,B,r0,T,ell. In particular
the basis algorithm's kernel queries do not invoke new U constructions.

Let Q be the resulting explicit polynomial bound on randomized subroutine
calls. Assign each failure probability at most eta/(2Q). The conic interface
and integer/finite-field factoring interfaces are charged at those failure
bits. Use their finite clocks and report ABORT on timeout or a failed exact
certificate; restart/amplify expected polynomial finite-field routines in
bounded blocks if needed. Deterministic LLL precision is not a randomness
source. The aggregate error is at most eta by the union bound, and the
clock is polynomial in original input size, N, and log(1/eta), with an
exponent depending only on the granted uniform conic polynomial.

## 8. Disposition

The tagged exact sequence, both resets, and stored expanded-coordinate
composition are admitted at the stated oracle scope. The report's unchecked
Friedman bound, unsupported coordinate-height line, and recurrence prose
are not needed. Its claims about large naive recurrence bounds are not
algorithmic lower bounds.

Still OPEN is a native implementation of the uniform expanded relative-conic
primitive at growing degree. Calling a conic algorithm that in turn requests
many complete lower U presentations reintroduces a coupled recurrence;
the present two-child U count does not pay that recurrence. No compact-input
expansion, general classical Selmer theorem, unconditional tower speedup,
hardness claim, or quantum advantage beyond charged factoring follows.
