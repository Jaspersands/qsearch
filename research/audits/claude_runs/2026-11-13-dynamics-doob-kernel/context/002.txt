# Macdonald classical baselines: parent proofs and report dispositions

Contract: numericalD, t=D/(D+1),q=t³, unrestricted labelled lambda; occupation
Born law, no coefficient advice. Claude classical13261bytes/215lines and
branching11204bytes/162lines fully parent-read. Both terminal/reaped. No
unrestricted polynomial classical sampler found; no hardness inferred.

## Native source/regularity repairs

Actual Borodin--Corwin1111.4408v4 Sections2.1.3-2.1.6 read, including
physicalPDFpage35/rendered printedpage33 to resolve subscript j+1 in
Pieri Eqs2.10-2.11. Local source borodin_corwin_2014.pdf/txt has actual
arXivv4 header; the filename is merely a label, not version authority.
For fixed degree the Hall Gram matrix is positive definite and analytic
on0<q,t<1. Gram--Schmidt in a fixed total order extending dominance thus
has nonzero positive Gram determinants and analytic coefficients. Generically
it equals the triangular orthogonal Macdonald P basis, hence supplies its
regular continuation at q=t³. Multiplying by the finite positive hook
product gives regular J. The branching report's unchecked integrality
citation is NOT needed. This is an existence/regularity proof, not a claimed
polynomial full Gram--Schmidt algorithm. Coincident spectral eigenvalues
are not a reason to divide by spectral gaps here.

## Exact row/column laws

Let r_k=1+t^k+t^(2k). Row law has cycle weights w_k=1/r_k, column w_k=r_k;
pi(mu)=Z_D^-1 prod_k w_k^m_k/(k^m_k m_k!). Z0=1 and
n Z_n=sum_k w_k Z_(n-k). Size-biased sequential choice k with probability
w_k Z_(n-k)/(n Z_n) gives the partition law. Exact expected rational random
sampling or bounded finite-bit TV<=2^-b costs poly(D,b).

The generating-series functional equation proves (no infinite-product
oracle) Z_n^row=(t;q)_n/(q;q)_n and Z_n^col=(q;t)_n/(t;t)_n. For example,
G(qx)/G(x)=(1-x)/(1-tx) gives
(1-q^n)Z_n=(1-t q^(n-1))Z_(n-1). Columns are complete homogeneous
functions of the THREE letters1,t,t², not an unknown normalization.

Actual sourceEq2.3-2.4 and hook transposition imply omega_qt J_lambda(q,t)
=J_lambda'(t,q). Since omega p_k=(-1)^(k-1)r_k p_k is an isometry between
the two Hall forms, the occupation laws of these conjugate inputs are
identical. This transfers any valid near-row sampler to near columns.

## Reviewed near-row and near-column classical sampler

For D>=2s, shapes kappa with kappa1>=D-s are in bijection with
(j,rho),0<=j<=s,rho partition j, via kappa=(D-j,rho). Their span equals
span{g_(D-j) P_rho: j<=s}. Actual horizontal-strip Pieri gives this:
if kappa/rho is horizontal of size m=D-j, interlacing yields
sum_(i>=2)(kappa_i-rho_i)<=rho1, so kappa1>=m. Equality forces
kappa=(m,rho), and its coefficient is strictly positive. Ordering j
therefore gives an invertible triangular matrix of dimension sum_j p(j).

Source Pieri products are computable finite rationals: f(u)=(tu;q)_inf/
(qu;q)_inf obeys f(qu)/f(u)=(1-qu)/(1-tu). In Eq2.10 pair factors with
the same t^(j-i); q-exponent differences are integers of sizeO(D), so
all infinite products telescope to polynomially many finite factors. For
horizontal strips, all starting arguments are q^a t^c with a,c>=0;
no poles/zeros arise at q=t³. Source subscript j+1 is an INDEX, not an
added exponent one. Every finite factor is1-t^e with e positiveO(D).

Solve for a target near-row P_lambda in this basis, expand only low-degree
P_rho, and obtain f=sum_(j<=s) g_(D-j) h_j, h_j degreej. For any mu,

 [p_mu]f * z_mu prod r_k^m_k = Phi(m1,...,ms),
 Phi=sum_(beta: |beta|<=s) c_beta prod_k r_k^b_k k^b_k (m_k)_(b_k).

