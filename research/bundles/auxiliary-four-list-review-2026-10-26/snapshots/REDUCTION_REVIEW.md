# Auxiliary Divisors For Generic-Class AG Full-Support Search

Date: 2026-10-26. Independent classical review.

## Decision And Handoff

**The auxiliary-code reduction is valid. Suitable auxiliary divisors exist
for every input class on all the certified levels with e >= 16. This is
not, by itself, an efficient constructor.**

The strongest fully specified construction supported here is a randomized
meet-in-the-middle algorithm taking

    T_access + 2^(r_2/2) poly(g, log q)

expected time and S_access + 2^(r_2/2) poly(g, log q) space, for e >= 32,
where T_access and S_access denote preprocessing time and storage, and

    r_2 = dim_F2 J(F_q)/2J(F_q) = dim_F2 J(F_q)[2].

The polynomial hides explicit curve/divisor representation costs. The
algorithm samples two sets of prime divisors whose degrees add to a,
matches their mod-2 classes, and halves the resulting divisible class.
The distribution argument below does NOT assume uniform prime classes.
Single-prime rejection gives a simpler 2^r_2 bound already for e >= 16.
These are constructions of this review from established primitives, not
claims that a cited paper states this particular AG attack or that it is
optimal.

**No uniform polynomial-time constructor for arbitrary G on the specified
infinite tower has been established here.** The source certificate does
not bound r_2 by O(log g), nor provide a polynomial small-effective-coset
algorithm. Linear r_2 would make the displayed algorithms exponential;
this is a limitation of these algorithms, not a hardness theorem.

Importantly, **halving need not be the exponential bottleneck** once the
explicit Jacobian, its order, uniform sampling, and pairings are available.
Section 5 gives a polynomial-time reduction using order-2 pairings and
integer linear algebra. Full odd-order factorization or odd-part discrete
logarithms are unnecessary.

The decisive next input is one of:

1. A certified rational 2-rank bound r_2 = O(log g) for the actual chosen
   cofinal tower sequence, together with charged source access.
2. A polynomial algorithm for the particular degree-a effective mod-2
   representative problem, possibly exploiting the tower.
3. An explicit auxiliary witness (F, eta) for each actual input, with its
   construction cost recorded. Once supplied, the full-support solve is
   polynomial and works for every syndrome.

Stop this literature search here. Neither the missing constructor nor a
failed experiment would establish classical hardness or quantum advantage.
The generic 3-torsion counting review is not repeated.

## 1. Input, Scope, And Exact Reduction

Read as source premises:

- [GENERIC_CLASSES.md](/Users/jaspersands/Developer/qsearch-research-work/generic-divisor-class-2026-10-26/GENERIC_CLASSES.md).
- [TOWER_SOURCE.md](/Users/jaspersands/Developer/qsearch-research-work/prime-ag-tower-source-2026-10-26/TOWER_SOURCE.md).

Fix an actual smooth curve X/F_q in the certified unramified S-split tower,
q = 100003, cover degree e, with

    g = 5e+1,  d = 10e+3 = 2g+1,  m = 22e,
    k = ell(G) = g+2 = 5e+3,
    a = deg(K-G-2F+D) = 2e-9 = (2g-47)/5.

B is any full-row-rank generator matrix of V = ev_D L(G), so the original
problem is Bz = s with every z_i nonzero. Here G is any rational degree-d
divisor class, represented away from D. No near-canonical assumption is
made. The tower's existence/source certificate is accepted, not reproved.

Choose a rational point O over infinity and write J = Pic^0(X)(F_q). Let

    C = K-G+D,           deg C = 2d+a,
    t = [C-(2d+a)O] in J.

For an effective rational divisor A of degree a, the condition is exactly

    [A-aO] = t in J/2J.                              (1)

If x = t-[A-aO] and 2f = x in J, then the degree-d class [F] = d[O]+f
satisfies 2[F] = [K-G+D-A]. Conversely, every successful F supplies an
effective representative of K-G-2F+D. No geometric half over an algebraic
closure is substituted for a rational half.

Move F within its class off D and compute a nonzero section of
L(K-G-2F+D). Multiplying a chosen canonical differential by that section
gives eta in Omega(G+2F-D). Principal-divisor witnesses, moving, RR bases,
and evaluations must all be charged; class congruences alone are not
evaluation matrices.

