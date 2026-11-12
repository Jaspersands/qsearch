# Native real-time Macdonald dynamics from few bosons

Reviewed WRITTEN classical algorithm. Numerical D>=1, global
q=t^3,t=D/(D+1), explicit occupation mu with k=length(mu) bosons, rational
time2pi*a/c of bit length L, target TV2^-b. Claim established: a complete
classical full-occupation sampler in (D+1)^O(k)poly(D,L,b) BIT time. Hence
EVERY fixed k is polynomial. This is a constructive classical competitor,
not an obstruction to arbitrary growing-k inputs or a speedup claim.
No physical-position interpretation or finite-size inference is used.

## 1. Exact k-boson spectral support from a multivariate zero

Actual Atai--Hallnas--Langmann2021, DOI10.1007/s00220-021-04166-z,
Eq31-34 and Lemma2 proof Eq39: the algebra homomorphism

 phi_(n,m)(p_r)=sum_(i=1)^n x_i^r - s_r sum_(j=1)^m y_j^r,
 s_r=(q^(r/2)-q^(-r/2))/(t^(r/2)-t^(-r/2))

maps P_lambda to the super-Macdonald polynomial. It vanishes identically
outside H_(n,m)={lambda:lambda_(n+1)<=m}. We need only vanishing, not the
stronger nonzero/basis theorem or a quantum position-space interpretation.
The vanishing also follows directly from the source's coproduct/duality
proof: expand in P_(lambda/nu')(x) Q_nu(y;t,q). A surviving Q_nu in m
variables requires length(nu)<=m, so nu' has width<=m. If column m+1 of
lambda has height>n, it remains intact in lambda/nu' and cannot be filled
by n horizontal strips. Thus the skew factor in n variables vanishes.
This uses finite positive-parameter skew/Pieri identities; no generic
spectrum gap or unverified special-parameter limit. All P/hook factors are
regular by positive-Gram continuation on 0<q,t<1.

At q=t^3, s_r=t^(-r)+1+t^r. Take n=3k,m=k and set

 (x_(3j-2),x_(3j-1),x_(3j))=(z_j/t,z_j,t*z_j),
 y_j=z_j+epsilon_j,  j=1,...,k.

Then phi(p_r)=-s_r sum_j[(z_j+epsilon_j)^r-z_j^r].
Every summand depends on only ONE epsilon_j and has zero constant term.
Consequently [epsilon_1...epsilon_k]phi(p_rho) is zero unless
length(rho)=k: more factors have degree>k; fewer factors cannot cover all
k distinct epsilon variables. For length(rho)=k it equals

 (-1)^k (prod_(r in rho) r*s_r)
        sum_(bijections of the k labelled factors to j) prod_j z_j^(r_j-1).

For repeated parts, the last sum is prod_a m_a(rho)! times the monomial
symmetric polynomial m_(rho_1-1,...,rho_k-1)(z_1,...,z_k), retaining zero
exponents. Distinct length-k partitions rho give distinct monomial
symmetric polynomials. Each prefactor is nonzero for0<t<1.

If lambda_(3k+1)>k, phi(P_lambda)=0 identically. Its displayed multivariate
coefficient therefore proves, INDIVIDUALLY for every rho of length k,

 [p_rho]P_lambda=0.                                           (A)

No cancellation among different rho can hide in this independent basis.
This is stronger than a univariate principal-specialization zero, which
would not prove (A). It agrees with the one-boson lambda_4<=1 control.
Since J is a nonzero scalar multiple of P, (A) gives the exact support of
p_mu in the orthogonal Macdonald basis: it is contained in H_(3k,k).
Only containment is claimed; some in-hook coefficients can also vanish.

Every subpartition of such a lambda stays in the same hook. All diagrams
of degree<=D inside H_(3k,k) can be enumerated by their first3k row lengths
and the k column heights BELOW these rows. Thus their total number M is
at most (D+1)^(4k), and enumeration costs that bound times poly(D).
Validate monotonicity and total degree; no full p(D) table is traversed.
For3k>D or k>D use the same overcount/fallback; fixed-k claim unchanged.

## 2. A sampler for an explicitly represented finite down-set state

This construction also extends bounded-Durfee eigenstate sampling to this
Macdonald family; its purpose is to pay the few-boson dynamics output.
Let S be an explicitly enumerated finite down-set of partitions of degree<=D,
size M. General coefficient vectors must be supplied as rational complex
numbers, with their total bit length charged; mere computability is not an
efficient input interface. The native phase-rounded vector below is computed
within the stated bound and meets this requirement. Work
in the monic orthogonal P_nu basis, with explicit rational positive norms

 h_nu=<P_nu,P_nu>=prod_(boxes) (1-q^(a+1)t^l)/(1-q^a t^(l+1)).

Norms are computed by hooks, not supplied as an oracle. Define Macdonald
row functions g_n=Q_(n) through

 g(z)=sum_(n>=0)g_n z^n=exp(sum_(r>=1)p_r z^r/(r*r_r)),
 r_r=(1-q^r)/(1-t^r)=1+t^r+t^(2r).

These g_n are DISTINCT from the Hall--Littlewood vertex V_n in the
Hamiltonian. Actual Borodin--Corwin Eqs2.10--2.11 gives multiplication
G_n by g_n in the P basis as a horizontal-strip Pieri matrix. Its entries
are finite positive rationals: pair f(q^a t^c)/f(q^b t^c), use
f(qu)/f(u)=(1-qu)/(1-tu), and telescope O(D) shifts per pair. For each
pair a,b,c>=0, all factors at q=t^3 are1-t^e, e positive O(D). Index j+1
is a partition index, not arithmetic +1. This was checked in the prior
272line classical audit. Enumerate every retained pair and test the strip;
all entries and hook norms have polynomial(D)-bit length.

Restricted raising products are exact between endpoints in S: every
intermediate shape is contained in the final endpoint. A path leaving a
down-set cannot return. Let T_n=diag(h)^(-1) G_n^T diag(h); it is exactly
g_n^dagger on S and preserves S. Newton's generating-series identity gives
native matrices D_r for p_r^dagger:

 D_1=r_1*T_1,
 D_r=r*r_r*T_r-r_r*sum_(i=1)^(r-1) D_i*T_(r-i)/r_i.           (B)

All lowerings commute on this invariant S. This recursion costs at most
poly(D)*M^3 rational operations; no sparsity or tight exponent is needed.
It pays arbitrary mode derivatives without a coefficient oracle.

For homogeneous nonzero f=sum_nu v_nu P_nu of degree d,

 p_r^dagger=r*r_r partial_(p_r),
 sum_(r=1)^d ||D_r f||^2/r_r = d ||f||^2.                   (C)

At each step choose r with probability ||D_r f||^2/(r_r*d*||f||^2), replace
f by D_r f WITHOUT numerical normalization, and lower d by r. At most D
steps occur. In normalized occupation basis D_r removes a part r with
amplitude sqrt(r*r_r*m_r). The map on labels is injective for fixed r.
Hence this procedure is exactly size-biased deletion from the occupation
Born law; the recorded multiset has the correct full output distribution.
All coherent signs and complex cross terms survive in v before squaring
with the positive diagonal norms h. No mixture of eigenstate Born laws.

## 3. Native initial coefficients and real-time phases

Take S=all degree<=D shapes of H_(3k,k). Compute (B) and norms. For every
lambda in S of degree D, compute the vacuum coefficient

 c_lambda=(D_(mu_1)...D_(mu_k) P_lambda)_empty / h_lambda.

Adjointness gives exactly c_lambda=<P_lambda,p_mu>/h_lambda, so by (A)
p_mu=sum_lambda c_lambda P_lambda, with no missing component. All these
numbers are exact rationals computable from the already constructed
matrices; no coefficient/advice table is supplied. The known initial norm
is R_mu=z_mu prod r_r^m_r. This identity can be used as a consistency check,
but the all-D proof is adjointness plus support, not such a finite check.

Compute E_lambda=sum_i(q^(-lambda_i)-1)t^(i-1) exactly, multiply a/c,
reduce modulo1 exactly, and approximate exp(-2pi*i*a*E_lambda/c) by a
dyadic complex number z_lambda to absolute delta<=2^(-b-5). Take
v_lambda=c_lambda*z_lambda, and sample using (C). The ideal and approximate
state vectors differ in norm by at most delta*sqrt(R_mu), by orthogonality.
Normalizing the approximate vector changes the bound to <=2delta; its
Born law is within2delta in TV. This estimate is dimension-independent.
Phases do not require precision proportional to numerical |a/c|: rational
modulo reduction is exact and polynomial in its binary length L.

Use B'=b+ceil(log2(8D^2+8)) fair bits at each CDF draw, compare to EXACT
rational cumulative probabilities, and skip empty intervals. Coupling to
continuous uniforms bounds total sampling error by D^2*2^(-B'). Together
with phase approximation this is less than2^-b. No inverse-small-norm
precision or expected unbounded rejection clock is hidden in this scheme.

## 4. Rational heights and whole BIT clock

A coarse uniform denominator suffices. Let B0 be the product of numerators
and denominators of1-t^e for1<=e<=8D, all r_i fori<=D, and all integers
1,...,D, omitting zero. Its bit length is polynomial(D). The exact constant
8 can be increased if a Pieri indexing bound needs it; no optimization
is claimed. Every Pieri/hook factor is in this finite set or its inverse.
O(D^3) such factors suffice per entry. Thus all T_n entries have denominator
dividing B0^poly(D), and magnitude at most2^poly(D). Recursion(B), with
at most D multiplication depth, preserves these bounds up to a polynomial
power and polynomially many log(M) bits from sums. A derivative history
has at most D steps; candidate vectors use at most D+1. All denominators
therefore divide B0^poly(D) times the initial dyadic phase denominator.
Their numerator lengths are poly(D,log M,L,b). Norms and probabilities
have the same type of bound. Exact small nonzero norms are legal rationals;
no numerical zero test is needed. D0 is the vacuum case.

This proves poly(D,M,L,b) BIT cost once the displayed finite-source and
algebraic claims are verified. With M<=(D+1)^(4k), it gives the proposed
(D+1)^O(k) poly(D,L,b) classical sampler for the SAME full native output.
For an eigenstate labelled by lambda with Durfee h, S=all subpartitions of
lambda has M<=(D+1)^(2h), yielding the analogous bounded-Durfee baseline.
Neither statement supplies an unrestricted growing-k or growing-h sampler.

## Review and implementation boundary

No quantum implementation or large sweep is proposed. Independent review
must attack (A), the monic Pieri normalization and finite factor ranges,
(B)/(C), native coefficient extraction, phase/modulo and the uniform bit
clock. Only a concrete small exact CAS identity check is appropriate.
The four paid dynamics reports are independent and still advisory/in flight;
this parent derivation does not depend on their conclusions.

## Closed proof and scoped exact control

Parent fully read/checked all272LF lines of
audits/reviews/2026-11-13-macdonald-few-phonon-independent.md. Source
vanishing, multivariate coefficient independence, all retained operators,
initial amplitudes, complex interference, exact phase arithmetic and
unnormalized-history BIT bounds are accepted. The proof's log-series
expansion bounds heights only; the actual algorithm uses the polynomial
Newton recurrence. Generic input coefficients require a charged explicit
representation, clarified above. Fixed-k and bounded-Durfee claims CLOSED
at this exact written scope. Growing k/h remains OPEN.

One exact Sage normalization fixture atD3 passed171 assertions, including
147 Newton/direct-derivative matrix entries and the coherent Euler norm
identity. Parent inspected script and receipt under
audits/controls/macdonald_newton_degree3/. Sage native Macdonald conversion
required generic rational-function conversion followed by evaluation due
to a rational-specialization API TypeError. This is an independent local
normalization falsifier only; no all-D theorem follows from passing it.

## Both terminal OpenAI reports: checked dispositions

Parent read all573LF lines of dynamics-few-phonon. Its independent proof
uses Cauchy plus vertical Pieri to establish phi_(u,v)(P_lambda)=0 outside
lambda_(u+1)<=v, where phi(p_n)=p_n(X)-r_n p_n(Y). Atq=t³ take the X
triples(x,tx,t²x), set x=y+epsilon and extract epsilon1...epsilonk. The
coefficient is exactly R_mu times the monomial symmetric polynomial of
mu-minus-one, proving the same support without a new source assumption.
Its monic norm ratios psi/phi, adjoint row matrices and Newton annihilators
are consistent with the parent construction. Whole fixed-k sampler accepted
at poly(D,M,L,b) BIT scope; no need adopt tighter operation exponents.

The report also proves a sharp coefficient statement. For nonempty lambda,
rho(lambda)=#{zero-based boxes(i,j):i=3j}=min{k>=1:lambda_(3k+1)<=k}.
The individual support theorem kills all power-sum lengths<rho. Principal
specialization has an EXACT order-rho zero atv1; therefore SOME coefficient
of lengthrho is nonzero. This is a valid existential nonvanishing argument,
not the invalid converse that a univariate zero kills each coefficient.

Parent read all526LF lines of dynamics-direct-sampler. It does not solve
unrestricted sampling. Its alternative complete fixed-k method uses the
span of products of3k Macdonald rows andk elementary columns, which equals
the fat-hook space by a triangular positive-Pieri argument. A two-copy
generating-function Gram kernel computes prefix occupation weights with
ALL cross terms. Native vertex action supplies the restricted Hamiltonian;
exact rational eigenspaces (coincident energies grouped) and phase modulo1
pay dynamics. This is consistent with the simpler verified derivative
sampler; no second implementation is needed. Retain only its safe generic
poly(D,M,L,b) cost, not unnecessary tight bounds.

Both degree2 interference controls check: native t2/3,q8/27 gives
P_(2),tau(11)=(133/169) sin²(1235*pi*tau/192), whereas dephasing gives
133/338. At tau192/1235 the coherent transition is zero. This is a scoped
shortcut falsifier, not evidence of hardness. General condensate p1^D has
strictly positive spectral overlap with EVERY shape by one-box Pieri, so
a fixed hook cannot cover all inputs. The full conditional projector
rankp(D)-p(D-1) similarly excludes only a universal low-rank factorization;
a structured high-rank contraction remains possible. No rank experiment,
new sweep or full conditional-array implementation is queued.
