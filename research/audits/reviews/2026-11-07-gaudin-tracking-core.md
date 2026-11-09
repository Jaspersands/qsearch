# Joint-charge traversal: independent core review

2026-11-07. CLOSED conditional mathematical review. Read current STATE/TRAPS,
GAUDIN_JOINT_CHARGE_TRAVERSAL.md, the retained Lutz primary text (main
equations10--12 and AppendixH), and the retained Boixo--Knill--Somma text.
No network/API/Git, controls, or quantum execution performed by this review.

**Disposition:** the written joint-charge randomization construction is
correct under its explicit rank-one branch, joint separation and charged
simulation assumptions. It removes the need for classical intermediate
Bethe roots/charge labels. It does NOT prove the same-sector separation
needed for the full native Richardson--Gaudin endpoint. This is neither a
novelty judgment nor a separation from classical algorithms.

## Selection comparison

Focused corpus been-tried/baselines queries were read for Gaudin traversal,
native Legendre reconstruction, and full-table scalar OPI. No catalog
baseline hit for Gaudin/Legendre is evidence of absence. Retained topical
notes supply the stronger comparators.

* Native Legendre: fresh character phase copies, polynomial coefficients as
  output, desired polynomial(degree,log p) recovery. The retained resultant
  operation is paid but its growing-degree split-mask loss remains; this
  comparison identified no new collective operation removing it.
* Full-table scalar OPI: explicit random halfsets, output a verified
  polynomial with the known DQI score. Published adaptive systematic-basis
  annealing is stronger than fixed-catalog lines; the present comparison
  identified no new adaptive quality mechanism that beats its prior tests.
* Gaudin: ordinary rational sites/coupling and a starting occupation string,
  output the continued quantum eigenstate. Joint-charge randomization is a
  concrete supplied-Hamiltonian operation that bypasses a distinct source
  assumption, the classical nonlinear root tracker. It therefore ranks
  first for a bounded constructive admission, while its quantitative
  spectral premise remains unresolved.

The next substantive test is the SAME-particle-number joint gap at growing
filling, for a natural explicit family such as eps_i=i and g in[0,1]. Do
not substitute another mesh/filter improvement, an easy one-particle
sector, or the already-false stronger constant floor for that obligation.

## 1. Path derivative and ideal traversal

Let P(s) be the promised isolated rank-one joint branch. C1 differentiability
follows locally from the C1 charges and isolation: at a fixed s0 the
proof-only Hermitian matrix sum_i(Q_i(s)-q_i(s0)I)^2 has a simple isolated
eigenvalue, so its local projector is C1 and agrees with the continued
joint branch. This argument does not compute the unknown q_i(s0).

In parallel gauge, for an orthogonal joint eigenbasis w at s,

    (q_wi-q_vi)<w|v'> = -<w|Q_i'|v>.

Squaring and summing gives

    kappa^2 ||v'||^2 <= sum_i ||Q_i'v||^2 <= L^2.

Degeneracy among complementary joint eigenspaces is harmless; degeneracy
of the target joint branch is excluded by the promise. The projective
angle between mesh neighbors is at most L/(kappa R), hence the squared
overlap is at least 1-(L/(kappa R))^2. For channels that measure P and then
arbitrarily evolve its complement without coupling back to P, the positive
always-target history has weight at least 1-L^2/(kappa^2 R). Other histories
can only add positive output density operators.

Use the standard trace distance D(rho,sigma)=||rho-sigma||_1/2. Then
R>=max(1,ceil(16L^2/(kappa^2 epsilon^2))) gives ideal distance <=epsilon/4.
If an unnormalized trace norm convention is used, adjust the constant by4.

## 2. Joint dephasing and dimension-free error

One independent round of uniform t_i in[0,T] multiplies a target--other
coherence by the product of characteristic functions of the m uniforms.
Since some |q_vi-q_wi|>=kappa/sqrt(m), choosing T>=4sqrt(m)/kappa makes
one sinc factor have absolute value <=1/2. After k rounds the multiplier
has absolute value <=2^-k. No separation among complementary eigenvalues
and no union bound over their number is required.

Let D be this averaged channel and Q=I-P. The ideal comparison channel

    M(rho)=P rho P + D(Q rho Q)

