# Uniform Derived-Rank Rees Extension

2026-10-23. Proposed corollary of the existing Rees composition, NOT an
independently verified theorem, new arithmetic primitive, implemented quantum
receiver, or application-level speedup. The point is a uniform parameter
bound, not another finite HSP benchmark. All input/source promises of
REES_HSP_REDUCTION.md remain in force.

## 1. The Unresolved Question

The previous proof only stated polynomial time at fixed nilpotency class.
Can it give a uniform algorithm when class grows but the derived algebra
is small, without hiding an exponent depending on class in log(p)?

Input: an explicit n-dimensional nilpotent Lie algebra L over a supplied,
verified odd prime field F_p, actual class c<p, and an ordinary coherent
HSP oracle on exp(L), or the separately justified coset-copy source.
Public structure constants, their validation, all copies/queries, reversible
arithmetic and precision costs are paid. No opaque group-to-Lie conversion
is included in this extension. Put r=dim[L,L] and r_d=dim gamma_d(L).

**Proposed bound:** the existing composition admits

    2^O(r^2 log(r+2)) * poly(n, log p, label/access width, log(1/epsilon))

bounded-error time. The exponent of the polynomial is independent of r and
c. More precisely, its scalar-line source factor is

    P_scalar = product_(d=2..c) (d+1)^r_d.

With the actual prime it improves to

    delta_d = gcd(d,p-1),
    P_p = product_(d=2..c) (delta_d+1)^r_d <= P_scalar.

For r=0 use the abelian algorithm and the empty product. For growing r,
the sufficient condition r^2 log(r+2)=O(log I), where I is explicit input
length, gives polynomial time. Padding an algebra with irrelevant abelian
directions can manufacture this regime: that is NOT an application.

## 2. Descend Along Public Lines, Not Whole Grades

In A/(sum_(j>d) A_j), grade A_d is central and dilation Delta_s acts on
it by scalar s^d. Choose ANY public complete flag of this grade. Every
line and every flag prefix is central and dilation invariant. The hidden
image remains homogeneous after quotienting by a prefix; nothing requires
the flag to be adapted to the UNKNOWN hidden intersection.

At each line, measure its character on d+1 fresh incoming sources, giving
scalar labels lambda_i. A nonzero solution of

    sum_i lambda_i s_i^d = 0

is enough for the existing complete central instrument. The central
intersection is either trivial or the whole line. The all-record proof
already covers both cases and every positive-probability label tuple.
Zero scales are consumed/discarded; an all-zero witness is forbidden.
Each returned source is independent of the measured records, so the
induction applies on disjoint fresh source trees.

