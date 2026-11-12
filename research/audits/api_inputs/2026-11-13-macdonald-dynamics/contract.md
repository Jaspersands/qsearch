# Native integrable real-time occupation sampling

Question: can a classical algorithm sample the SAME full joint occupation
law after real time under the Nazarov--Sklyanin Hamiltonian, for arbitrary
explicit occupation input, in poly(D,L,b) BIT time? This is the selected
scientific question; all failures below are scoped, never hardness.

Input numerical D>=1; explicit partition mu of D (bosonic occupation m_k),
binary rational tau=a/c (c>0), bit length L, accuracy b. Actual time is
T=2*pi*tau. Global t=D/(D+1), q=t^3; use these parameters at EVERY degree.
Canonical bosonic basis corresponds to p_mu/sqrt(R_mu), where
R_mu=z_mu product_k r_k^m_k, r_k=(1-q^k)/(1-t^k)=1+t^k+t^(2k).
No eigenvector, coefficient table, quantum input, sampler or advice supplied.

Define vertex coefficients V_n by
V(z)=exp(sum_(k>=1) (1-t^k) p_k z^k/k)=sum_n V_n z^n.
Star is adjoint in the Hall(q,t) form. The native self-adjoint Hamiltonian is
H=sum_(n>=1) q^(-n) V_n V_n^*/(1-t), restricted to degree D.
This is actual Nazarov--Sklyanin2015 Eq1.17. Eigenvectors are normalized
Macdonald J_lambda with EXACT rational eigenvalues
E_lambda=sum_(i>=1) (q^(-lambda_i)-1)t^(i-1) (Eq1.18).
The zero-based box sum form is
E_lambda=(q^(-1)-1)sum_(i,j in lambda) t^i q^(-j).
Let U_(nu,lambda) be their real normalized power-sum amplitudes. Target:
P_(mu,tau)(nu)=|sum_lambda U_(nu,lambda) exp(-2*pi*i*tau*E_lambda)
                                      U_(mu,lambda)|^2.
Output one partition nu, within TV 2^-b. Input load costs O(poly D).
Optional simpler observable is a specified normalized mode count k*n_k/D;
its estimation must not be confused with the full sampler.

Existing independently checked WRITTEN transform U and its actual inverse
cost poly(D,b), clean on arbitrary superpositions/reference; no circuit has
been implemented. Accept this interface in this task; do not re-review it.
Then U diag(exp(-2*pi*i*tau*E)) U^dagger is a complete written quantum
candidate costing poly(D,L,b). E is a polynomial-bit rational computable
from lambda. Compute tau*E modulo1 EXACTLY before phase approximation.
Transform error does not grow with |tau|. All lower scratch is retained
and erased up to clean error; no exact-angle or eigenvalue oracle.
This is a direct instance of KNOWN efficient-diagonalization fast forwarding
(Gu--Somma--Sahinoğlu2021 Thm3.1), not novelty or an advantage proof.

Strong baseline: explicit p(D)=exp(O(sqrt D)) symmetric-function linear
algebra, then rational spectral phases, yields exp(O(sqrt D))*poly(D,L,b)
classical sampling. Its time dependence is ALREADY poly(L), so time alone
is not a classical separation. Need improve its dependence on D.
Row/column eigenstate laws have exact weighted-cycle DP. Near-row/column
with deficit s have D^O(s)poly(D,b) samplers (attached note). General
Macdonald eigenstate Born sampling is unresolved. Those eigenstate samplers
do not automatically simulate coherent superpositions or this dynamics.
Jack3 has a stronger bounded-Durfee classical representation (attached
only for the few-phonon obligation), not automatically Macdonald.

Native vertex entries are nonnegative in normalized occupations, so the
positive row eigenvector suggests a Doob transform to a reversible Markov
generator. A stochastic/imaginary-time sampler or stationary-law sampler
is NOT automatically a real-time Born sampler. Exact determinants,
finite-colour lifts and matrix product representations must pay the
representation size, input conversion, output conditionals, signs and
precision. No free trace, random-state loading or physical-position map.
At q=t^3 coincident global contents are legal; do not divide by their gaps.

One-boson useful control: actual Mickler2026 Thm4.1 gives
[p_D]J_lambda=(1-t^D)/D product_(boxes except origin)(t^i-q^j).
Hence it vanishes exactly when lambda_4>=2; first zero (i,j)=(3,1).
This yields polynomial spectral support for mu=(D), but not automatically
an efficient occupation-output sampler. For k>1 do NOT infer individual
p_mu coefficient vanishing from a univariate principal-specialization zero:
cancellations among different mu of the same length are possible.

Falsifiers: exact all-D polynomial classical sampler; a missing native
transform interface; a coefficient/normalization or source-access oracle;
exponential cost hidden in phase precision, conditional sampling or variance.
Do not infer hardness/advantage from failure of any route or finite tests.
No proposal to sweep tiny D unless a concrete identity can be falsified.
