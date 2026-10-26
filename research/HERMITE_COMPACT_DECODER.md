# Compact Hermite Decoder And Reversible Workspace

2026-10-21. Constructive follow-up to HERMITE_PINNED_DECODER.md.
Written resource and composition claims await independent review.
No quantum gate implementation, novelty claim, or central admission.

## Question And Decision

The previous pass used dense scalar matrices and an explicit affine basis.
Those are implementation choices, not intrinsic requirements of the pinned
decoder. This pass replaces them with polynomial-module interpolation,
a cardinal-polynomial right inverse, and recomputation of differential
solution vectors. The decoder still sees only the syndrome and retained
error blocks, never the true error/support or the original input tables.

The concrete consequence is a classical workspace bound of

    O_s(q*ell*log q) bits, with polynomial_s(q,ell) time.

Here s is the differential order, fixed for a fixed approximation target.
An input-preserving reversible simulation gives

    O_s(q*ell*log q*log(q*ell)) workspace,
    polynomial_s(q,ell) time.

The extra logarithm is NOT removed. This is not the exact original tight
O(q*ell*log q) quantum-space bound.

The primary quantum starting point is still
[Wu--Yang, 2610.01902v1](https://arxiv.org/html/2610.01902v1).
The possible contribution is a compact implementation of the proposed
small-characteristic pinned substitution, not a new decoding paradigm.

## Why Not Black-Box Rank Guessing?

Wiedemann/Krylov methods were considered. A scalar recurrence does not by
itself certify an inverse or full rank: an unobserved invariant subspace
can be singular. Weighted normal equations can also lose rank over a finite
field. A fully verified black-box approach remains possible, but is not
needed for this structured system.

Instead the interpolation unknowns are a fixed-rank polynomial vector,
not an unstructured scalar matrix. Polynomial row reduction and
interpolation modules are established techniques; see
[Mulders--Storjohann](https://cs.uwaterloo.ca/~astorjoh/jscpopov.pdf) and
[Kotter--Nielsen--Hoholdt interpolation](https://arxiv.org/abs/2207.01319).
This implementation uses elementary commutative-field operations and
gives the specific module invariant below.

## 1. Cardinal-Polynomial Right Inverse

Use the same fixed information set as the dense reference: all ell jets
at points 1,...,n/2. Set

    P(X)=product_(a=1)^(n/2) (X-a)^ell.

For a selected point a, let Q_a=P/(X-a)^ell and

    h_a(Z)=1/Q_a(a+Z) mod Z^ell.
    L_(a,j)(X)=Q_a(X)*(X-a)^j
                * [h_a(Z) mod Z^(ell-j)]_(Z=X-a).

The degree of L_(a,j) is less than K. Its information-set jets equal the
unit vector at (a,j), by direct Taylor expansion at a and multiplicity at
every other information-set point. These are columns of the inverse
evaluation matrix.

Given scalar syndrome u, compute

    (e0)_(a,j)=sum_h coefficient_h(L_(a,j))*u_h,

and set all other error blocks to zero. Consequently G*e0=u.
Each cardinal polynomial is built, used and discarded separately.
The full inverse matrix is NEVER stored.

Schoolbook multiplication, exact linear deflation, truncated series
inversion and Horner translation use O(K+ell) field elements.
The local residue-duality map from the previous pass is computed one
ell-by-ell block at a time. Even that dense local workspace is within
O(q*ell), because ell<q.

## 2. Constant-Rank Interpolation Module

Retain the previous parameters K, A and s, and the strict guard inequality

    (n-(d+2))*(ell-s) > A+K-1.

Write r=s+2 for the number of polynomial components. At a field point a,
define truncated polynomials

    Y_0(Z)=1,
    Y_(j+1)(Z)=sum_(u=0)^(ell-s-1) binom(j+u,j)*y_(a,j+u)*Z^u.

The module consists of Q in F_q[X]^r such that

    sum_j Q_j(a+Z)*Y_j(Z) == 0 mod Z^(ell-s)

at every point. It is closed under polynomial multiplication.
Start with the identity basis of F_q[X]^r and impose one coefficient
constraint at a time, in increasing Taylor order at each point.

Suppose the current basis already satisfies all earlier constraints and
the discrepancies for the next one are delta_i. If all are zero, do
nothing. Otherwise select p with delta_p nonzero and update

    B_i <- B_i - (delta_i/delta_p)*B_p, for i != p,
    B_p <- (X-a)*B_p.

These rows are a basis of the NEW constraint kernel, not just some valid
vectors. To prove spanning, write a vector in the old basis with polynomial
coefficients c_i(X). Because all lower Taylor constraints at a vanish,
the new discrepancy is sum_i c_i(a)*delta_i. After eliminating nonpivot
rows, the remaining coefficient of B_p therefore vanishes at a and is
divisible by X-a. The update has nonzero determinant X-a, so independence
is retained.

Use shifted weights

    w_0=-(K-1), w_(j+1)=-j.

A row has shifted degree max_j(deg Q_j+w_j), with ties broken by the
largest component index. Select a minimum-leading-term nonzero discrepancy
row as pivot. Every nonpivot update preserves or lowers shifted degree;
the pivot multiplication increases it by one.

After all constraints, perform shifted weak-Popov row reduction:
when two rows have the same leading component, subtract a monomial multiple
of the smaller one to cancel the larger leading term. The pair
(shifted degree, leading component) strictly decreases, so this terminates
in polynomially many reductions.

The resulting basis has distinct leading components. For a nonzero
polynomial combination of these rows, choose its maximal shifted term,
breaking ties by largest leading component. That term cannot cancel.
Thus the shortest nonzero module vector is at least as long as the
shortest basis row. The previous scalar dimension count proves some
module vector has shifted degree at most A, so the shortest row does too.
This supplies the same required degree bounds without solving the dense
homogeneous scalar system.

Existence of a short row is NOT a prescription to choose the shortest one.
The implementation considers all basis rows satisfying the degree bounds
and deterministically minimizes the certified number of zero leading
pivots, breaking ties by shifted degree and row index. This uses only the
unaugmented syndrome, never R or its values. It changes neither the root
guarantee nor the worst-case s*ceil(K/q) bound.

On the native input, the shortest row leaves a 24-dimensional affine
space and the eight pins leave four dimensions unresolved. The selected
alternative has 12 possible free coefficient positions, reduced by the
remaining identity equations to dimension one; the same eight pins then
resolve it. This is a real negative control against equating small
interpolation degree with a good decoder. It is not a general theorem
that the selection rule is optimal.

## 3. Storage Of The Module Basis

Let M=n*(ell-s) be the number of imposed scalar constraints.
Initially every row has shifted degree at most zero. Updates and reduction
therefore keep shifted degree at most M. Since the smallest weight is
-(K-1), every component has ordinary degree at most M+K-1.

At most r^2*(M+K+1) coefficients suffice for the persistent basis.
Local jet expansions use r^2*ell further field elements; temporary row
updates cost only a constant number of rows. For fixed s all are
O_s(q*ell), not O((q*ell)^2).

The artifact's peak basis-coefficient count measures this ONE component.
It is not a Python RSS measurement or a physical qubit estimate.

## 4. Differential Solving Without An Affine Basis

For the computed operator L=sum_j Q_(j+1) D^[j], define h and the leading
pivots R(t) exactly as in HERMITE_PINNED_DECODER.md. Let Z be the degree
indices with R(t)=0. Their count z satisfies

    z <= s*ceil(K/q).

Assign arbitrary values at these free degree indices. Descend from
degree K-1 to zero, solving f_t from the coefficient of X^(t+h)
whenever R(t) is nonzero. This defines an affine parametrization

    f(c)=f0 + sum_(j=1)^z c_j*f_j.

It includes every genuine solution, but may include vectors failing
remaining coefficient equations. In particular, zero pivots are not
assumed to be genuinely free.

Do NOT store the K-by-z array of directions. For each remaining identity
or pin constraint, regenerate f_j one at a time and retain only that
constraint's scalar row in the c variables. Maintain an incremental
echelon system of at most z rows and z+1 columns.

The implementation processes batches of at most floor(2K/(z+1)) constraints.
Each regenerated direction fills one column of that batch, and is then
discarded. The batch contains at most 2K field elements including its
right-hand side. This reduces repeated work without caching a K-by-z
direction array. Early full rank still triggers verification of ALL
original equations and pins, including unprocessed batches.

After a unique c is determined, regenerate the directions needed to form
f(c). Then recheck EVERY original polynomial coefficient equation and pin,
including constraints skipped after reaching full rank. Inconsistency
or unresolved rank means ABSTAIN. Full original syndrome and distance
checks are retained in the outer decoder.

The surviving dimension is exactly that of the full affine system:
nonzero-pivot rows were solved by construction; all other rows were
imposed or explicitly rechecked after a unique solution was obtained.
There is no randomized rank estimate or hidden solution list.

Storage is O(K+z^2) field elements. Since ell<q and s is fixed,
z^2=O_s(ell^2)=O_s(q*ell). The potentially expensive recomputation is
explicit and polynomial, not omitted from the time bound.

## 5. Reversible Bound Without Rereading The Stream

The compact algorithm is deterministic given the public pin set and the
augmented syndrome. Its loop bounds and worst-case recomputation time are
polynomial in q,ell for fixed s.

Apply the input-preserving simulation of
[Bennett](https://doi.org/10.1137/0218053) to this POSTPROCESSING ONLY.
For a fixed positive time-overhead exponent it uses O(S*log T) space
and polynomial time when classical time T is polynomial. All constants
and the logarithmic space overhead are retained.

Do not apply a naive history simulation to the entire length-N stream:
that could require revisiting or retaining the original input. Here the
decoder input is the small syndrome/register state AFTER source loading.
Recomputation accesses only public field arithmetic and retained registers.
The streamed membership tables are never consulted again.

The input-preserving decoder can be computed and uncomputed coherently,
used to form the equality herald, and used again to erase the original
error register on accepted labels. The full B_(d+2) isolation and local
second-moment argument from the preceding pass remain necessary.
The native 8->12 missing-guard counterexample is not superseded.

## Proposed Theorem With Quantifiers

This is a REVIEW-PENDING theorem proposal, not a promoted result.

For every fixed alpha<1, choose constants
0<lambda<tau<1/2 with 1/2+sqrt(lambda*(1-lambda))>alpha.
Choose fixed s satisfying

    (s+3)/(2*(s+2)) < 1-tau.

There is an ell0 depending on these constants such that, for all ell>=ell0
and sufficiently large q, the interpolation inequality holds including
the two-block guard. More precisely, its limiting agreement threshold is

    (s+3)/(2*(s+2))
      + s*(s+1)/(2*(s+2)*(ell-s)).

The second term can be made smaller than the chosen fixed margin uniformly
for ell>=ell0; the additional 2/n guard cost then vanishes.

For ell=o(q), random pin budget r=O_s(ell+log q) has r/n=o(1).
Take pin failure at most 1/n. The product-source tail is exponentially
small, and the previously derived unnormalized second-moment bound gives
overall success approaching one. Therefore sufficiently large q gives
success at least .99.

Subject to the source and composition proofs, the resulting one-pass
algorithm has polynomial_s(q,ell) preprocessing/update/postprocessing
time and O_s(q*ell*log q*log(q*ell)) reversible workspace.
The input tables can be arbitrary and arrive in arbitrary order.
No additional input pass or QRAM is introduced.

This covers sufficiently large FIXED ell as well as growing ell=o(q).
It does NOT cover all fixed multiplicities, particularly ell=1.
For ell=floor(q^a), 0<a<1, it retains the proposed polylog(N) consequence.
Any transfer of the published classical lower bound must retain its
unknown alpha-dependent constants and the correct input-access model.

## Falsifiers And Scope

1. A module update that only preserves valid rows without spanning the full
   kernel would invalidate the shortest-vector argument. The spanning
   proof above is essential.
2. Arbitrary unshifted row reduction can violate the asymmetric degree
   bounds. Tests check every local constraint and every component bound.
3. Treating all zero pivots as free without residual equations is wrong.
   The compact solver is compared to independently computed dense ranks.
4. Early full rank is not permission to skip consistency checks. Explicit
   wrong-pin and high-degree inconsistent controls must be rejected.
5. A small Python object count is not a qubit bound. The written coefficient
   ledger, all scratch storage, and reversible checkpoint overhead matter.
6. Fixed s is crucial. Uniform efficiency as alpha approaches one with
   the input size is NOT established.
7. This is still a classical decoder inside a proposed quantum streaming
   composition. No new unrestricted classical hardness or time advantage
   follows from the decoder alone.
8. Module interpolation, polynomial row reduction, side-information
   decoding and reversible simulation are prior art. Review the novelty
   of this particular theorem/application, not of those ingredients.

## Reproduction And Next Work

Run `python -m theorems.hermite_compact_decoder` for the native replay.
Run the compact, pinned and folded-RS test suites together.
The dense pinned producer remains unchanged as an independent reference.

The saved replay uses the same q=31,ell=24,n=30,K=360 ambiguity as the
preceding pass: two weight-8 errors with one syndrome, source cap8 and
guard radius10. The chosen interpolation module stores at most3609
coefficients in its basis in this replay, compared with the dense
600-by-603 scalar interpolation matrix. The selected reduced system
stores156echelon field entries; its constraint batch stays below720.
These are component counts, not total RSS or physical qubits.
The complete four-decode replay, including the rejected shortest-row
policy, took about21seconds on this machine. It is a correctness replay,
not a timing advantage. Native quantum execution remains false.

Next scientific work should audit the stated theorem and compare it with
existing side-information and streaming results. Do not launch size/seed
campaigns, hide the extra logarithm, claim ell=1, or build a large circuit
before the theorem's correctness and significance receive independent review.
