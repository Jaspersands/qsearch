# The Convenient AG Example Is Not A Generic Local-Repair Test

2026-10-27. Independent agent mathematical review accepts the scoped
arguments below; see ../multibasis-extraction-review-2026-10-27/review.md.
This is not external peer review, a general hardness theorem, an executed
quantum algorithm or an advantage claim.

## Research Decision

The native problem is unchanged: explicit full-row-rank B over F_1019,
arbitrary syndrome s, and a required output z with Bz=s and EVERY z_i
nonzero. No planted witness, changed alphabet or free curve oracle is used.

The current degree-eight matrix admits a stronger deterministic classical
repair than the previous dimension-only greedy baseline. Its full Schur cube
does not prevent this. The same special-divisor construction remains easy
through dyadic degree 256, conditional on actual inputs and a checked fiber
partition. No degree-256 input was generated.

Conversely, the intended closed-prime-divisor source almost always excludes
these short kernel moves. This is a statement about the exact source law,
not a hardness inference. It invalidates using the convenient 11I-E matrices
as representative experiments for generic-class local repair.

Two proposed classical shortcuts also fail as general arguments: unfocused
stationary walks retain exponentially small hit mass, and fixed-bank walks
on valid states can have isolated vertices. State-adaptive long-move search
is still open. Do not confuse these three algorithm classes.

## 1. A Constructive Native Solver For The Special Divisors

On an unramified degree-e cover of the genus-six source, I is the pullback
of infinity, deg I=e, and div(dx/y)=10I. For a split, unramified fiber F_a
over x=a, div(x-a)=F_a-2I and |F_a|=2e. Suppose G=11I-E, with E effective
of degree e-3 and disjoint from the evaluation set D. Then

    eta_a=(dx/y)/(x-a),
    div(eta_a)=12I-F_a,
    div(eta_a)-(G-F_a)=I+E >= 0.

For every f in the COMPLETE L(G), f eta_a has possible simple poles only
at F_a. The residue theorem gives sum_(P in F_a) f(P)/y(P)=0. Thus the
vector v_a with coordinates 1/y(P) on F_a and zero elsewhere is a kernel
word, nonzero at every position of its fiber. This uses unramifiedness and
y(P)!=0. Column multipliers lambda_P require v_a(P)/lambda_P.

Given any particular solution z0, choose independently on each fiber

    c_a outside {-z0(P)/v_a(P): P in F_a}.

Then z=z0+sum_a c_a v_a has the original syndrome, and all coordinates are
nonzero. Disjoint supports are essential. There are at most 2e forbidden
scalars; 2e<p guarantees a choice. At p1019 this covers e<=509, or dyadic
e<=256. The prior dimension-only guarantee covered dyadic e<=128.

This is search, not uniform sampling. There is no asymptotic dequantization
at fixed p from the finite cutoff alone. A bad scalar set outside the cutoff
is not evidence of infeasibility.

The actual genus-41, 43-by-176 input has eleven disjoint 16-column blocks.
Every block has rank15 and a one-dimensional full-support nullspace. Its
alternating vector (-1,1,...,-1,1) agrees up to scale with these residues.
repair.py extracts and verifies these vectors FROM B, obtains a particular
solution, applies the repair and checks the original input. It accepts only
a supplied disjoint partition and verified local directions with block size
<p. An arbitrary hidden column permutation does not come with a free
partition-recovery oracle. Supplied candidate partitions are cheap to check.

Preprocessing by elimination is polynomial, conservatively O(m^3) field
operations and O(m^2) space. Once certified, a target solve uses the stored
linear inverse, O(m) inverses and forbidden-value computations, plus O(km)
original verification. The scalar scan needs only block_size+1 candidates,
not the whole field. No new broad workbench or heuristic tuner was added.

## 2. The Generic Source Usually Has No Such Local Moves

Fix an actual tower curve, D, and e>=8. Set

    g=5e+1, d=2g+1, k=5e+3, m=22e, t=2e.

For any T subset D of size t, completeness and Riemann-Roch imply

    rank(B_T)=ell(G)-ell(G-T)=t-ell(K-G+T),

