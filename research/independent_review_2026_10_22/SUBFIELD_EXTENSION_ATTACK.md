# Subfield attack strengthened to arbitrary public points

**Status: proved algorithms, with explicit remaining scope.** The earlier
single-buffer construction in SUBFIELD_CLASSICAL_ATTACK.md can fail on
rank-deficient point sets. That failure can be repaired. The deductions
below retain the given field, every public point, and every target bit.
No favorable-point distribution or supplied witness is needed.

## A. Every even degree: arbitrary points, enough zero targets

Write F=F_(Q²), k=F_Q, n=2 log2(Q), and let Z be the zero-target
coordinates. Assume Q>=16. Every element of k is an accepted zero value.
Choose theta outside k, so F=k+theta*k. Write

    S=span_k{H_i:i in Z},       r=dim_k S,
    d=dim_k(F^K/S)=2K-r.

For |Z|>=K, the MDS property gives K<=r<=2K-1. The upper bound comes
from the first row of H, which is one. We first give an elementary
algorithm when |Z|>=3K, and then reduce this threshold to 2K.

Choose a k-basis U of S from the zero-coordinate columns. Since r<=2K-1,
at least K zero coordinates remain. Choose any K of them as B. They
are F-linearly independent. Consequently

    S + theta*span_k{H_i:i in B} = F^K.

Put a fixed accepted value t on every one-target coordinate, giving a
syndrome h. Solve in the quotient F^K/S for y_i in k, i in B, such that
sum_(i in B) theta*H_i*y_i=-h mod S. For y_i=0 use x_i=0. For y_i!=0,
sample a_i uniformly in k until x_i=theta*y_i+a_i has inverse-trace bit
zero. Every such nonzero coset has zero-bit density at least 7/32, by
the exact coset calculation in SUBFIELD_CLASSICAL_ATTACK.md. Thus this
step costs constant expected work per buffer.

The new residual syndrome lies in S, because all H_i*a_i terms lie in
S. Correct it with values in k on U by linear algebra. Every coordinate
has its required bit, and Hx=0. There are at most K buffers. With a cap
B0 on each buffer search, failure is at most K*(25/32)^B0; a cap never
causes a false answer. All linear algebra can use the binary expansion
of the supplied field, so no uncharged k-field oracle is required.

### The stronger 2K-zero guarantee

The same algorithm works with |Z|>=2K by choosing disjoint U and B more
carefully. On ground set Z let M1 have columns H_i over k, with rank r,
and let M2 have columns theta*H_i in F^K/S, with rank d. The matroid
union rank formula is

    max(|U|+|B|) = min_(T subset Z)
        [|Z\T|+rank_M1(T)+rank_M2(T)],

where U,B are disjoint and independent in their respective matroids.
For |T|>=K, the MDS property implies rank_M2(T)=d, while
rank_M1(T)+|Z\T|>=r. For |T|<K, rank_M1(T)=|T|, so the displayed
quantity is at least |Z|>=2K. Thus the union has rank r+d=2K and
provides disjoint bases U,B. These bases are obtainable by the standard
polynomial matroid-union algorithm, using ordinary linear independence
tests. Now B has size d<=K. The quotient correction and buffer argument
above apply unchanged.

