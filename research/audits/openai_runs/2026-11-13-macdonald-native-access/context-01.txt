# Native Macdonald transform at mesoscopic deformation

## Selection and exact contract

After starting from STATE/TRAPS, corpus been-tried and baselines were run
for Macdonald/Jack eigenbasis transforms (saved /tmp/qsearch_macdonald_*).
No exact catalog baseline matched; that is not absence evidence. Actual
primary2610.12326v1, Sections2-4 through Cor4.9, and1411.1315v3 definitions
were then read. The October2026 paper supplies a full Lax spectral theorem
AND an all-degree creation identity, making a complete q-deformed transform
plausible. This beats another local Selmer arithmetic subclass (general
classical comparator still open) or conductivity-window barrier (no full
joint-poly candidate) for current constructive expected value. It does not
supersede the independent BO work-law classical question. No novelty claim.

Input: numerical D>=1, explicit partition lambda of D or arbitrary supplied
shape-label superposition (its loading charged), integer accuracy b. Fix
N=D+1, t=D/(D+1), q=t^3, for ALL degree stages in this D-instance; do not
change q,t as degree decreases. Hall occupation metric is
 <p_mu,p_nu>=delta_mu,nu z_mu prod_k r_k^m_k, r_k=(1-q^k)/(1-t^k)
 =1+t^k+t^(2k) in[1,3]. Target full clean transform
 |lambda>|0> -> |Jhat_lambda(q,t)>|0>
in normalized power-sum occupation coordinates, with restricted operator
error<=2^-b. The corresponding classical sample has probability
 theta_lambda,mu^2 z_mu prod r_k^m_k/H_lambda.
No coefficient table, state source, Lax oracle, spectral basis or hidden
advice is supplied. Candidate resource poly(D,b); strongest unrestricted
baseline is explicit symmetric-function expansion on p(D)=exp(O(sqrtD))
partitions. No established asymptotic advantage: a polynomial classical
sampler may exist. A full transform is useful for native discrete-BO/Macdonald
spectral dynamics, not automatically a physical position wavefunction.

## Actual source facts and specialization obligation

Use w=z^-1, auxiliary norm ||w^ell p_mu||^2=q^ell||p_mu||^2. Full Lax
L=Qcal^dagger D_(t/q) Qcal, Qcal=pi_nonpositive Q(z),
Q(z)=exp sum_(k>=1)(1-t^k)p_k z^k/k. Source Eq8/Props3.11-3.13:
L Psi_(lambda,s)=[s]Psi, pi0Psi=J_lambda, and ||Psi||²=H_lambda/tau.
Contents [s]=t^i q^-j=t^(i-3j) at row i,column j. The source is initially
generic q,t. At q=t^3, globally coincident contents and zero varpi_lambda
MUST be handled using regular un-hatted cyclic projectors; do not use a
hatted basis with zero principal specialization. Within each partition,
addable and shifted-removable corner contents strictly interlace.

The row Q: w Lambda[w] -> Lambda extracts pi0 Q(z). Source Lemma4.7(ii)
and Proposition4.8 give Q w Psi_(lambda,s)=q^-j J_(lambda+s).
The shift I:w-polynomials degree n-1 -> positive-marker degree n is
I(f)=w f/sqrtq, an isometry. Hence A=Q I and
A Psi_(lambda,s)=q^(-j-1/2) J_(lambda+s), with POSITIVE scalar.
From the full block form, AA^dagger=Q Q^dagger =T2-I on Lambda_n.
Source product resolvent gives eigenvalue
 chi_lambda=(1-t)(q^-1-1) sum_boxes [box].
Parent predicts chi=Theta(n/N²) uniformly n<=D, so its inverse square root
is polynomially conditioned. This prediction and all scalars need proof.

Let V=A^dagger(AA^dagger)^(-1/2). Then on Jhat_mu it should produce
normalized Lax corner vectors with positive removal weights
 p_(mu,r)=q^(-2j(r)-1) tau_(mu-r,r) H_mu/(chi_mu H_(mu-r)).