because deg(K-G)=-3. A nonzero ker(B) word of weight <=t exists exactly
when some such restriction has rank below t. Padding a smaller support to
t positions is legitimate.

For each fixed T, [G] -> [K+T-G] is a bijection of degree-class torsors.
No multiplication-by-2/3 torsion factor appears. At most A_(t-3) image
classes are effective, where A_r counts degree-r effective divisors. The
class-count estimate from [Cascudo-Cramer-Xing, Proposition 3.4](https://arxiv.org/html/1207.2936#S3)
therefore gives, for uniform classes,

    eps_class <= binom(22e,2e) g / (p^(3e+3)*30^2).

Uniform classes are NOT the implemented-source contract. Reuse the reviewed
maximum-class-mass transfer in ../constructive-tower-2026-10-27/PRIME_CLASS.md:
each degree-d class contains at most (p^(g+2)-1)/(p-1) degree-d primes,
N_d>=p^d/(2d), and h<=33^(2g). Thus exact uniform CLOSED-prime sampling gives

    C_e=2dp/(p-1)*(33^2/p)^g,
    eps_prime <= C_e eps_class.

The prime-count premise p^d>=4(g+1)^2(d+6)^2 is checked. If the source then
rejects non-full Schur cubes with failure probability <=eps_cube, use

    Pr(d_min(ker B)<=2e | full cube) <= eps_prime/(1-eps_cube).

There is no independence assumption here. Additional acceptance conditions
need additional accounting. Approximate or biased source laws do not inherit
this estimate without an error budget.

This is a high-probability source property, not an efficient minimum-distance
certificate for each matrix. Exhaustively checking all subsets T would be
exponential. Do not silently add that enumeration to a polynomial source
algorithm. For a particular fixed move bank, directly checking its kernel
membership and weights is polynomial, but does not certify every kernel word.

At e8 the resulting upper bound is about 1.39236e-57. The unconditioned
bound decreases for every integer e>=8: bound the binomial one-step ratio by

    (22*9/8)^22/(4*20^20).

Including the genus, prime-degree and field factors bounds the total ratio
by 0.000057254. The cube-rejection bound also decreases to zero. All reported
probabilities are exact rational upper bounds before decimal display.

The even narrower condition that 11I-G has an effective representative has
uniform-class probability <=g/(p^(4e+3)*30^2); transfer and condition as above.
The actual degree-eight example was handpicked in this special set, not
sampled from the prime law. Its weight16 kernel words are fully consistent
with the counting theorem. No higher-degree matrix was generated here.

## 3. Which Walks Are Actually Excluded

### Unfocused affine walks: a first-hit bound

Let Omega={z:Bz=s}, S=Omega intersect (F_p^*)^m. Initialize uniformly on
Omega and use transitions preserving that uniform measure, for example
state-independent mixtures of kernel translations. Then each time marginal
is uniform, whether or not the walk mixes. With pi=|S|/|Omega| and
H=min{t>=0:X_t in S},

    Pr(H<=T) <= min(1,(T+1)pi),
    E H >= sum_(j>=1) max(0,1-j*pi) >= (1-pi)/(2pi).

The existing exact count gives pi=(1-1/p)^m(1+R_s),
|R_s|<=alpha=(p^k-1)/(p-1)^delta, delta>=12e-3. At fixed p the lower bound
is exponential in e for THIS class of searches. It does not cover a designed
initial state, state-dependent drift or focused repair. Fast mixing on Omega
alone would not fix the rare-target problem.

### Walks on valid states: isolation, not first-hit hardness

For a fixed nonzero v in ker B of weight w and a nonzero scalar c, the pair
z,z+cv being full support excludes two values on supp(v) and one elsewhere.
Character expansion, for p>=5 and alpha<1, gives

    Pr_(z uniform S)(z+cv in S)
      <= ((p-2)/(p-1))^w * (1+eta)/(1-alpha),
    eta=(p^k-1)*(2/(p-2))^delta.

The code caps normalized character magnitudes at1, which also safely handles
p3. On the native fixed field, alpha and eta decay exponentially. Exact base
and ratio checks bound (1+eta)/(1-alpha) by2 for all e>=8.

Conditional on the source distance event in Section2, every nonzero move has
w>=2e+1. For any L(e) directions fixed from B,s BEFORE drawing the state,

    Pr_(z uniform S)(any distinct valid bank-line neighbor)
      <= min(1,2L(e)(p-1)*((p-2)/(p-1))^(2e+1)).

For polynomial L this tends to zero. For example at the UNCONSTRUCTED e16384,
using L=17e-3 (a full kernel basis), the bound is below 5.849e-6. This is an
analytic parameter calculation, not a measured experiment. Add eps_prime /
(1-eps_cube) if reporting failure over the source as well.

This rules out irreducible valid-state samplers using only such a bank on
those instances; it is NOT a first-witness lower bound. Adaptive long moves,
invalid intermediates, larger banks, and unrelated classical solvers remain
unassessed. In particular, do not use isolated solutions to claim search is
hard: finding even one isolated solution already solves the search problem.

### Exact countercontrol and the LLL distinction

For ANY odd prime p let m=2(p-1)+1, B=(1,...,1), s=-1, x=(1,...,1),
v=(1,...,p-1,1,...,p-1,0), and d_j=v+e_j-e_m, j<m. These form a kernel
basis: in the usual basis its matrix is I+v*1^T with determinant1. Every
nonzero scalar move from x along d_j has a zero coordinate, since an
unmodified duplicate of -1/c remains. Yet other full-support solutions
exist and the rowspace distance is the maximum m. This is a non-AG
arithmetic countercontrol, not a new oracle problem or hardness instance.

The [Harvey-Vondrak resampling-oracle framework](https://arxiv.org/html/1504.02044v3)
requires both removal of conditioning and control of which new bad events
can be created. Pairwise independence is insufficient. For a uniform
sum-zero triple over F_p, the zero events are pairwise independent, but
Pr(z0=0 | z1,z2 nonzero)=1/(p-1), not1/p. Linear resampling along a kernel
direction is efficient and removes the one-coordinate conditioning, but
its potential new zero events lie on its support. Section2 precludes
bounded-support kernel repairs for typical large source inputs. It does
not prove that every possible resampling-oracle method fails.

## 4. Four Bases, Still No Extractor

The reviewer proved an additional native structural fact: complete
degree-(2g+1) AG inputs have FOUR disjoint column bases, not merely the three
implied by distance alone. Clifford/Riemann-Roch bounds prove the matroid
base-packing inequalities. Four is maximal because m<5k. The review gives
exact non-AG matrices meeting the numerical distance promises with only
three bases, so the native hypothesis cannot be dropped.

Known three-basis additive existence results still leave extraction steps
unimplemented. Literal partial-syndrome tables have exponentially many
entries; fixed alphabets of at most four values cannot cover all syndromes.
See the review for proofs, primary sources and exact controls. This is a
bounded failed extraction attempt, not a claim that no extractor exists.

## 5. Next Scientific Decision And Handoff

Do not spend the next pass building an MCMC framework, repeating AJT
existence, optimizing another prime, or testing generic-source claims on
11I-E examples. The new results remove those default next actions.

The leading remaining quantum claim is the reviewed unambiguous-decoder
transfer for full-support AG intersection, with raw success bounded by
(1-E_dec)^2/(1+alpha), not a measured speedup. Its actual significance now
depends on (a) whether that improved guarantee is already implicit in known
zero-error decoding/reduction results, (b) a complete end-to-end resource
statement, and (c) a useful problem reduction or a defensible new explicit
computational task beyond an unexplained classical extraction gap.

Next GPT pass: audit that precise novelty/theorem boundary against the
current Ragavan-Shutty paper and quantum-decoding literature, and produce
one consolidated theorem or a decisive falsifier. Compare the surviving
claim with the dormant bounded-copy DCP receiver direction; do not resume
DCP merely because this audit found another classical limitation. No new
receiver mechanism was supplied here. A publication-scale conditional coding
result is still not a Shor-level result.

Gemini: preserve the exact prime-sampler contract when implementing genuine
higher covers. Use 11I-E examples only as known-easy calibration cases.
Check the actual local kernel ranks and source provenance. Do not treat
this work as a new candidate-registry admission. Main CLI/UI wiring is
unchanged; these are mathematical controls, not a new search service.