This uses van de Woestijne's scalar diagonal-equation theorem, quoted as
[Fact 2 of Ivanyos--Santha](https://arxiv.org/html/1503.09016): d+1 inputs
and deterministic time polynomial in d and log p. Their elementary
recursion immediately following Fact 2 also gives (d+1)^m variables
for m equations. This ingredient and the scalar recursion are known.
For delta_d=1 the two-label equation is elementary linear algebra.
We are not extrapolating the paper's FIXED-degree multi-equation theorem
to a uniform complexity assertion. No scalar solver is implemented here.

For the field-sensitive version, solve a degree delta_d equation instead.
Choose u with d*u=delta_d modulo p-1, and set s_i=x_i^u for x_i!=0 and
s_i=0 otherwise. Then s_i^d=x_i^delta_d and nonzeroness is preserved.
Computing u is modular inversion after division by delta_d; when the
modulus is1, u=0 works on NONZERO entries. Never turn 0^0 into1.
The new lift_scalar_witness verifies the supplied equation before converting.
It is not a diagonal solver or a field-element search.

## 3. Uniform BCH Without Enumerating Free Lie Words

For Z(t)=log(exp(X)exp(tY)), the standard differential identity is

    Z'(t) = [ad_Z/(1-exp(-ad_Z))] Y,   Z(0)=X.

This is the usual inverse-exponential differential construction, not a
new BCH formula; compare [Wehler, Section4.1](https://www.mathematik.uni-muenchen.de/~wehler/LieAlgebrasLieGroupsScript.pdf).
Here is a self-contained finite-field implementation argument.
Modulo z^c write

    f(z) = (1-exp(-z))/z = sum_(k=0..c-1) (-1)^k z^k/(k+1)!,
    b_0=1,  b_k = -sum_(j=1..k) f_j b_(k-j).

Thus b_1=+1/2, b_2=1/12, b_4=-1/720. The sign corresponds to the
ordered product exp(X)exp(tY), not its reverse. All inversions divide by
integers at most c, hence are valid for p>c.

Assume Z_0,...,Z_j are known. Repeated polynomial bracket convolution
computes the coefficient of t^j in sum_(k=0..c-1) b_k ad_Z^k(Y).
Divide by j+1 to obtain Z_(j+1), for j=0,...,c-1. All brackets of
length >c vanish. The universal rational BCH polynomial has total Lie
degree <=c and denominators supported on primes <=c, so this recurrence
reduces modulo p. Its t-degree is <=c; the ODE uniquely determines these
coefficients because 1,...,c are invertible. Sum them to evaluate at t=1.
There is no analytic convergence assumption or infinite-series truncation
error. The derivative's characteristic-p kernel is irrelevant below degree p.

The implemented recurrence makes exactly

    (c-1)*c*(c+1)*(c+2)/6

bracket calls. With an N-dimensional structure tensor each costs O(N^3)
field operations, and polynomially many O(log p)-bit operations. Polynomial
convolution stores O(cN) field elements, aside from the public tensor and
arithmetic workspace. Reversible implementation must compute/copy/uncompute
these operations and pay for its ancillas. This proves a uniform public
arithmetic bound, NOT an implementation of that reversible circuit.

The callback implementation assumes a genuine bilinear Lie bracket and a
correct class bound. Canonical vector checks do NOT establish either.
An explicit underestimated-class control gives the wrong answer, as it
must. Production use must freeze/validate public structure constants and
compute the lower-central series, not infer promises from passing examples.

## 4. Complete Parameter Accounting

Nonzero lower-central terms strictly decrease: equality at any nonzero
term would propagate and contradict nilpotence. Therefore

    c <= r+1,
    r_d <= r-d+2 (2<=d<=c),
    D = n + sum_(d=2..c) r_d <= n + r(r+1)/2,
    P_p <= P_scalar <= (r+2)^[r(r+1)/2].

The public flag does not shrink the cover below its proven ansatz dimension
bound. It changes the descent schedule and its arithmetic dependency.

Take M=n+t terminal sources with t=ceil(log_2(3/epsilon)). This conservative
choice bounds rank failure using the earlier 1/((p-1)p^t) inequality.
There are L=M*P_p lifted leaves and c*L original oracle calls OR original
copies. Work backward through every scalar-line conversion to count nodes;
do not reuse incoming states or suppress zero-scale targets.

If T is the number of conversion nodes, their arities are at least2, so
T<=L-M and the number of central character measurements is exactly L+T-M.
The full-instrument count including leaves and final readout is L+T+M<=2L.
Each complete instrument receives error at most epsilon/[3(L+T+M)].
Its precision overhead depends on log L, not L. The scalar solver is
deterministic under its cited theorem; capped failure allowances are still
needed if a randomized replacement is used. Input source approximation
must obey the JOINT bank contract, not only marginal fidelity.

All algebraic precomputation on the cover and its central quotients is
polynomial in D,c,log p. Combining the preceding counts gives the uniform
parameter bound in Section1. This is not a claim about an uncharged
free-Lie input bridge or the general-exponent outer reduction.

If gcd(d,p-1)<=b for all d<=c, then P_p<=(b+1)^[r(r+1)/2]. For example,
p=2q+1 prime with q prime and q>c has indices1 or2, hence P_p<=3^[r(r+1)/2].
This gives a sufficient r^2=O(log I) regime for SUCH SUPPLIED primes. No
efficient safe-prime generator, density theorem, or arbitrary-prime claim
is being smuggled into the input model.

## 5. Try To Kill The Claim

- **Does an arbitrary central line preserve the hidden subgroup?** It
  need not lie inside it. The quotient uses HZ/Z; dilation preserves both
  H and Z. Transversality is unnecessary by the existing central lemma.
- **Does fixed-class complexity prove this by itself?** No. Its hidden
  exponents must not depend on c in log p. The scalar solver's uniform
  degree bound and the explicit ODE arithmetic close that specific gap.
- **Could known commutator enumeration already do this?**
  [Ivanyos--Magniez--Santha, Theorem11](https://arxiv.org/html/quant-ph/0102014v1)
  gives time polynomial in input size plus |G'|. Here |G'|=p^r, so that
  particular bound is not f(r)*poly(log p). This comparison does NOT
  establish novelty against all quantum HSP algorithms.
- **Is it practical?** No. A class12 filiform profile (13,11,10,...,1)
  has D=79. Even at p=47, producing16 terminal samples consumes exactly
  30,943,274,395,471,606,638,515,847,168 original inputs under this schedule.
  This is a sufficient symbolic count, not a measured quantum runtime.
- **Is the classical problem hard?** Not established for any useful
  explicit application. Generic oracle query gaps already exist in abelian
  HSP and do not prove a new computational separation. Existing explicit
  orbit/stabilizer families must still face their classical algorithms.
- **Does this validate the whole Rees theorem?** No. A flaw in its cover,
  central contraction, source assumptions or oracle accounting invalidates
  this corollary. It inherits every unverified whole-theorem obligation.

The extension should be dropped if its sole value becomes reparameterizing
bounds or adding fixtures. Next scientific work needs a genuinely new
algorithmic consequence, a decisive whole-proof counterexample, or the
unresolved native classical construction, not a benchmark campaign here.

## 6. Artifacts And Verification

`theorems/uniform_bch_rees.py` contains the arithmetic evaluator, witness
conversion/verification, and exact scalar-line source budget. It imports
only the standard library; it does not touch offloaded theorem modules.
`tests/test_uniform_bch_rees.py` compares against independent matrix exp/log
at classes1,2,3,4,5,6,8,9,12, including boundary primes and a127-bit prime.
It checks attained class, operation count, multiplication order, inverse,
associativity, invalid contracts, every scalar field entry/degree at six
small primes, exact forest accounting and the field-sensitive schedule.
These are mathematical unit controls, not generated oracle problems.

39 new tests pass; combined with the9 source-bank controls,48 pass (0.42s).
Python syntax and targeted whitespace checks pass. The review manuscript
compiled successfully; document compilation is not a formal proof check.
The full Rees integration is NOT validated: its transitive
prime_character_opi.py and jet_oracle_homogenization.py dependencies remain
compressed,dataless, confirmed by fresh metadata inspection.
No hydration, relocation, qsearch/UI/central-registry admission, Git write,
new agent, or contact with another task was performed.
