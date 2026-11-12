# Broad-character phase construction: independent core review

2026-11-12. Reviewed the completed paid report
`audits/openai_runs/2026-11-12-fast-character-build/response.md`, its exact
`audits/api_inputs/2026-11-12-accelerated/character-build.md` request, the
three supplied Legendre notes, and the retained Russell--Shparlinski text
(in particular Theorems 5--6). Read current `STATE.md`, `TRAPS.md`, and
`GOAL.md`. No network, API calls, Git, code, or numerical sweep was used.

**Disposition.** Equation (5), including its constant, is proved for the
explicit bounded-parity-expansion source model. It is an average over
irreducible targets, uniform over every fixed public choice of coefficients
and query subsets. It rules out a uniform polynomial-resource construction
of that form. It is not a general source, circuit, query, or decoding lower
bound. The report needs the scope repairs below; its principal inequality
does not need repair.

## 1. Core inequality and coherence

Fix `d>=3`, odd prime `p>=256d^2`, `m=2d-1`, and all exact-degree-m
squarefree public masks with arbitrary nonzero leading coefficient. There
are `M=(p-1)(p^m-p^(m-1))` masks. For coefficients independent of hidden Q,
suppose

    h_R(Q)=sum_A c_(R,A) f_A(Q),  f_A(Q)=product_(x in A) F_Q(x),
    sum_A |c_(R,A)| <= L,
    xi_Q=M^(-1/2) sum_R h_R(Q)|R>.

Here `xi_Q` is one successful unnormalized clean branch, not its
renormalized output. Put `g_R=lambda_p(Res(Q,R))` and
`T_Q=M^(-1/2)sum_R g_R|R>`. Then

    J_Q=|<T_Q,xi_Q>|^2 = s_Q * squared conditional fidelity.

The exact complex-coefficient expansion is

    E J_Q = M^(-2) sum_(R,R',A,A') c_(R,A) conjugate(c_(R',A'))
                       E[g_R g_R' f_A f_A'].

Thus the proof retains interference between every pair of factor classes;
it does not replace their coherent superposition by a mixture. Target-
dependent global phases cannot invalidate this squared-overlap expression.

For a uniform irreducible monic Q of degree d, identify its d conjugate roots
with full-degree elements theta of F_(p^d), only for analysis. Norm identities
give `F_Q(x)=chi_(p^d)(x-theta)` and the nonzero resultant identity. Every Q
has exactly d such roots, so the averages agree. This uses no algorithmic
extension-field access.

If two squarefree masks have different monic nonsplit parts, some nonlinear
irreducible factor in their product has odd multiplicity. Multiplication by
any native parity `product_(x in A triangle A') (x-X)` cannot cancel it.
Finite fields are perfect, so an odd-multiplicity root remains over the
algebraic closure. The polynomial is nonsquare and has degree at most
`2m+p`; the usual Weil bound applies even when the parity includes all p
base-field points.

Writing `q=p^d`, the excluded subfield union has size at most

    B <= sum_(e=1)^floor(d/2) p^e <= (3/2)sqrt(q).

Restricting the complete sum to full-degree elements costs at most B.
Native query factors have no zeros there. Padding resultant zeros changes
the summand only at roots of `RR'`, at most `2m` elements, by at most one
each. Therefore the cross-class correlation is at most

    [(p+4d-3)sqrt(q)+B+4d-2]/(q-B) <= epsilon,
    epsilon=2p^(1-d/2).

The last constant is comfortably valid at the stated threshold. The
bound is simultaneous for all public R,R',A,A'; it is not a claim for
each fixed Q.

A class with nonsplit part B and `s=m-deg B` contains exactly
`(p-1)binom(p,s)` labels. Since `s<=m<=p`,

    mu_B=binom(p,s)/[p^m(1-1/p)] <= 1/[(1-1/p)m!].

