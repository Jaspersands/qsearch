# Compact-input Kronecker computation by one Laurent coefficient

CLOSED WRITTEN end-to-end CLASSICAL algorithm (13 November 2026). Native input: three partitions lambda,mu,nu in compact binary Frobenius coordinates, with the actual Durfee lengths a=Durfee(lambda)<=fixed d, b=Durfee(mu)<=fixed e. Numerical n may be exponential in total input bit length L. Output exact ordinary g(lambda,mu,nu), target deterministic poly_de(L) BIT time, including output. No character, count, advice, coefficient or lattice-point oracle. The existing numerical-n dense-grid algorithm is NOT enough. The earlier fixed-Durfee proof is closed written, both paid reports terminal and checked; its algebra can be reused, not its clock.

Selection: this exact coefficient mechanism removes a specific native input-size blocker for the same externally motivated counting problem. Corpus lookup on binary Frobenius/fixed Durfee/super-Weyl/Barvinok preceded primary source checks; no exact prior record found (not novelty). Strongest baseline is the checked numerical-n compiler, ordinary fixed-row vector-partition algorithms, and Panova's min-dimension-polynomial theorem. Actual Barvinok-Pommersheim fixed-dimensional binary counting theorem is now checked. Full ratio-promise/growing-Durfee and quantum novelty remain out of scope.

Let X=(x_1..x_a | y_1..y_a), Z=(u_1..u_b | v_1..v_b), p_r(X)=sum x_i^r+(-1)^(r-1)sum y_i^r. Tensor alphabet T has even xu,yv and odd xv,yu. F=hs_nu(T)=sum g(rho,sigma,nu)hs_rho(X)hs_sigma(Z), with surviving shapes in(a,a)/(b,b) hooks. This identity, ordinary g, hook vanishing and independence are already checked. Hence if Durfee(nu)>2ab, F=0 and g=0; otherwise c=Durfee(nu)<=2ab is fixed. For n=0 output1; reject inconsistent input sizes by exact binary sums.

NEW SINGLE COEFFICIENT: Q_X=prod_(i,j)(x_i+y_j), Q_Z similarly. Delta(x)=prod_(i<j)(x_i-x_j), and similarly y,u,v. Expand each Q_X inverse as prod_i x_i^(-a)*prod_(i,j) sum_(k>=0)(-y_j/x_i)^k, and similarly Q_Z about u. Let alpha_i=lambda_i-i, beta_j=lambda'_j-j be lambda's Frobenius arms/legs, gamma/delta those of mu. Exact formula:
 g(lambda,mu,nu) = [x^alpha y^beta u^gamma v^delta]
   F * Delta(x)Delta(y)Delta(u)Delta(v)/(Q_X Q_Z).

