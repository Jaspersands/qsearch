# 2026-11-13 — Independent few-phonon real-time Macdonald audit

**The native fixed-k claim is valid.** From a supplied occupation partition
mu of numerical size D and length k, at global t=D/(D+1), q=t^3, the FULL
occupation law after native NS time 2pi*a/c has a classical sampler of fixed
BIT clock (D+1)^O(k) poly(D,L,b), with TV error at most 2^(-b). Here L is the
binary rational-time input length. No spectral coefficients, eigenvectors,
state preparations or conditional-probability oracle are supplied.

There is one scope clarification: the generic down-set routine is polynomial
in the bit length of an EXPLICIT complex rational coefficient vector, or in
an explicitly charged approximation interface. Unqualified 'any computable
superposition' supplies no complexity bound. The native dynamics below
constructs exactly the required polynomial-bit dyadic-phase vector, so this
clarification does not weaken the fixed-k theorem. Arbitrary signs and
coherence in that vector are fully retained.

Read: current STATE/TRAPS, MACDONALD_FEW_PHONON_CLASSICAL, the exact native
real-time contract, and the earlier independently checked BC Pieri audit.
The newly retained Atai–Hallnas–Langmann text was present and stable across
two reads (122788 bytes, 2001 LF lines). Actual Eqs. (31)–(39), Lemma 2 proof
and Appendix C.2 were read, as were its Hall norm conventions. No in-flight
paid report, network, API, Git, implementation or numerical extrapolation
was used. Only this review was written.

## 1. The source vanishing is valid at the native specialization

Actual source LF 440–497 defines the algebra homomorphism

    phi_(n,m)(p_r)=sum_i x_i^r-s_r sum_j y_j^r,
    s_r=(q^(r/2)-q^(-r/2))/(t^(r/2)-t^(-r/2)),