The probabilities and hook products have polynomial-bit rational formulas.
A shape-side C prepares these weights and removes r. A Fock-side B applies
V, coherently resolves [r], then the principal half-phase of two reflections
to send the Lax vector to its parent with positive phase. If fully paid,
B_down^dagger C_down erases the entire common path, as in the closed Jack
construction. Need uniform inverse-poly tau and paid content resolution.
Expected gap: contents lie in a fixed compact positive interval, distinct
values t^k for integer k in[-3D,D] separated by Omega(1/N). Approximate QPE
must recover k CLEANLY; no free exact irrational-eigenvalue label.

## Parent native-access proposal, unreviewed

Qcal=exp(C), because every monomial lowers the marker and truncation is
monotone. On normalized occupation/marker coordinates,
 C=sum_k w_k a_k^dagger T_(-k),
 w_k=sqrt[(1-t^k)(1-q^k)/(k q^k)].
For k<=D, w_k<=16 sqrt(k)/N. Define gamma_k=N w_k/sqrtk<=16.
A CONSTANT-normalization block for C^dagger is plausible:
prepare k with amplitude sqrt(k m_k/D), leaving leftover marker mass as
failure; multiply by gamma_k/16 using a known rotation; remove the boson,
shift marker up by k, retain k; project k onto a uniform power-of-two
M-label state with D<=M<2D. The top block is
 C^dagger * N/[16 sqrt(D M)].
Every arithmetic operation must be reversible, pair labels kept and erased
correctly; top projection is a block encoding, NOT free postselection.
Normalization<=32 is independent of D. This avoids an exponential
exp(poly(D)) Taylor normalization from a crude sparse-oracle bound.
Taylor LCU of exp(C) at this constant normalization uses degree poly(b),
constant total coefficient normalization (possibly huge), fresh signals and
no expanded word list. Qcal^dagger D_(t/q) Qcal then gives a native constant-
normalization block of L; D_(t/q) has bounded eigenvalues since ell<=D.
The Q row and A inherit constant-normalization blocks by projecting marker.

V must be compiled without an unknown lambda normalization or preparation
oracle. A generic rectangular polar compiler can use the binomial series
for (AA^dagger)^-1/2 on its inverse-poly singular interval. Crucially,
I-B^dagger B for a contraction B should be block encoded as
P U^dagger (I-P) U P using a failure-projector block and SAME inverse banks,
not as a two-term LCU whose norm2 would explode when raised to powers.
Known-normalization oblivious amplification then produces a near-isometry.
All retained work, actual inverses, controls and finite bits remain charged.

## Classical attacks before any quantum implementation

Rows and columns are exact polynomial classical controls. Orthogonality and
triangularity show the single-row polynomial is proportional to degreeD of
exp sum_k p_k/(k r_k); the single-column is proportional to e_D. Thus their
occupation laws are weighted-cycle measures prod w_k^m_k/z_mu, with
w_k=1/r_k for rows and w_k=r_k for columns. Dynamic programming
Z0=1, Z_n=(1/n)sum_(k=1)^n w_k Z_(n-k), followed by size-biased cycle
selection k with probability w_k Z_(n-k)/(n Z_n), samples the exact law.
All rational coefficient bit lengths and finite-bit TV approximation are
polynomial. This is a direct deduction, no hardness inference.

Actual Diaconis--Ram1007.4779 Eqs1.1-1.4 specifies the inverse-Hall-weight
stationary law, hence the ROW control, not arbitrary squared eigenfunctions.
Its q,t>1 domain can be reached by reciprocal parameters: on fixed degree,
Hall weight changes by the common factor(t/q)^D, leaving the Born law and
orthogonal polynomials unchanged. Actual OConnell--Pei1212.6716v2 Theorem2,
Eq11 and stochastic Eq13 specify t=0 random-word/tableau laws. They do NOT
by themselves give this fixed-labelled q=t^3 occupation law. Parent checked
actual statements; no claim to have ruled out other Macdonald-process routes.

Falsifiers: source poles at q=t^3; incorrect creation scalar/chi; exponentially
small transition overlap; constant-normalization C block fails; QPE label
workspace cannot be cleanly erased; generic polar cost hides exponential
normalization; positive classical representation gives unrestricted sampler.
No quantum implementation or finite sweep is authorized by this candidate.
Next decisive work: native access/polar proof, specialized branching proof,
and a constructive strongest-classical attack on this exact output law.