Bounding same-class correlations by one and cross-class correlations by
epsilon in the full expansion gives the slightly sharper intermediate form

    E J_Q <= L^2 [sum_B mu_B^2 + epsilon(1-sum_B mu_B^2)]
          <= L^2 [1/((1-1/p)(2d-1)!) + 2p^(1-d/2)].

This proves report (5) at L=1 and (11) generally. Markov's inequality (6)
is valid. It permits exceptional easy Q, including success concentrated on
an exceptional target set. It does not imply a pointwise upper bound for
every irreducible Q or an average over all squarefree Q.

## 2. Exact scope and corrections

1. **Polynomial quantifier.** The right side at L=1 is uniformly
   `exp(-Omega(d log d))` as d grows. It defeats inverse-polynomial success
   with polynomial L whenever `log p<=poly(d)`, and therefore defeats a
   claimed uniform `poly(d,log p)` algorithm for every prime above any
   polynomial threshold: choose a polynomial-size prime subfamily. It does
   not by itself rule out `1/poly(d,log p)` success pointwise when log p is
   arbitrarily enormous. At general p the actual rejection test is
   `L^2[(1-1/p)^(-1)/(2d-1)!+2p^(1-d/2)] < s_0 f_0`.

2. **Fixed-B padding error.** Report lines 94--98 require Q to be root-free,
   or every supported mask to be coprime to Q; merely `gcd(Q,B)=1` is
   insufficient. For example, take degree-three
   `Q=X(X-1)(X-2)`, an irreducible quadratic B, and a split cubic L
   containing X. For every scalar a, `lambda(Res(Q,aBL))=1`. The native
   scalar factor `chi(a)^3` instead changes sign when a changes quadratic
   class, so one global phase cannot correct the class. This preliminary
   claim is valid for the theorem's irreducible degree-d targets and its
   failure does not affect (5). Do not silently discard zero labels.

3. **Allowed clean operation.** The Cauchy--Schwarz argument covers a
   public query-list state u_R, one diagonal native-parity operation, and
   projection onto one public normalized state v_R, with the coefficient
   label R retained: `c_(R,A)=conjugate(v_(R,A))u_(R,A)` after grouping
   repeated parities. Public diagonal corrections are allowed. Arbitrary
   label mixing, oracle-dependent classical branching, intermediate
   interference, nonlinear BIT processing, and arbitrary retained garbage
   are not automatically covered. For K separately accepted clean
   branches the corresponding inequalities must be summed, costing up to
   K; an exponentially large accepted subspace cannot be covered for free.
   A polynomial number of branches or repetitions still fails on the
   polynomial-size-prime subfamily. No unknown preparation inverse is
   supplied or needed in this proof.

4. **Thinning and precision.** A fixed public subset of relative density
   alpha has maximum class mass at most `mu_max/alpha`; the report's
   subset bound follows for the normalized target on that subset. It is
   not target-adaptive thinning. The all-coefficient projection argument
   is valid within the same bounded-expansion architecture. A trace-
   distance epsilon implementation claim must refer to the full normalized
   output including herald flags (or an equivalent event-probability
   guarantee); then the joint projector probability changes by at most
   epsilon. The initial public squarefree projection succeeds with
   delta=(1-1/p)^2. Multiplying by this omitted constant can only decrease
   the upper bound on all-flags success.

## 3. Constructive target and classical baseline

The broad ideal target really would suffice. In the virtual etale-algebra
state the unit fraction is `u=product_j(1-p^(-d_j))>=1-d/p`. The intersection
of unit labels and squarefree exact-degree-m labels has ambient density
at least `delta+u-1`, so its squared overlap with T_Q is at least
`(delta+u-1)^2/(delta u)>=(1-(d+2)/p)^2`. On the virtual Fourier support,
the trace pairing twisted by a unit is nondegenerate and every Hankel solve
returns Q. Consequently report (2) and its decoding lower bound are valid
for every monic squarefree Q, not just irreducibles. This supplies no
native procedure to prepare its phase. The paid QFT, public arithmetic,
Hankel solve, and output costs in the supplied note remain polynomial.