and states vanishing outside H_(n,m)={lambda:lambda_(n+1)<=m}.
The required implication also follows directly from the unrestricted
coproduct identity in the PROOF of Lemma 2, LF 513–531:

    phi(P_lambda)=sum_(nu subset lambda')
       (-q^(-1/2)t^(1/2))^|nu| P_(lambda/nu')(x;q,t) Q_nu(y;t,q).

If length(nu)>m, the Q factor in m variables is zero. Otherwise nu' has
width at most m. If lambda_(n+1)>m, column m+1 of lambda has height >n,
and that column is untouched by nu'. The skew factor therefore vanishes
in n variables. This is precisely the column-height criterion proved in
source Appendix C.2, LF 1687–1708 (or follows from n horizontal-strip
branching steps). Thus every summand is zero.

This reasoning does not require the 'nonzero inside the hook' direction,
a nondegenerate spectrum or a generic-parameter limit. All parameters lie
in 0<q,t<1, where the source's positive Hall product and finite Pieri formulas
are regular. Its Remark 2 also explicitly permits this domain. We use this
source only for symmetric-function identities; its physical torus Hilbert
space and its differently normalized Hamiltonian are not substituted for
the native Hall-Fock NS input/output contract.

## 2. Multivariate extraction proves INDIVIDUAL length-k support

At q=t^3, s_r=t^(-r)+1+t^r. Choose n=3k,m=k and substitute

    (x_(3j-2),x_(3j-1),x_(3j))=(z_j/t,z_j,t z_j),
    y_j=z_j+epsilon_j.

Then phi(p_r)=-s_r sum_j[(z_j+epsilon_j)^r-z_j^r]. Each summand has positive
epsilon degree and involves only ONE epsilon variable. In a product p_rho:
more than k factors cannot contribute to epsilon_1...epsilon_k, while fewer
than k cannot cover its k distinct variables. Hence only length(rho)=k
survives. For that length the coefficient is exactly

    (-1)^k product_(r in rho)(r s_r)
       * sum_(bijections of labelled factors to j) product_j z_j^(r_j-1).

If parts repeat, the sum is

    product_a m_a(rho)! * m_(rho_1-1,...,rho_k-1)(z_1,...,z_k).

Zero exponents MUST be retained among the k positions. In particular the
factor m_1(rho)! accounts for their repetitions. Subtracting one from all
k positive parts is a bijection with partitions of D-k of length at most k,
padded by zeros. These monomial symmetric polynomials in k variables are
linearly independent. Every scalar prefactor is nonzero.

For lambda outside H_(3k,k), the entire specialized phi(P_lambda) is zero
by §1. Its displayed coefficient therefore forces, separately for EVERY
rho of length k,

    [p_rho]P_lambda=0.

There is no cancellation between different rho in this conclusion. Since
p_rho are Hall-orthogonal, the spectral expansion of the native p_mu has
support contained in H_(3k,k). Integral J differs by a nonzero scalar and
has the same conclusion. Only containment is claimed.

This hook is a down-set. A diagram of degree <=D in it is determined by
its first 3k row lengths and its k column heights BELOW those rows.
Each coordinate is in {0,...,D}. Enumerating these tuples, validating the
partition and total size, therefore lists the whole down-set S in
(D+1)^(4k) poly(D) time, with size M<=(D+1)^(4k). The count already includes
all degrees <=D. When 3k>D the same enumeration bound remains valid; no
full partition table is secretly traversed. For a nonempty input k<=D.

## 3. Exact native matrices in the monic P basis

Retain the GLOBAL input q,t at every smaller degree. Source Hall norms are

    h_lambda=<P_lambda,P_lambda>
       =product_b (1-q^(a(b)+1)t^l(b))/(1-q^a(b)t^(l(b)+1)) >0.

They are native rational hook products. The row functions needed here are

    g_n=Q_(n),
    sum_n g_n z^n=exp(sum_(r>=1) p_r z^r/(r r_r)),
    r_r=(1-q^r)/(1-t^r).

Although the COORDINATE basis P is monic, g_n is Q_(n), not P_(n).
It is also not the Hall–Littlewood vertex V_n in the NS Hamiltonian.
Using either wrong normalization would invalidate the Newton matrices.

Let G_n[lambda,nu] be the actual horizontal-strip coefficient for
P_nu g_n, with both endpoints in S. It is computed from BC (2.10).
Pair f(q^a t^c)/f(q^b t^c) using f(qu)/f(u)=(1-qu)/(1-tu).
For a horizontal strip the relevant exponents
lambda_i-lambda_j, nu_i-nu_(j+1), lambda_i-nu_j,
nu_i-lambda_(j+1) are all nonnegative. The j+1 symbols are indices.
All shift factors specialize to ratios of 1-t^e with 1<=e<=8D;
in fact the preceding exponent bounds give e<4D+3. There are O(D^3)
factors per matrix entry, so their BIT generation is polynomial in D.
The previous audit's finite-factor proof applies to all strip endpoints,
not only near-row shapes.

With H=diag(h_lambda), set T_n=H^(-1) G_n^T H. Then T_n is exactly g_n^dagger
on S. Indeed its outputs are subpartitions of its input, all retained in
this down-set. No omitted raising path can leave S and later return to an
endpoint in S. The lowering operators commute because the full g_n^dagger
do and S is invariant.

Differentiating the generating series and taking adjoints gives

    D_1=r_1 T_1,
    D_r=r r_r T_r-r_r sum_(i=1)^(r-1) D_i T_(r-i)/r_i.

Thus D_r is exactly p_r^dagger=r r_r partial_(p_r). This pays every mode
lowering with O(poly(D) M^3) rational operations. There is no Macdonald
coefficient oracle, Gram diagonalization or hidden basis conversion.

## 4. Rational heights: why the derivative clock is uniform

Define B0 to be the product of the positive integer numerators and
denominators of 1-t^e, 1<=e<=8D; of r_i, i<=D; and of 1,...,D.
It has O(D^2 log(D+1)) bits. The endpoint factor bounds above and the hook
products imply, for a fixed polynomial A(D), that every T_n entry has
denominator dividing B0^A and absolute value at most (D+1)^A.
For example an enlarged A=32(D+1)^3 safely suffices. All entries are built
without approximating an infinite product.

A useful nonrecursive height certificate is the formal logarithm identity

    D_r=r r_r sum_(ell=1)^r (-1)^(ell-1)/ell
                * sum_(n_1+...+n_ell=r, n_i>=1) T_(n_1)...T_(n_ell).

We use this to BOUND heights, not to enumerate its 2^(r-1) terms. Each
monomial has at most r factors, its coefficient denominator divides B0^2,
and matrix multiplication introduces at most M^(r-1) paths. Consequently
D_r entries have denominator dividing B0^(r A+2), with numerator bit length
polynomial in D and log M. The displayed Newton recurrence computes them
in polynomially many matrix operations without that expansion.

More strongly, a derivative history D_(r_j)...D_(r_1) has sum r_i<=D.
Its total denominator exponent is at most D A+2D, and its absolute-entry
growth has logarithm O(D A log(D+1)+D log M+D log D). Adding
(D A+2D) log2(B0) bounds the numerator bits as well. This also bounds
candidate next derivatives, since only r<=the remaining degree is tested. It gives
uniform bounds over every possible sampled history, not just typical ones.

The initial coefficients below come from another degree-D derivative
product and division by one h_lambda, so they obey the same polynomial
height bound. Multiplying by a common dyadic phase approximation adds its
bit precision. Every later unnormalized vector therefore has numerator
and denominator lengths poly(D,log M,b); computing phases additionally
costs poly(L). Norms sum h_lambda|v_lambda|^2 and have the same type of bit
bound. Their quotients in probabilities can have new denominator primes,
but still polynomial bit lengths. Crucially those quotients NEVER feed
back into the vector: no conditional numerical normalization is performed.
Thus exact very small norms create neither extra precision nor growing
arithmetic ancestry. Zero is decided exactly.

## 5. A sampler for coherent rational down-set vectors

For a nonzero homogeneous f=sum_lambda v_lambda P_lambda of degree d,
allow arbitrary explicitly represented complex rational coefficients.
Then

    sum_(r=1)^d ||D_r f||^2/r_r = d ||f||^2.

In the normalized occupation basis D_r sends mu to mu minus one r-part
with amplitude sqrt(r r_r m_r(mu)). For fixed r this label map is injective.
Thus the identity holds termwise, including arbitrary coherent input
superpositions. In P coordinates all cancellations are performed in D_r v
before taking its positive diagonal-H norm; this is not an incoherent
mixture of eigenstate distributions.

Choose r with probability ||D_r f||^2/(r_r d ||f||^2), record r, and replace
f by D_r f WITHOUT normalization. The exact occupation distribution of
this conditional state is the distribution after size-biased deletion of
an r-part from the original Born sample. Induction therefore shows that
the complete recorded multiset has exactly the original full occupation
Born law. Degree decreases by r>=1, so there are at most D draws.
Candidate zero norms give empty intervals and are never chosen.

All vectors, norms and conditional probabilities are exact rationals
(complex rationals for vectors), so §4 applies to every history. An
arbitrary nonzero input rational vector of coefficient bit length B would
add polynomial dependence on B. Merely calling its amplitudes 'computable'
would not supply that interface. The next section constructs it natively.

## 6. Initial coefficients, long-time phases and deterministic TV budget

For every degree-D lambda in S, let

    c_lambda=(D_(mu_1)...D_(mu_k) P_lambda)_empty / h_lambda.

Adjointness gives this real rational as the coefficient of P_lambda in
p_mu. Repeated parts contribute their factorials through the iterated
derivatives; there is no extra division by k!. Section 2 proves there are
no omitted spectral components. These coefficients are obtained from the already computed matrices, including
all signs; no coefficient table is supplied. Their exact norm identity is

    sum_lambda h_lambda c_lambda^2=R_mu
       =z_mu product_r r_r^(m_r(mu)).

This is a proof consequence, not a finite validation assumption.

Use the NATIVE NS eigenvalues E_lambda=sum_i(q^(-lambda_i)-1)t^(i-1),
not the differently normalized operator in the super-Macdonald paper.
They are rational with denominator dividing D^(3D)(D+1)^D and polynomial
bit length. Form a E_lambda/c and reduce modulo 1 by exact integer arithmetic
in poly(D,L) time. Compute each exp(-2pi i a E_lambda/c) to absolute error
delta<=2^(-b-5), with a COMMON dyadic real/imaginary precision, and write
v_lambda=c_lambda z_lambda. Bounded-argument elementary pi/sine/cosine
algorithms have polynomial BIT cost. Numerical |a/c| does not enter the
clock: its binary length L and exact modulo reduction do.

Orthogonality gives initial vector error <=delta sqrt(R_mu), independent
of M and of the sizes of individual c_lambda. Its normalized version is
within 2delta of the exact normalized time-evolved state, and is nonzero
because delta<1. Its full occupation Born law consequently has TV error
<=2delta. Approximate the phases ONCE. Thereafter the rational-vector
sampler is exact except for its finite random draws; rare conditional
histories do not request renewed phase precision.

At each CDF draw use

    B'=b+ceil(log2(8D^2+8))

fair bits, compare the dyadic uniform with exact rational CDF endpoints,
and skip empty intervals. There are at most D boundaries at a step and
D steps. Coupling with continuous uniforms gives total additional TV error
<=D^2 2^(-B'), uniformly over adaptive histories. Hence

    TV error <=2delta+D^2 2^(-B') < 2^(-b).

This is a deterministic runtime bound with finite randomness, not an
unbounded rejection clock. Enumeration, matrices, initial vectors,
phase arithmetic and at most D^2 candidate matrix-vector products cost
poly(D,M,L,b) BIT operations. With M<=(D+1)^(4k), this is precisely
(D+1)^O(k) poly(D,L,b). D=0 is the direct vacuum case.

As a separate valid corollary, starting with a labelled eigenstate and
S=its subpartitions gives the bounded-Durfee Macdonald sampler: if its
Durfee size is h, M<=(D+1)^(2h). Neither corollary nor the fixed-k theorem
asserts a polynomial bound for arbitrary growing k or h. The complete
same-output classical match is established for every FIXED number k of
input bosons; no general classical obstruction or advantage follows.
