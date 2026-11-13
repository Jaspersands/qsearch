# Compact-input Kronecker computation by one Laurent coefficient

NEW proposed end-to-end CLASSICAL algorithm. Native input: three partitions lambda,mu,nu in compact binary Frobenius coordinates, with the actual Durfee lengths a=Durfee(lambda)<=fixed d, b=Durfee(mu)<=fixed e. Numerical n may be exponential in total input bit length L. Output exact ordinary g(lambda,mu,nu), target deterministic poly_de(L) BIT time, including output. No character, count, advice, coefficient or lattice-point oracle. The existing numerical-n dense-grid algorithm is NOT enough. The earlier fixed-Durfee proof is closed written, both paid reports terminal and checked; its algebra can be reused, not its clock.

Selection: this exact coefficient mechanism removes a specific native input-size blocker for the same externally motivated counting problem. Corpus lookup on binary Frobenius/fixed Durfee/super-Weyl/Barvinok preceded primary source checks; no exact prior record found (not novelty). Strongest baseline is the checked numerical-n compiler, ordinary fixed-row vector-partition algorithms, and Panova's min-dimension-polynomial theorem. Actual Barvinok-Pommersheim fixed-dimensional binary counting theorem is now checked. Full ratio-promise/growing-Durfee and quantum novelty remain out of scope.

Let X=(x_1..x_a | y_1..y_a), Z=(u_1..u_b | v_1..v_b), p_r(X)=sum x_i^r+(-1)^(r-1)sum y_i^r. Tensor alphabet T has even xu,yv and odd xv,yu. F=hs_nu(T)=sum g(rho,sigma,nu)hs_rho(X)hs_sigma(Z), with surviving shapes in(a,a)/(b,b) hooks. This identity, ordinary g, hook vanishing and independence are already checked. Hence if Durfee(nu)>2ab, F=0 and g=0; otherwise c=Durfee(nu)<=2ab is fixed. For n=0 output1; reject inconsistent input sizes by exact binary sums.

NEW SINGLE COEFFICIENT: Q_X=prod_(i,j)(x_i+y_j), Q_Z similarly. Delta(x)=prod_(i<j)(x_i-x_j), and similarly y,u,v. Expand each Q_X inverse as prod_i x_i^(-a)*prod_(i,j) sum_(k>=0)(-y_j/x_i)^k, and similarly Q_Z about u. Let alpha_i=lambda_i-i, beta_j=lambda'_j-j be lambda's Frobenius arms/legs, gamma/delta those of mu. Proposed exact formula:
 g(lambda,mu,nu) = [x^alpha y^beta u^gamma v^delta]
   F * Delta(x)Delta(y)Delta(u)Delta(v)/(Q_X Q_Z).

Reason: a surviving rho of Durfee EXACTLY a contains the a-by-a rectangle and hs_rho(X)=Q_X*s_(rho_i-a)(x)*s_(rho'_j-a)(y). Multiplying both Vandermondes yields two alternants with exponents rho_i-i and rho'_j-j; the fixed strictly descending nonnegative target can match only rho=lambda, coefficient+1. If Durfee(rho)<a, use hs_rho=sum_kappa s_kappa(x)s_(rho'/kappa')(y), kappa subset rho and len(kappa)<=a. Every such kappa has kappa_a<a. Delta(x)s_kappa is an alternant with at least one exponent<a. Q_X inverse shifts every x exponent by -a and then only DECREASES x exponents, so every resulting monomial retains at least one negative x exponent; it cannot contribute to the target. Delta(y) does not change x. This is a formal-chamber claim needing careful scrutiny, not a numerical rational-function expansion. Same for Z. No full basis enumeration.

NEW FINITE RATIONAL COMPILER: use Giambelli for nu in c fixed Frobenius rows:
 hs_nu(T)=det(hs_(r_i+1,1^(s_j))(T))_(i,j<=c).
Expand only c! terms, a constant depending on d,e. Give every selected hook its own auxiliary t_j,w_j. The hook generating identity is
 sum_(r,s>=0) hs_(r+1,1^s)(T) t^r w^s = (H_T(t) E_T(w)-1)/(t+w),
where H_T(t)=prod_odd(1+z*t)/prod_even(1-z*t), E_T(w)=1/H_T(-w)=prod_even(1+z*w)/prod_odd(1-z*w).
For coefficient t^r w^s with r,s>=0 one may use H_T(t)E_T(w)/(t+w), expanding 1/(t+w)=t^(-1)sum_(j>=0)(-w/t)^j; the subtracted1 has only negative t degree. Hooks have independent auxiliary variables, so no leakage between hook factors.

After multiplying by Vandermondes/Q_X/Q_Z, expand constant-size numerators and determinant permutations. Each resulting rational term is a Laurent monomial times a product of a FIXED number of factors(1-epsilon*z^v)^(-1), with integer exponent vectors v of fixed dimension and epsilon=+/-1. Target exponents are binary Frobenius coordinates. No numerator is expanded to numerical degree n.

CRITICAL FINITENESS: claim every contributing geometric occupation is <=n. Hook j consumes auxiliary w-degree, so j<=s_j<=n. The H even-denominator occupancies sum to at most r_i+j+1<=r_i+s_j+1<=n; E odd-denominator occupancies sum to <=s_j<=n. Numerator contributions have nonnegative t,w degrees. Each Q_X geometric variable increases a y exponent; all other sources have nonnegative y exponents, including Delta(y), so its value<=target beta_j<=n; similarly v. Negative x/u/t shifts do not create an unbounded cycle. This must be proved term by term, not from cancellation after an infinite expansion. Auxiliary hook cell r_i+s_j+1 can exceed n for off-diagonal Giambelli pairs? CHECK THIS: if so use a uniform 2n+O_de(1) box instead, with binary sizeO(log n). A valid explicit O_de(n) box is sufficient.

For each rational term write all exponent matching equations A k=b with 0<=k<=C_de*n+C_de. Deal with (-1)^k by enumerating parity of the fixed number of signed indices and substituting k=2z+epsilon (constant number of branches). Each branch is an explicit bounded rational polytope in a fixed number D_de of variables; entries of A are fixed small integers, right sides have O(L) bits. Count its integer points using the actual fixed-dimensional algorithm; sum with the known signs. Equality constraints can be two inequalities or removed by paid Smith form. Need account empty/lower-dimensional polytopes. Counts are <=(C_de*n+C_de+1)^D_de, so output/intermediate bitsO_de(log(n+1)); all lists/branches depend only on fixed d,e. Full uniform algorithm generates its fixed matrices from d,e, not hidden advice.

Required result: prove/refute this complete binary-input compiler, with every formal-series coefficient, variable bound, source hypothesis, output and bit cost. No extension to growing Durfee, no claimed new quantum algorithm, no novelty/priority claim. Standard fixed-dimensional integer counting is a classical baseline, not a free oracle. Supplied actual source excerpts retain URLs/hashes/physical LF locators.

STATUS: proposed new compact-input proof; independent review and exact coefficient control pending.


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
bits. These are derived bounds, still under independent audit.