### Degree Minimality

The parent's additional observation is correct. If deg F <= 2g and F is
nonspecial, RR gives ell(F) = deg F + 1-g <= g+1. If F is special and
ell(F)>0, Clifford gives ell(F) <= deg F/2+1 <= g+1. Thus ell(F)>=g+2
forces deg F>=2g+1. Dropping the auxiliary degree cannot retain the needed
k-dimensional auxiliary space. This is not an obstruction to other,
non-AG auxiliary constructions.

## 2. Once F Exists, The All-Syndrome Solver Works

The mixed multiplication theorem applies because both degrees are at
least 2g+1:

    L(F)L(F) = L(2F),
    L(G)L(2F) = L(G+2F).

Consequently V*E^2 = ev_D L(G+2F), where E = ev_D L(F). Evaluation of
L(G+2F) need not be injective. The relevant theorem is
[Couvreur--Marquez-Corbella--Pellikaan, Theorem 5 and Corollary 6](https://arxiv.org/html/1401.6025v3).

Let h be the residue vector of nonzero eta in Omega(G+2F-D), and T its
support. Residues are not all zero: otherwise eta would lie in
Omega(G+2F), impossible because 3d > 2g-2. More directly, a simple pole
with zero residue is not a pole. Thus

    h perpendicular to V*E^2,
    |T| >= 3d-2g+2 = 20e+9 > 2d = 20e+6.           (2)

For the support estimate, eta has order -1 at points of T and order at
least zero at D\T. Outside D its order is at least the coefficient of
G+2F. Hence div(eta) >= G+2F-sum_(P in T)P, and taking degrees gives
|T| >= 3d-2g+2. This also covers non-effective G and F: eta can have
additional poles at their negative coefficients, which the inequality
already accounts for.

Let M generate E. Both B and M have k rows: d<m and RR gives k=g+2.
A nonzero word in either code vanishes at no more than d points of D.
For every U subset T, if rank B_U<k then |U|<=d; if
rank M_(T\U)<k then |T\U|<=d. By (2) these two deficiencies cannot occur
together. Therefore

    rank B_U + rank M_(T\U) >= k    for every U subset T.

The matroid-intersection min-max theorem gives a common size-k column
basis I subset T, found with polynomially many matrix-rank queries.
Separate full-rank restrictions would not alone imply a common basis;
the all-subsets inequality is the missing step that makes this claim valid.

For completeness, the actual norm solve can be written without any
probabilistic rank test. Restrict B,M,h to T; set w=1_I and c_i=w_i/h_i.
For u=M^T v put

    z_i = h_i ((u_i+c_i)^2 - nu),  i in T,
    z_i = 1,                     i outside T,

where nu is a nonsquare in F_q. The quadratic term in Bz vanishes by
orthogonality. The coefficient matrix of v is

    2 B_T diag(w) M_T^T = 2 B_I M_I^T,

which is invertible. Solve the resulting linear equation for the residual
syndrome after subtracting the constant terms, including B_(outside T)1.
Every coordinate is nonzero because nu is nonsquare. For this q, nu=2
works. This is the auxiliary-code norm ansatz of
[Ragavan--Shutty, Section 6.1, Theorem 6.2](https://arxiv.org/html/2610.00502v1),
with the common-basis and support arguments supplied above.

This produces witnesses, not a uniform distribution over the solution
fiber. It preserves the original syndrome and all coordinates.

## 3. Existence In Every Doubling Coset

This section proves a sufficient bound directly, rather than invoking an
unquantified positive-density assertion. Let Q=J/2J and N=|Q|=2^r_2.
For a degree-n prime P define v(P)=[P-nO] in Q. Write B_n for the number
of degree-n primes and B_n(c) for the number with v(P)=c.

For n>=1 define the deliberately loose constant

    C_n = (g+1)(n+6).

The following estimates suffice:

    |n B_n - q^n| <= C_n q^(n/2),
    |n sum_(deg P=n) chi(v(P))| <= C_n q^(n/2)       (3)

for every nontrivial character chi of Q.

Proof of the character estimate: class field theory associates chi to a
connected unramified double cover Y_chi -> X in which O splits. It is
geometric, and Hurwitz gives genus 2g-1. The difference
#Y_chi(F_(q^n)) - #X(F_(q^n)) equals

    sum_(j|n) j sum_(deg P=j) chi(v(P))^(n/j).

Weil's bound makes its absolute value at most (6g-2)q^(n/2).
The proper-divisor terms have j<=n/2. Bounding each jB_j by
q^j+1+2gq^(j/2), and using at most floor(n/2) terms, bounds their sum by
n(g+1)q^(n/2). This proves (3); the trivial-character estimate follows
from the same argument on X. No large class-field presentation is
constructed in this proof.

The class-field interpretation of mod-2 prime conditions is also explicit
in [Czogala--Koprowski, Theorem 1 and Section 3](https://arxiv.org/html/1904.12177v1).
The finite-field Weil/prime-count and tower framework is discussed in
[Elkies et al., Lemma 2.1 and Section 3.2](https://arxiv.org/html/math/0208060).

Character orthogonality now gives

    |n B_n(c) - q^n/N| <= C_n q^(n/2).              (4)

In particular, if

    q^(n/2) > 2 N C_n,                              (5)

every coset contains a degree-n prime, and uniform prime sampling hits
any prescribed coset with probability at least 1/(3N).

At n=a and r_2<=2g, condition (5) holds for every e>=16 in this family.
This was checked at e=16 by the exact integer inequality

    100003^23 > (2 * 2^162 * 2378)^2.

Its left/right ratio is greater than 12,944,860,411. The ratio increases
with e: the exponential factor per increment is q^2/2^20, whereas the
ratio of successive C_a values is less than 2. Thus the initial exact
inequality proves the whole range, not just the tested values.

**Deduction:** for every rational degree-d G on every such level e>=16,
there exists an effective degree-a prime A satisfying (1), hence a rational
F of degree d and a nonzero differential as required. This theorem does
not depend on the same-code cubic annihilator being present or absent.

The sufficient bound fails at e=8 when using r_2<=82. This says neither
that auxiliary F fails to exist there nor that its actual r_2 is 82.

## 4. A Constructive Birthday Attack

Uniform prime sampling is an actual available primitive, not a free
oracle: [Bruin, Algorithm 3.2](https://arxiv.org/html/1003.2563) gives an
expected-polynomial sampler in an explicit Khuri-Makdisi curve
representation, for nonempty prime sets of the requested degree. It does
not require the zeta function. The needed graded coordinate algebra and
divisor factorization still have to be supplied/computed.

A uniformly sampled prime does NOT give an exactly uniform class in Q.
Let mu_n be its class distribution. From (3), if q^(n/2)>=2C_n,

    |mu_hat_n(chi)| <= epsilon_n := 2 C_n q^(-n/2)   (6)

for nontrivial chi. This quantitative bias bound is what the algorithm
uses.

Set b=floor(a/2)=e-5 and c=ceil(a/2)=e-4. Suppose

    q^b >= 64 C_b^2 N,     q^c >= 64 C_c^2 N.        (7)

Then epsilon_b,epsilon_c <= 1/(4 sqrt(N)). Sample two independent lists
of L=ceil(sqrt(N)) uniform primes of degrees b and c. Store the first
list by v(P), and seek v(P)+v(R)=t. A match gives A=P+R of degree a.
Here sampling is with replacement; that causes no correctness problem.

### Why The Nonuniform Birthday Search Succeeds

Let p_t be the match probability for one pair. Fourier inversion gives

    p_t >= (1-(N-1)epsilon_b epsilon_c)/N
        >= 15/(16N).

Also max mu_n <= 1/N+epsilon_n. If Z counts matching pairs between the
two lists, then

    E Z = L^2 p_t,
    E Z^2 <= E Z + (E Z)^2
               + L^3 p_t (2/N+epsilon_b+epsilon_c).

The last term accounts for pairs sharing a list entry; pairs sharing no
entry are independent. Under (7), E Z^2/(E Z)^2 < 5, so
Pr(Z>0)>1/5 by the second-moment inequality. Independent restarts give
expected O(sqrt(N)) samples, class evaluations, and stored entries.
This proof avoids assuming independence among all L^2 candidate sums.

At the worst-case rank r_2=2g, both inequalities (7) hold for all e>=32.
For the more restrictive b at e=32, the exact check is

    100003^27 > 64 * 5346^2 * 2^322.

The integer part of the ratio is
64,040,584,432,915,384,358,798,429,809. Successive ratios grow because
q/2^10>97 and C_(e+1)/C_e<2. The c inequality is easier at the initial
level and obeys the same growth estimate. Hence e>=32 is an all-level
sufficient guarantee, not an empirical extrapolation.

Combining with Section 5 gives the displayed 2^(r_2/2) construction cost.
The single-prime alternative from Section 3 needs O(2^r_2) trials and
only polynomial working space beyond preprocessing. Smaller degrees can
use their actual rank and the same inequalities; the stated cutoffs are
conservative universal ones. No optimality is asserted, and no unproved
multi-list/subset-sum heuristic is included in the guarantee.

## 5. Charge Class Coordinates And Halving Correctly

### Established Primitives

[Bruin, Sections 3.5-3.9](https://arxiv.org/html/1003.2563) supplies uniform
Jacobian sampling given the zeta function, efficient Frey-Ruck pairings,
and rational torsion-basis computation. For n=2 the perfect pairing is

    J[2](F_q) x J(F_q)/2J(F_q) -> {+1,-1}.

A rational 2-torsion basis therefore labels mod-2 classes by r_2 bits.
Pairing computations, RR representations, and the basis are preprocessing,
not an assumption that arbitrary group elements arrive as bit vectors.
[Couveignes](https://arxiv.org/html/0706.0272) is an antecedent for the
torsion linearization methods; its hypotheses explicitly include the
Frobenius characteristic polynomial.

### Polynomial Halving: A Reduction, Not An Implementation Claim

Here is a self-contained way to avoid charging an unnecessary 2^r_2
enumeration for halving. This is a synthesis using the preceding pairing
primitive. It is not a claim that computing a Kummer map alone returns
a rational half.

Suppose h=|J(F_q)|=2^s M with M odd is known and uniform sampling is
available. Multiplying uniform elements by M samples the 2-primary
subgroup H uniformly. Its order is 2^s, and s=O(g log q). For any list
T_1,...,T_t in H[2], all F_2 relations can be computed in expected
polynomial time: pair against independent uniform Jacobian elements and
take the kernel of the resulting sign matrix. Verify every proposed
kernel basis vector by actual group addition. If any is false, add rows.
Perfectness makes this a Las Vegas procedure with polynomial expectation.

Now take sampled generators h_1,...,h_t of a subgroup of H. Their full
integer relation lattice can be recovered as follows. Let
phi: Z^t -> H map the standard basis to this list, and initialize

    L_0 = 2^s Z^t subset ker(phi).

At each stage compute the elementary 2-group

    V_i = {v in Z^t : 2v in L_i}/L_i.

SNF/HNF computes a basis of V_i with at most t elements. Their images
under phi lie in H[2]. Compute the kernel of this map by the verified
pairing procedure, and adjoin its lifted vectors to L_i. If there is no
enlargement, L_i=ker(phi): otherwise the nontrivial finite 2-group
ker(phi)/L_i would contain an element of order 2, giving an enlargement.
There are at most st strict enlargements, and lattice entries have
polynomial bit length. Thus the full relation lattice and the generated
group order are obtained in polynomial time.

Continue uniform sampling until that order is 2^s. The expected number
of samples is polynomial; completion is certified by the known order.
Apply SNF to obtain coordinates, including a target by appending it to
the generator list if necessary. Divisibility by 2 in H and a half, when
one exists, are now ordinary integer congruence computations.

For x in J, first solve 2u=Mx in H. If it is insoluble then x is not in
2J. Otherwise

    y = u - ((M-1)/2)x

satisfies 2y=x. No factorization of M and no discrete logarithm in the
odd-order part was used. All successful outputs can be checked by
doubling in J. Large scalar multiples here use repeated Jacobian
addition/reduction, not expanded divisors with degree proportional to 2^s.

For comparison, purely generic black-box p-group algorithms have
prime-exponent base cases with p^(r/2) cost; see
[Sutherland, Sections 1, 3 and 4](https://arxiv.org/html/0809.3413).
That generic expense is not a lower bound for a Jacobian with pairings.
Conversely, knowing h alone does not justify taking an inverse of 2
modulo h when h is even.

### Zeta Function And Explicit Access

The order and uniform sampler are not automatically supplied by B. But
at fixed p it would also be wrong to declare point counting inherently
exponential in g. [Kyng, Theorem 1.1](https://link.springer.com/article/10.1007/s40993-022-00398-7)
states a zeta algorithm for the normalization of an arbitrary absolutely
irreducible plane model of degree Delta, with cost polynomial in Delta
and the finite-field extension degree, times p^(1/2+o(1)). The paper
explicitly gives an outline rather than a full complexity proof; its
reported implementation uses a larger p dependence. At fixed p=100003,
these are polynomial dependencies, not poly(log p) guarantees.

An explicit polynomial-size plane/graded model, normalization and divisor
arithmetic are still necessary. This review does not construct them for
arbitrary higher tower levels. A compact tower-existence certificate is
not those inputs. Even a polynomial theoretical order computation could
be impractical at the concrete matrix sizes in the parent note.

## 6. Why Other Apparent Shortcuts Do Not Close The Problem

### RR Systems And Random F

[Cascudo--Cramer--Xing, Remark 3.5](https://arxiv.org/html/1207.2936)
uses uniform class sampling when most classes satisfy the desired
vanishing equations. That is not a method to force effectivity of a
specified low-degree class after multiplication by 2. RR efficiently
tests a chosen F; choosing a successful F is a different task. Random
F can land in a very sparse effective locus. This review neither repeats
nor disputes the parent's accepted generic-G 3-torsion bound.

### Small Mod-2 Representatives From Linear Algebra

Suppose explicit primes P_j of degrees n_j have classes
[P_j-n_j O] spanning Q. Solving a binary linear equation produces a
subset J_0 for the target. It yields the effective representative

    A = sum_(j in J_0) P_j + (a-sum_(j in J_0) n_j) O

only if the selected total degree is at most a. Spanning by itself does
not bound this weight. A basis with total degree <=a would give a
polynomial constructor using Section 5, even with some linearly growing
r_2. Finding a low-weight representation in a larger factor base is a
separate optimization/search problem; no hardness claim is made for the
structured instances here.

There is a concrete obstruction to using only the 23e supplied splitting
points. Let S_X be all their lifts, including O. Class field theory gives

    Cl_(S_X) = J / <[P-O] : P in S_X>.

Since the S-split pro-2 extension above every finite level is still
infinite, it has a nontrivial quadratic quotient. Thus

    Q / span_F2{[P-O] : P in S_X} != 0.              (8)

Consequently those known rational points do not even span all target
cosets. If that quotient has rank r_S, exactly a 2^(-r_S) fraction of
uniform target cosets lie in the span, before imposing the degree bound.
This does not obstruct using additional rational points or higher-degree
primes. It does rule out assuming the splitting-point certificate is
already a universal small-representative constructor.

### Class Fields And Singular Elements

Explicitly building the full unramified elementary cover for Q has degree
2^r_2 and genus 1+2^r_2(g-1). Polynomial complexity in that cover's size
is exponential in r_2. Chebotarev existence or positive density does not
remove this cost. The proof in Section 3 uses individual double covers
only as a counting argument.

[Koprowski, Algorithms 3, 8 and 9](https://arxiv.org/html/2008.10335)
constructs singular square classes and compatible mod-2 coordinates.
Some routines assume a Picard-group presentation; the random routine
requires a divisor-class order and does not promise a uniform output.
They provide useful primitives, not a proved degree-a representative
algorithm for every prescribed coset. Random singular functions also
do not automatically yield the required effective divisor degree.

## 7. Rational 2-Rank Is Not Tower Depth

Always r_2<=2g in this odd characteristic. The base hyperelliptic curve
has full rational 2-torsion of rank 12, but this does not propagate as
either a constant rank or full rank at all higher levels. The splitting
condition proves r_S>=1 at finite tower levels, not an asymptotic upper
bound r_2=O(log g).

A refined chain of quadratic covers has depth log_2 e, while g=5e+1.
There is no identification of that depth with the dimension of the
rational 2-torsion of its terminal Jacobian. Likewise, the logarithm of
a next elementary class-field degree is the relevant class-group rank
at that level, not the logarithm of the already accumulated cover degree.

This review establishes neither logarithmic nor linear r_2 growth for
the particular unspecified cofinal sequence. The parameter accounting is:

| Certified rank regime | Birthday construction, with charged access |
| --- | --- |
| r_2=O(log g) | Expected polynomial time and space |
| r_2=o(g), but larger than O(log g) | Stated bound is subexponential in g, not necessarily polynomial |
| r_2=Theta(g) | Stated bound is exponential in g |
| Only r_2<=2g | Worst-case upper bound 2^g poly(g), not an efficiency theorem |

Large rational torsion is compatible with many rational points in
general; [Elkies et al., Theorem 1.3](https://arxiv.org/html/math/0208060)
constructs such families. That result is not a rank computation for this
specific tower. No characteristic-2 Deuring--Shafarevich formula is used
for 2-torsion in characteristic 100003.

## 8. Access Ledger And Falsifiers

The geometric attack consumes X, D, G and a usable divisor/RR backend,
not just the explicit matrix B. Without them it is an auxiliary-advice
attack, not yet a matrix-only solver. With them it amortizes its curve,
class-coordinate and F preprocessing across syndromes for the same B.
Finding a new F for a new generic G is part of input-dependent work.

| Stage | What must be charged or certified |
| --- | --- |
| Tower generation | Actual selected level, equations and evaluation places; existence alone is insufficient |
| Curve arithmetic | Polynomial-size representation, RR and divisor operations, factoring finite algebras |
| Class preprocessing | Zeta/order, exact uniform Jacobian sampling, perfect pairings, certified relations |
| Effective A | Prime sampling costs and the 2^(r_2/2) birthday lists, or a genuinely stronger constructor |
| Rational F | Halving, actual divisor representatives, principal witnesses, moving off D |
| Auxiliary code | Basis/evaluation of L(F), differential and residues, verification against the original B |
| Syndrome solve | Common-basis matroid intersection, linear solve, original Bz=s and all z_i!=0 |

Decisive falsifiers for a future efficiency or obstruction claim:

1. Prove r_2=O(log g) on the actual generated sequence: the birthday
   attack then becomes polynomial, subject to the access ledger.
2. Supply a bounded-total-degree mod-2 basis or another short-coset
   algorithm: this bypasses birthday search, even if r_2 is larger.
3. Claim supplied splitting points span Q: check (8); this contradicts
   the still-infinite S-split tower.
4. Claim all auxiliary divisors fail when the cube annihilator is zero:
   the all-G existence result for e>=16 contradicts that extension.
5. Claim halving costs 2^(2g) necessarily: the verified-pairing reduction
   in Section 5 refutes that necessity under its stated access assumptions.
6. Claim polynomial construction from Chebotarev alone: require the
   actual sampler, fixed-degree success probability and coset-query cost.
7. Claim a matrix-only attack: require extraction of the geometric data
   or a direct auxiliary-matrix algorithm; supplied geometry is not free.
8. Claim hardness because these searches are expensive or unknown:
   no such implication is supported.

## 9. Verification And Limits

No higher tower was generated, no generic G was sampled, no actual
auxiliary F was computed, and no timing benchmark is reported. There is
no new coding infrastructure. Only this review file was created.

Small exact controls used native arbitrary-precision integer arithmetic:

| e | g | a | Single-prime sufficient bound using r_2=2g | Both birthday bounds |
| --- | --- | --- | --- | --- |
| 8 | 41 | 7 | Fails | Fail |
| 16 | 81 | 23 | Passes | Fail (degree-11 side) |
| 32 | 161 | 55 | Passes | Pass |
| 64 | 321 | 119 | Passes | Pass |

The tested inequalities were q^a>(2*2^(2g)*C_a)^2 and
q^n>64*C_n^2*2^(2g), for n=floor(a/2),ceil(a/2). Also
2^50001 mod 100003 = 100002, confirming the nonsquare. The monotonicity
arguments, not the finite table, extend the bounds to all larger levels.

The all-syndrome algebra, rank argument, prime-bias estimate, birthday
second moment and pairing/lattice halving reduction are written proofs
in this review; they were not implemented or independently machine-checked.
The literature supplies the named primitives, not an already assembled
polynomial attack on this generic-divisor family.

**Final status:** auxiliary F is mathematically unavoidable at sufficiently
large levels, and a concrete rank-parameterized classical constructor is
available. Uniform polynomial construction for the parent's full source
model remains unresolved. This supports neither hardness nor advantage.