For two distinct monic squarefree degree-d polynomials, write their product
as `D^2 UV`, with `D=gcd(Q,C)`. The distinct part UV is nonsquare. Comparing
the padded sign product directly with `chi(UV)` costs at most 2d in the
complete sum: common roots cost at most two each, other roots one each.
Weil therefore proves the report's correlation bound
`(2d-1)/sqrt(p)+2d/p`. At `p>=256d^2` the resulting agreement bound is
stronger than the stated 3/4. Union-bounding at most p^d candidates gives
exactly the stated sample count and `p^d poly(d,log p,log(1/eta))` time.
Filtering candidates for squarefreeness makes its hypothesis explicit and
does not change the bound. Alternatively, for any distinct monic degree-d
C, QC cannot be a square since that would force Q to divide C; the general
degree-2d Weil bound also handles the unfiltered enumeration.

Verification of an adaptively proposed candidate must use fresh samples,
with its error budget divided over the capped number of proposals. Public
candidate evaluation supplies no values of the unknown Q. The elementary
baseline is independently checked here. The retained Russell--Shparlinski
Theorem 6 supplies a query/POVM result with `d<=p^(1/2-epsilon)` for fixed
epsilon; it does not supply an efficient receiver, and that hypothesis
must not be replaced by just `p>=256d^2`. The supplied full-table baseline
retains its existing degree/error promises and polynomial-p cost. No
classical hardness follows.

## 4. A concrete native operation outside the restriction

The missing permission is not extension/value access. Ordinary nonlinear
processing of BIT answers already escapes polynomial parity-expansion norm.
This can be proved on the actual irreducible-target promise, so it is not
merely a large expansion on an irrelevant full Boolean cube.

Take `d>=4`, choose `2d` distinct public points, and set

    b_j=(1-F_Q(x_j))/2,
    H(Q)=product_(i=1)^d (-1)^(b_(2i-1)b_(2i)).

Compute the 2d bits, apply the d reversible AND phases, and uncompute.
This uses 4d BIT calls and polynomial workspace/gates. Each pair factor is
`(1+F_1+F_2-F_1 F_2)/2`, so H has `4^d` parity terms, all of magnitude
`2^(-d)`. For every nonempty native subset A, the same full-degree-element
Weil argument gives `|E_Q f_A|<=epsilon=2p^(1-d/2)`. Hence for every A,

    |E_Q H f_A| <= 2^(-d)+2^d epsilon.

Any exact representation `H=sum_A c_A f_A` on the promised irreducible
targets consequently satisfies

    1=|E_Q H^2| <= (sum_A |c_A|)(2^(-d)+2^d epsilon),
    sum_A |c_A| >= 2^d/(1+4^d epsilon) >= (8/9)2^d.

The last inequality follows from
`4^d epsilon<=2^(9-2d)d^(2-d)<=1/8` in the stated regime.
To make this a relative coefficient phase, apply H only on masks with
publicly nonsquare leading coefficient, and apply 1 on the other half.
Even a Q-dependent global rephasing cannot give polynomial norm to all
amplitudes: if both rephased amplitudes had norm at most L, their product
with one conjugated would represent H with norm at most L^2. Thus
`L>=sqrt(8/9)2^(d/2)` remains necessary.

This is an explicit permitted, efficient operation outside the falsified
architecture, not a resultant-phase synthesis or reconstruction algorithm.
It explains why the proved obstruction must remain a narrow source-model
result. The next constructive obligation is to derive the desired relative
nonsplit phases, or another useful recoverable-moment law, from such an
explicit native operation with paid joint probability and precision.

**Claim gates remain false:** unrestricted phase-synthesis impossibility,
pointwise all-Q upper bound, arbitrary receiver failure, query/gate lower
bound, classical hardness, novelty, speedup, or quantum execution. No
further finite control is needed for the algebra above. Parent integration
should record the restricted closure and these scope repairs in the
handoff/state; no sweep or new receiver implementation is warranted by
this report alone.