Reason: a surviving rho of Durfee EXACTLY a contains the a-by-a rectangle and hs_rho(X)=Q_X*s_(rho_i-a)(x)*s_(rho'_j-a)(y). Multiplying both Vandermondes yields two alternants with exponents rho_i-i and rho'_j-j; the fixed strictly descending nonnegative target can match only rho=lambda, coefficient+1. If Durfee(rho)<a, use hs_rho=sum_kappa s_kappa(x)s_(rho'/kappa')(y), kappa subset rho and len(kappa)<=a. Every such kappa has kappa_a<a. Delta(x)s_kappa is an alternant with at least one exponent<a. Q_X inverse shifts every x exponent by -a and then only DECREASES x exponents, so every resulting monomial retains at least one negative x exponent; it cannot contribute to the target. Delta(y) does not change x. This is a formal-chamber identity; the common completion is proved below. Same for Z. No full basis enumeration.

NEW FINITE RATIONAL COMPILER: use Giambelli for nu in c fixed Frobenius rows:
 hs_nu(T)=det(hs_(r_i+1,1^(s_j))(T))_(i,j<=c).
Expand only c! terms, a constant depending on d,e. Give every selected hook its own auxiliary t_j,w_j. The hook generating identity is
 sum_(r,s>=0) hs_(r+1,1^s)(T) t^r w^s = (H_T(t) E_T(w)-1)/(t+w),
where H_T(t)=prod_odd(1+z*t)/prod_even(1-z*t), E_T(w)=1/H_T(-w)=prod_even(1+z*w)/prod_odd(1-z*w).
For coefficient t^r w^s with r,s>=0 one may use H_T(t)E_T(w)/(t+w), expanding 1/(t+w)=t^(-1)sum_(j>=0)(-w/t)^j; the subtracted1 has only negative t degree. Hooks have independent auxiliary variables, so no leakage between hook factors.

After multiplying by Vandermondes/Q_X/Q_Z, expand constant-size numerators and determinant permutations. Each resulting rational term is a Laurent monomial times a product of a FIXED number of factors(1-epsilon*z^v)^(-1), with integer exponent vectors v of fixed dimension and epsilon=+/-1. Target exponents are binary Frobenius coordinates. No numerator is expanded to numerical degree n.

CRITICAL FINITENESS: claim every contributing geometric occupation is <=n. Hook j consumes auxiliary w-degree, so j<=s_j<=n. The H even-denominator occupancies sum to at most r_i+j+1<=r_i+s_j+1<=n; E odd-denominator occupancies sum to <=s_j<=n. Numerator contributions have nonnegative t,w degrees. Each Q_X geometric variable increases a y exponent; all other sources have nonnegative y exponents, including Delta(y), so its value<=target beta_j<=n; similarly v. Negative x/u/t shifts do not create an unbounded cycle. This must be proved term by term, not from cancellation after an infinite expansion. For every off-diagonal cell, r_i+s_j+1<=n-c+1<=n.

For each rational term write all exponent matching equations A k=b with 0<=k<=C_de*n+C_de. Deal with (-1)^k by enumerating parity of the fixed number of signed indices and substituting k=2z+epsilon (constant number of branches). Each branch is an explicit bounded rational polytope in a fixed number D_de of variables; entries of A are fixed small integers, right sides have O(L) bits. Count its integer points using the actual fixed-dimensional algorithm; sum with the known signs. Equality constraints can be two inequalities or removed by paid Smith form. Need account empty/lower-dimensional polytopes. Counts are <=(C_de*n+C_de+1)^D_de, so output/intermediate bitsO_de(log(n+1)); all lists/branches depend only on fixed d,e. Full uniform algorithm generates its fixed matrices from d,e, not hidden advice.

Required result: prove/refute this complete binary-input compiler, with every formal-series coefficient, variable bound, source hypothesis, output and bit cost. No extension to growing Durfee, no claimed new quantum algorithm, no novelty/priority claim. Standard fixed-dimensional integer counting is a classical baseline, not a free oracle. Supplied actual source excerpts retain URLs/hashes/physical LF locators.

STATUS: complete written binary-input proof, independently reviewed and parent checked. No implementation or priority claim.


## Parent refinement: bounded dimension and exact cap

For c=Durfee(nu)<=2ab, the number of geometric occupations is
D=a^2+b^2+c(4ab+1)<=a^2+b^2+8a^2b^2+2ab. The signed indices are exactly
the a^2+b^2 Q-inverse occupations and the c hook w/t occupations. All
numerator and determinant branches have a count depending only on a,b.

The off-diagonal hook concern has a simple resolution: if r_i,s_j are any
Frobenius arm/leg of nu, then r_i+s_j+1<=sum_i r_i+sum_j s_j+1=n-c+1<=n.
Thus the explicit cap n is valid for every geometric index. Auxiliary
w-degree first bounds the hook j by s_j; the t-degree then bounds total H
occupancy by r_i+j+1<=n. Every Q_X occupation increases one y exponent,
while all other rational factors have nonnegative y exponents; hence it is
at most the target leg beta_j<=n. The same holds for v and Q_Z. There is
no unbounded cancellation cycle in an individual monomial coefficient.

Each parity branch is an explicit bounded polytope A k=b, 0<=k<=n with
D fixed and binary right sides. Replace signed k by2z+epsilon and enumerate
only the fixed number of parity choices. Barvinok-Pommersheim Algorithm5.2
counts each branch with its actual binary input-size clock. The count size
is at most(n+1)^D, so even the signed intermediate totals have O_de(log n)
bits. These bounds are proved in the complete independent audit and checked by the parent.


## Closed proof and report dispositions

Complete proof: `audits/reviews/2026-11-13-binary-durfee-native-audit.md`,
219 lines, all parent read. The theorem is deterministic poly_(d,e)(L) BIT
computation of exact ordinary g for EVERY valid compact binary Frobenius
triple with two fixed Durfee bounds. Validate all arrays/sizes; n=0 is
handled separately; c>2ab returns zero. No numerical-n loop or supplied oracle.

One common completion uses weights x=u=t=1 and y=v=w=2. Every geometric
direction has strictly positive integer weight, so each coefficient is finite
before cancellation and all polynomial/inverse identities agree there. The
private t,w variables justify omitting each hook's subtracted1. The explicit
n-box then follows from w,y,v degree equations. Exact uniform branches number
at most c!(a!b!)^2*2^(4abc+a^2+b^2+c). All are generated, not supplied advice.

The source backend is Barvinok--Pommersheim, Theorem4.4 and Algorithm5.2,
retained actual text at `audits/sources/2026-11-13-kronecker-ratio/`.
Binary facet size is LF155--174; algorithm statements LF936--964 and
1056--1105. Lower-dimensional and empty bounded polytopes are covered.
Alternatively enumerate fixed-many vertex candidates, compute the affine
hull, pay Smith/Hermite integer parametrization, and reduce its dimension.
Construct the short generating function, choose the moment-curve direction
avoiding all poles, and take each exact fixed-degree Taylor constant term.
Keep denominator leading signs; no numerical limit or free count oracle.
Counts and signed totals have O_de(log n) bits. Internal counting arithmetic
has polynomial-in-L bits, not a claimed O(log n) bound on every intermediate.

Three paid jobs completed with material findings parent checked in full:
- Claude coefficient,245LF: exact extractor confirmed. Its formal-ring,
  exact-Durfee, cap, parity, lower-dimensional and bit-cost obligations are
  discharged in the full proof. Its loose doubled Q-variable bound is safe
  but the actual count is a^2+b^2. Its numerator-choice signs are unnecessary:
  H/E numerator coefficients are positive; determinant signs remain.
- OpenAI counting,318LF: independent explicit parity polytope, affine-hull
  fallback and paid Taylor evaluator checked. No source authentication was
  inferred from its label; parent read the actual primary files.
- Claude Sergeev,231LF: direct alternative below checked. Its criticism of a
  per-variable cap concerns that alternative only; the direct prompt already
  specified a weight cap. Its displayed input-size formula in section6 is
  incorrect: always use n=c+sum arms+sum legs. No practical-runtime claim
  imported. No retry. First two sessions reaped; third finished with saved
  usage and its PID absent (session ID was lost on tool-output truncation).
Reports/bundles are listed in `audits/api_inputs/2026-11-13-binary-durfee/dispatch.json`.
Round runner estimate USD2.528020, not provider billing or a measured balance.

Finite falsifier: `audits/controls/binary_durfee/exact_coefficient.py/.json`
checks ALL504 triples n=1..5, two actual Durfee bounds<=2, against ordinary
Sage Kronecker products.54 cached numerators,88 reference products; exact
QQ arithmetic and legitimate monotone exponent pruning. Parent inspected
all185 script lines. No mismatch; no all-input theorem inferred from this
finite control. No rerun or large sweep needed for the unchanged extractor.

## Direct Sergeev alternative and prior-art boundary

Parent read actual Rosas, arXiv math/0001084v1, Theorem11 LF557--622 and
hook-product application LF677--718. The supersymmetric coproduct/Sergeev
mechanism is prior art. Neither those excerpts nor Panova's open-question
paragraph proves priority of this general complexity composition. No novelty
claim is made. The Giambelli proof above is sufficient without this route.

Put m=2ab, E=(xu,yv), O=(xv,yu). Substitute U=E,V=-O into Theorem11.
Vandermonde and V^delta signs cancel. For c<=m, split the diagram of nu into
C=nu intersect[m]^2 and row/column tails r_i=max(nu_i-m,0),
s_j=max(nu'_j-m,0). Then
 F=Alt_E Alt_O [prod_i E_i^(m-i+r_i) prod_j O_j^(m-j+s_j)
                   prod_((i,j)in C)(E_i+O_j)]/[Delta(E)Delta(O)].
Only boxes IN C are cross factors. All firstm row/column lengths can be
computed in O_de(L) binary work from Frobenius data; never list all rows.
All E letters are distinct monomials, as are O letters, so both Vandermondes
remain nonzero under tensor substitution despite multiplicative relations.

Order original variables x,u,y,v and give them weights1,2,4,...,W where
W=2^(2a+2b-1). Distinct squarefree tensor monomials have distinct weights;
y/x and v/u have positive weight. Factor each other denominator binomial
by its lower-weight monomial. Its geometric ratio has positive weight.
All identities hold in the resulting finite-generation positive-weight
Laurent completion; this gives exactly the extractor's required chamber.
No claim of per-variable monotonicity is needed for the new Delta ratios.

There are D'=m(m-1)+a^2+b^2 indices, only Q indices signed. If M is one
numerator/prefactor exponent and tau is the target, the weight equation gives
 sum k <= wt(tau)-wt(M)
       <= W*(2n+2m(m-1)+a^2+b^2).
Every numerator exponent is O_de(n), encoded in binary. This termwise box,
parity split and the same charged counting algorithm give poly_de(L).
No auxiliary hook variables; constants remain enormous. No implementation
or additional finite controls were necessary to establish the main theorem.

## Remaining question and falsifiers

The classical fixed-Durfee baseline is closed, including compact binary
input. Growing Durfee and the full polynomial dimension-ratio promise are
NOT closed. Prior publication status remains unverified. A valid wrong
extractor coefficient, unbounded index solution or uncharged counting step
would refute this proof; no such defect was found. Choose the next research
question against independent high-upside directions, not a parameter variant.