is CPTP because every sampled evolution commutes with P. The difference
D-M acts only on the two off-diagonal blocks. On the complement this
action is multiplication by a contraction F with ||F||<=2^-k. Positivity
gives ||P rho Q||_1<=sqrt(Tr(P rho)Tr(Q rho))<=1/2. Consequently

    ||(D-M)(rho)||_1 <= 2^-k.

The same proof holds for any untouched reference, replacing P,Q,F by their
tensor products with its identity. Thus this is sufficient for channel
hybrids, not merely a pointwise estimate for pure unentangled inputs.
Taking k=ceil(log2(8R/epsilon)) gives accumulated trace-norm error <=epsilon/8.

## 3. Explicit finite precision and polynomial clock

All bounds used by the algorithm must be explicit rational upper/lower
bounds. Choose a rational or dyadic T in
[4sqrt(m)/kappa,8sqrt(m)/kappa]; exact irrational sampling is unnecessary.
Let K_calls=R k m, B bound all charge operator norms, and 0<epsilon<=1.
One concrete conservative allocation is:

* couple a continuous uniform time to its lower dyadic grid point, with
  grid width <=epsilon/[192 K_calls(1+B)];
* round each Hamiltonian to total operator error
  <=epsilon/[192 K_calls(1+T)]; divide this tolerance by the Pauli-list
  length when rounding individual coefficients;
* simulate each rounded evolution to operator error
  <=epsilon/(192 K_calls).

The sum of the three errors per unitary is <=epsilon/(64 K_calls).
The corresponding total channel trace-norm error is <=epsilon/32, using
||Ad_U-Ad_V||<=2||U-V||. Combined with the previous two sections, the final
standard trace distance is at most

    epsilon/4 + epsilon/16 + epsilon/64 < epsilon.

Uniform dyadic sampling requires only a fixed bounded number of random
bits per call. The number of precision bits is polynomial in the binary
bounds and log(K_calls/epsilon). Standard product-formula simulation alone
suffices for the claimed polynomial-in-1/epsilon endpoint; no favorable
log(1/epsilon) simulation theorem is needed. The charged sum of evolution
times weighted by Pauli norm is at most R k T A. Polynomially many terms,
explicit rational coefficients and polynomial numeric A,L,1/kappa are
essential. A binary encoding of an exponentially large coefficient does
not pay its simulation cost.

This prepares an averaged output density operator close to a pure target.
It does not certify every individual random seed, coherently transform an
arbitrary input branch superposition, or fast-forward the model.

## 4. Native source and strongest comparator scope

For the stated Gaudin charges, ||P_ij-I||=2 gives the written bounds
L<=G sqrt(sum_i S_i^2) and ||Q_i||<=1+G S_i. Their Pauli descriptions have
O(N) terms per charge. The exact Hamiltonians conserve particle number.
Approximate simulations can be charged in the preceding full-space hybrid;
one need not silently assume an approximate circuit preserves the sector.

The sum_i Q_i=M identity proves separation squared >=1/N only for different
integer particle numbers. These evolutions stay in the starting sector,
so this does not pay the relevant same-sector gap. The retained N3
counterexample to a stronger floor2, the source's finite scans, and small
Smale bounds do not falsify or prove inverse-polynomial separation.

Lutz et al. explicitly assume a polynomial classical charge tracker in
their proposed adiabatic route and leave finite-g same-sector separation
unproved. AppendixH's weak root-separation lower bound is not an upper
bound on the physical gap. Boixo--Knill--Somma already supply the underlying
random-dephasing eigenpath idea; this review concerns the paid joint-charge
composition, not authorship of that mechanism.

Classical one-site/determinant readouts with roots supplied, small-particle
sectors, and the conditional all-prefix Born sampler remain genuine
comparators from RATIONAL_GAUDIN_PREFIX_ADMISSION.md. They do not provide
the present full quantum state from the occupation-string input. Conversely,
failure to find a classical full-state substitute gives no hardness result.
Any claim about observables must retain their actual classical access and
precision assumptions. Full native efficient preparation remains UNADMITTED
until a suitable uniform same-sector gap is proved.