Thus target probability is the row law tilted by Phi². Enumerate the
at-most(D+1)^s vectors(m1,...,ms) and weight each by
Phi² prod_(k<=s)(w_k/k)^m_k/m_k! * Z_(D-sum k m_k)^(parts>s).
The last coefficient uses a restricted cycle DP. Sample this vector, then
complete large parts with the same restricted DP. This gives D^O(s)poly(D,b)
BIT sampling for fixed s, with no target Jack/Macdonald coefficient oracle.
All matrix/table sizes and rational bit costs are charged. For D<2s,
exhaustive p(D) computation already fits D^O(s). No claim is made that this
covers growing balanced shapes polynomially. A signed poly-sparse input
superposition additionally requires explicitly supplied amplitudes and
precision; fixed-label sampling alone does not grant arbitrary input access.

## Elementary uniform separation from the Jack row law

This replaces the paid report's unverified Poisson--Dirichlet proof sketch.
It uses only exact finite weighted-cycle identities, no limit theorem.
Let Q_D be the Jack row Ewens law with theta=1/3, and P_D the deformed row.
Put h=log(1+1/D), u=hD in[1/2,1],
 g(x)=log((1+2cosh x)/3), G(mu)=sum_parts g(hk).
The likelihood ratio is EXACTLY L=P_D/Q_D=e^-G/E_Q[e^-G], since the
linear contribution sum hk=hD cancels. g(0)=g'(0)=0 and
 g''(x)=(2cosh x+4)/(1+2cosh x)^2.
For0<=x<=1, cosh1<8/5 implies50/147<=g''(x)<=2/3, hence
 (25/147)x²<=g(x)<=x²/3. Convexity also gives sum g(x_i)<=g(sum x_i).

For D>=200, event A is a cycle with length in[.90D,.91D], and event B is
two cycles with lengths in[.40D,.41D]. There cannot be two A cycles or
three B-range cycles. On A, G>=g(.90u); on B,
G<=2g(.41u)+g(.20u), because remaining total length<=.20D. Therefore

 G_A-G_B >= [27/196-627/5000]u²
            =3027u²/245000 >=delta0:=3027/980000.

Each integer interval has at leastD/200 entries. Under Ewens, exact
factorial moments are
 E m_k=theta Z_(D-k)/(k Z_D),
 E[m_k(m_l-1{k=l})]=theta² Z_(D-k-l)/(kl Z_D).
Z_n=(theta)_n/n! decreases in n, so every displayed Z-ratio>=1.
Consequently Q_D(A)>=1/600 and Q_D(B)>=1/720000. The latter is half
the ordered double factorial-moment sum, valid also for k=l.
Since G_B upper bound<=627/5000<1/2, the possible L values on B are
separated above those on A by at leastdelta0/4 (normalizer<=1).
Relative to1, one event must have |L-1|>=delta0/8. Thus, for EVERY D>=200,

 TV(P_D,Q_D)>=delta0/(16*720000)>0.

The constant is intentionally tiny; it proves uniform inverse-polynomial
TV approximation by the Jack law fails, while BOTH row laws are classical
polynomial. It is neither a quantum advantage nor a generic hardness result.
No finite scan or external asymptotic assumption supports this deduction.

## Other paid-claim dispositions

The three-colour Hall lift is an exact isometry and simply adds independent
part colours conditional on the original sample. It is not a paid Schur
preparation/sampler. Its displayed skew expansion misses the overall
integral-form scalar, and disjoint support is sufficient, NOT necessary,
for a tractable mixture/contraction. Do not promote that as a no-go.

The single-cycle coefficient formula follows directly from the ACTUAL
Mickler sourceTheorem4.1, without an unchecked book citation: specialize
p_k=(1-v^k)/(1-t^k), divide by1-v, letv->1. Only the p_D term survives.
Hence [p_D]J=(1-t^D)/D *prod_nonorigin(t^i-q^j). At q=t³ it vanishes iff
lambda4>=2, because the first nonoriginzero is(i,j)=(3,1). This is one
coefficient, not a sampler. Parent checked the report's lambda21 coefficients
algebraically; no extra sweep is needed.

Derivative-norm identities are valid, but their general iterates encode
the original law. No complete compact recurrence is supplied. Do NOT run
the suggested D<=30 sweep or continue another nearby moment barrier; it
would not decide a full algorithm. 'No formula found' never closes all
classical methods. Exact gate/bit exponents and the broad 'strictly weaker'
complexity assertion about fixed-label versus arbitrary superpositions are
not adopted. Distinct input models have been kept explicit.

## Independent proof disposition

Parent checked all272 LF lines of audits/reviews/2026-11-13-macdonald-
classical-independent.md. Near-row/column bounded-clock BIT sampling and
the uniform finite-D TV floor are accepted with their exact scope. The
common denominator for Phi includes the r_k powers, not only the c_beta
denominators. Finite-CDF rounding charges every table boundary. No
Poisson--Dirichlet limit or general hardness inference is used.