This use of matroid union is standard prior mathematics, not a new
combinatorial theorem. The rank formula is given in
[Goemans's matroid-union notes, Theorem 4](https://math.mit.edu/~goemans/18433S07/matroidunion.pdf);
[Cunningham's account of the matroid partition theorem](https://www.math.uwaterloo.ca/~whcunnin/coming.of.matroids.pdf)
also explicitly identifies its efficient constructive proof. The proof
above checks the actual rank hypotheses for this native H.

## B. Extension degree at least three: random accepted zero lines

Let n=e*m, e>=3, F=F_(Q^e), k=F_Q, Q=2^m. Let

    A={v in F:Tr_(F/k)(v)=0},
    T={1/v:v in A, v!=0}.

For every u in T, the entire k-line u*k consists of accepted zero values.
Indeed Tr_(F/k)(1/(u*a))=a^(-1)*Tr_(F/k)(1/u)=0 for nonzero a, and
zero is accepted too.

**Lemma: span_k(T)=F for every e>=3.** Suppose otherwise. Nondegeneracy
of the relative trace pairing supplies nonzero c with Tr_(F/k)(c/v)=0
for every nonzero v in A. Multiplying by X^(Q^(e-1)) gives the polynomial

    P_c(X)=sum_(j=0)^(e-1) c^(Q^j)*X^(Q^(e-1)-Q^j).

It has degree Q^(e-1)-1 and vanishes on all Q^(e-1)-1 nonzero roots
of L(X)=sum_(j=0)^(e-1) X^(Q^j). Hence P_c=c*L(X)/X. But the term
of exponent Q^(e-1)-Q on the left has coefficient c^Q!=0; its exponent
is positive and divisible by Q. Every nonconstant exponent on the right
is Q^j-1, which is not divisible by Q. This contradiction proves the
lemma. It also explains why e=2 is exceptional.

Suppose |Z|>=eK and choose any eK distinct zero-target coordinates.
For each such i, the set {u*H_i:u in T} spans the entire F-line F*H_i
over k. For a subset I of these coordinates, the sum of those spans has
k-dimension e*min(K,|I|), which is at least |I|. The independent-
transversal lemma therefore gives one u_i in T per selected coordinate
such that the eK columns u_i*H_i form a k-basis of F^K.

For completeness, the lemma follows by induction. If a proper subset
of the candidate sets has span dimension exactly its size, solve that
subset and then pass to the quotient by its span. The same dimension
inequalities hold for the remaining sets. If no proper subset is tight,
choose any nonzero representative for one set and quotient by its line;
all remaining subset dimensions decrease by at most one and still meet
the inequalities. This is the usual linear Rado--Hall argument, not an
assumption that a greedy selection always succeeds.

### Finding the directions without enumerating the subfield

Independently sample v_i uniformly from the relative-trace-zero space A.
Abort this trial if any v_i=0; otherwise put u_i=1/v_i and compute the
binary rank of the expanded columns u_i*H_i*k. A full-rank trial yields
a basis, and a single linear solve corrects the syndrome of fixed accepted
one-target values. All remaining zero coordinates can be set to zero.

This random search has a polynomial clock for fixed e in the native
scaling. In any k-basis of F, the coordinates of 1/v have denominator
Norm_(F/k)(v) and numerators of degree at most e-1: use the adjugate of
the multiplication-by-v matrix. Multiply the determinant of the eK
candidate columns by those denominators. The result is a nonzero
polynomial, by the independent-transversal argument, of total degree
at most eK*(e-1) in the independent coordinates of the v_i in A.
Schwartz--Zippel and a union bound give the conservative trial-failure
bound

    gamma <= eK*(e-1)/Q + eK/Q^(e-1).                 (1)

No property of random public points is used. Once gamma<=1/2, the
expected number of trials is at most two, and R capped independent
trials fail with probability at most gamma^R. At fixed e, N=n² and
K=floor(N/8), (1) is O(n²*2^(-n/e)). The relative trace, its kernel,
random draws, inversions and binary Gaussian elimination all cost
polynomially many bit operations. No q-entry or Q-entry table is needed.

### Explicit native thresholds and a conservative bit cost

Method A applies at every even n>=8, since then Q>=16. For e=3,
the bound in (1) is at most

    (3/4)*n²*2^(-n/3) + (3/8)*n²*2^(-2n/3).

At n=33 this is less than 0.4; it decreases along multiples of three
thereafter. Thus n>=33, 3|n is an explicit sufficient threshold for
expected at most two trials. The n=21 control is outside that conservative
theorem, although its returned witness independently verifies.

Using elementary polynomial-basis arithmetic, building the binary systems
and Gaussian elimination on O(nK) rows and O(nK) columns costs at most
O(n^9) bit operations at N=n². This is a conservative expected bound for
method B and the elementary 3K-zero version of A, including the expected
coset samples. Polynomially capped versions add only logarithmic factors
for inverse-polynomial failure. The sharper 2K-zero version of A adds a
standard polynomial number of linear-rank oracle calls for matroid union;
no O(n^9) bound is asserted for that unoptimized implementation.
These are elementary upper bounds, not measured large-instance timings or
a comparison of optimized constants with the quantum circuit.

## C. Deterministic degree-three attack, without a sampling threshold

The random-direction method B is not necessary when e=3. Three explicit
directions suffice, followed by deterministic matroid intersection.
This gives a polynomial algorithm for every n divisible by three with
n>=6, provided there are at least 3K zero targets.

Let a,b be a k-basis of A=ker Tr_(F/k), which has k-dimension two.
Choose three distinct t_1,t_2,t_3 in k; Q>=4 suffices. Define

    u_j=1/(a+t_j*b),       j=1,2,3.

Every u_j*k is accepted for bit zero. Moreover, u_1,u_2,u_3 are a
k-basis of F. Indeed z=a/b is outside k and therefore has degree three
over k. A relation sum_j c_j*u_j=0 would, after clearing denominators,
give a polynomial of degree at most two vanishing at z. It must be the
zero polynomial. Evaluating it at each -t_j forces c_j=0. No random
element, primitive multiplicative generator, or q-size enumeration is used.

Choose any 3K zero-target coordinates. On the ground set of 9K pairs
(i,j), use these two matroids:

1. the linear matroid over k represented by u_j*H_i in F^K;
2. the partition matroid allowing at most one pair for each coordinate i.

For any subset I of coordinates, the available vectors span
sum_(i in I) F*H_i, of k-dimension 3*min(K,|I|)>=|I|. The Rado argument
in B therefore guarantees a common independent set of size 3K.
Deterministic polynomial-time matroid intersection finds it. Its selected
vectors form a k-basis of F^K, so solve once for the syndrome of the fixed
accepted one-target values. The resulting x_i=u_j*c_i, c_i in k, satisfy
all zero bits; every original parity check is zero. Set unused zeros to
zero. The algorithm has no probabilistic failure event.

The required rank oracle is explicit: expand each u_j*H_i against a
binary basis of k and use binary Gaussian elimination. The binary rank
divided by log2(Q) is exactly its k-linear rank. These are scalar orbits
of vectors in a k-vector space, not arbitrary blocks whose selection
would be a different combinatorial problem. The partition oracle is a
coordinate-duplicate check. The ground set, number of oracle calls,
matrix sizes and arithmetic bit costs are all polynomial in n and N.
Standard deterministic augmenting-path matroid intersection is described
in [Goemans's notes, Section 5.2](https://math.mit.edu/~goemans/18433S11/matroid-intersect-notes.pdf).

A basis a,b is obtained without a k-field oracle: compute the binary
kernel of relative trace, pick nonzero a, form a*k using a binary basis
of k, and pick b outside that span. The two spaces have dimensions 2m
and m respectively, so this succeeds. Three distinct t_j are obtained
from 0, 1, and any k basis vector outside F_2.

A conservative bit bound for C is O(n^3*K^4)=O(n^11) at N=n^2, using
the elementary exchange-graph implementation. In each of O(K)
augmentations, rebuild a binary elimination basis with O(nK) rows and
columns, costing O((nK)^3) bit operations. Reduce O(K) outside vectors
against it, retaining their scalar coefficients in the selected k-basis;
this costs O(n^2*K^3) and identifies all fundamental circuits. A shortest
augmenting path then uses a graph with O(K) vertices and O(K^2) edges.
Precomputing the scalar-orbit columns with elementary field arithmetic
and the final solve/verification fit below the stated bound. This is an
unoptimized polynomial upper bound, not a claim of superior practical
constants or a ruled-out polynomial quantum speedup.

Self-attack: the Cauchy-fraction independence proof uses the PRIME relative
degree three; arbitrary independent a,b would not establish full degree
in a composite extension. No such generalization is assumed here. Rado
is used to prove the matroid optimum, not to justify a potentially failing
greedy assignment. A separate bounded prototype of this deterministic
variant and its native witness are recorded below.

## Native consequence and self-attack

For every even n>=8, arbitrary distinct public
points and any target with at least 2K zeros admit a polynomial classical
solver by A. For every n>=6 divisible by 3, any target
with at least 3K zeros admits a deterministic solver by C. In particular, for
uniform independent target bits, BOTH guarantees hold with overwhelming
probability for their respective n, independently of how the public
points were chosen. Hoeffding bounds the excluded target probability
by exp(-N/8) for the 2K threshold and exp(-N/32) for 3K.

This also applies to the natural inversion experiment that samples a
uniform codeword X in C and publishes only b_i=Tr(inv0(X_i)). Its target
law is exactly Pr[b]=2^(-N)*lambda_b, with |lambda_b-1|<=eta_N. Hence
the excluded probabilities are at most (1+eta_N) times the same Hoeffding
bounds. The hidden sampled X is never given to the algorithm; it finds
its own valid preimage. This is not a supplied-witness attack.

This substantially narrows possible advantage claims. The main A/C
guarantees leave other field degrees, especially prime n>3, and targets
below their zero-count thresholds unresolved. Method B gives additional
zero-rich subfamilies, not a general result for the remaining degrees.
The original problem did not
promise prime field degree or such targets, so those restrictions must
be stated as a new proposed hard subfamily, not silently retrofitted.

The main falsifiers are precise: a missing subfield trace factor, a
failure of the independent-transversal criterion, or a zero cleared
determinant. The displayed trace calculation, the MDS rank calculation,
and the actual independent representatives address them. The earlier
subfield-point one-hot counterexample falsifies only the single-buffer
ansatz; method A explicitly repairs it with multiple buffers. Neither
the existence of local zero lines nor the finite rank of a single
experiment is being substituted for these global arguments.

## Bounded implementation controls (experimental observations)

`subfield_extension_attack.py` was run once, with no input resampling.
The saved `subfield_extension_receipt.json` contains each full input and
witness, plus direct checks of all original parity and trace constraints.

- The n=20, N=400, K=50 one-hot input with all supplied points in the
  subfield, which defeated the earlier single-buffer method, is now solved
  by the elementary 3K-zero algorithm. The free binary rank is 500; the
  joined rank is 1000, using 50 nonzero buffers.
- At n=21, N=441, K=55 over X^21+X^2+1, points are the fixed polynomial
  labels 0 through 440. A fixed sampled target has 219 zero bits. The
  degree-three algorithm uses 165 of them, reaches binary rank 1155 on its
  first direction trial, and returns a native witness.

The script checks irreducibility, point distinctness, all syndromes, and
every inverse-trace target. Its two cases took about 0.46 seconds locally.
This is not an asymptotic benchmark. The sharper 2K-zero matroid-union
method is proved above but is not implemented in this small control.
At n=21 the conservative bound (1) exceeds one, so that experiment is
not claimed to be certified by the asymptotic sampling bound at that size.

`deterministic_subfield_attack.py` was then run once at n=9, N=81, K=10,
over X^9+X^4+1, with points 0 through 80 and exactly 3K=30 zero targets.
Its three directions are polynomial labels 275, 401 and 291. It constructs
a common independent set of size 30, reaches binary rank 90, and returns
a witness satisfying all original constraints. The full input, witness,
selected pairs and augmenting paths are in
`deterministic_subfield_receipt.json`. All 30 augmentations in this fixture
had length one; this checks the native direction/rank/solve interface but
does not exercise exchange paths. The general guarantee uses the standard
matroid-intersection theorem, not an empirical claim that greedy works.

A separate adversarial exchange control uses n=6, N=36, K=4 over
X^6+X+1. Eleven selected vectors have binary rank 22 and span the
k-hyperplane Tr_(F/k)(second syndrome component)=0. All three directions
at the last unused zero coordinate alpha=0 lie in that hyperplane, so
direct addition is impossible. The augmenting path adds pair (0,0),
removes (0,1), and adds (11,1), reaching rank 24 and a valid native witness.
`matroid_exchange_control.py` and `matroid_exchange_receipt.json` record
this single deliberately obstructed fixture. It tests the exchange branch
that the n=9 run did not exercise; it does not replace the general theorem.

## Search is solved here; uniform native sampling is a separate claim

The algorithms above find a witness. They do not reproduce the quantum
algorithm's exact uniform law conditional on native success. In the
specified implementation, when |Z|>2K in A or |Z|>eK in B/C, at least one
unused zero-target coordinate is deterministically set to zero. By
CONIC_REFORMULATION.md, a uniform native witness has any zero coordinate
with probability at most

    (2N/q)*(1+eta_(N-1))/(1-eta_N).

Consequently these stated classical output laws have total-variation
distance at least one minus that quantity from the uniform native law.
This is a distributional limitation, not a defect in their search result.
Randomizing unused coordinates would require a fresh distribution analysis;
it cannot be called a uniform sampler merely because every output verifies.
SUBFIELD_SAMPLING_LIMIT.md proves a stronger limitation: even randomizing
the correction positions and unused coordinates leaves these algorithms
at total-variation distance 1-2^(-Omega(n^3)) from uniform, because many
correction values necessarily lie in a rare relative-trace/subfield set.
This remains a statement about these algorithms, not a sampling lower bound.

For comparison, systematic accepted-prefix proposals followed by the K
linear completion checks do yield an exactly uniform witness conditional
on acceptance, but pay the previously derived lambda_b*2^(-K) acceptance
rate. The quantum full-list protocol pays lambda_b*(1-delta)^2/P and is
also exactly uniform conditional on native success. This distinction may
be a useful sampling question, but it does not restore a search advantage
on the families solved above and is not a classical sampling lower bound.

## A precise limit of simply exchanging the two target bits

**Proved deduction, limited to subfield-affine lines.** For fixed extension
degree e and Q sufficiently large, no affine k-line is entirely accepted
for bit one. Thus the zero-line attack cannot be extended to one-heavy
targets merely by exchanging the local bit labels.

To see this, write a line as u*(t+k), u!=0, and let d be the degree of t
over k; d divides e. If d=1, the line is u*k. Its inverse-trace bit is
Tr_k(r/z) with r=Tr_(F/k)(1/u), so it is either identically zero (r=0)
or exactly balanced (r!=0), including the totalized zero point.

If d>1, put r=Tr_(F/F_(Q^d))(1/u). On k the bit is Tr_k(R(z)), where

    R(z)=sum_(j=0)^(d-1) r^(Q^j)/(z+t^(Q^j)).

For r=0 this is identically zero. Otherwise R has precisely d distinct
simple poles, none rational over k, and R(infinity)=0. The smooth
Artin--Schreier curve Y²+Y=R(Z) has genus d-1. If S is its finite
additive-character sum over k, its point count is Q+S+2, hence

    |S+1| <= 2*(d-1)*sqrt(Q).

An all-one line would have S=-Q, impossible when
Q-1>2*(e-1)*sqrt(Q). The simple poles rule out an Artin--Schreier
coboundary, so the genus bound is applicable. This is the same standard
[Artin--Schreier bound](https://arxiv.org/html/1409.3694v1) used in the
quantum source audit.

Self-attack: this result says nothing about arbitrary binary affine flats
that are not k-lines, nonlinear local sets, or an adaptive global solver.
Small fields are excluded for a reason: in F_16 with modulus X^4+X+1,
the polynomial-label plane {2,3,4,5} is an all-one F_4 coset. A direct
four-value check confirms it; extrapolating that small example would fail
the displayed large-Q bound. No general hardness conclusion follows.
