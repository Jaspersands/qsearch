# Finite-copy nonlinear clock and independent native-operation screens

2026-11-14. Fresh STATE/TRAPS pass after weak-phase parking. Independent
arithmetic and physical comparisons preceded source checks; no API call or
quantum implementation. The selected scientific question is whether the
finite-copy mean-field compiler actually pays the error/clock needed for a
native nonlinear-wave scalar output. A cheap exact fluctuation test blocks
importing a mean-field-norm-only estimate. It is not a nonlinear-algorithm
lower bound. Reviews/source locators are listed below.

## Candidate, access and asymptotic obligation

Physical candidate: normalized Hartree/Gross--Pitaevskii wave on a periodic
fixed-volume 3D box, D=2^(3n) grid sites. Input binary n,T,g, explicit short
Fourier lists for initial wave and potential, a box-membership circuit,
and additive accuracy epsilon. Output the mass in that box at T. Lists,
initial preparation, every fresh copy and observable readout are charged.
Desired advantage is poly(n,T,1/epsilon,input bits) versus a dense D-grid
calculation; this comparison is insufficient unless adaptive classical
spectral/low-rank resolution is also charged on the SAME solution family.
No all-amplitude output, QRAM or supplied nonlinear trajectory is assumed.

Mechanism: prepare M product copies, evolve the symmetric linear many-body
Hamiltonian sum h_a+(M-1)^-1 sum_(a<b)W_ab, and measure a one-body output.
An all-input quantitative mean-field theorem plus a paid combined-evolution
clock must bound M and all gates polynomially in the native parameters.
This operation is ALREADY present in Lloyd et al2011.06571v2, actual
Eqs3--5 and supplement, downloaded at
audits/sources/nonlinear_mean_field_selection/lloyd.{pdf,txt}.
It is not newly supplied by naming it here. Source actual LF101--142,
330--383 and575--670 retain energy, stability and copy/step conditions.

First normalization attack: psi_j=phi(x_j)/sqrt(D), so the contact term is
gD|psi_j|^2 psi_j, W=gD sum_j|j,j><j,j| and ||W||=|g|D.
Kinetic norm grows as D^(2/3). Replacing these by constants changes the
equation. Individually fast diagonal/Fourier phases do not pay their
combined evolution or mean-field error. This is not a gate lower bound;
energy/regularity-restricted estimates could change the outcome. If those
same regularity bounds imply polynomial classical Fourier resolution, that
stronger comparator already removes the nominal grid-size advantage.

## Exact fluctuation counterfamily: all copy counts

For every M>=2 take

 H_M = kappa/(M-1) sum_(a<b) Z_a Z_b,   input |+>^tensorM.

The one-particle Hartree Hamiltonian is kappa <Z> Z=0, so the Hartree
trajectory is exactly |+>. The full unitary is diagonal and elementary:
tracing M-1 independent signs gives

 rho_1(t) = (I+c_M(t)X)/2,
 c_M(t) = cos(2 kappa t/(M-1))^(M-1),
 trace_distance(rho_1(t),|+><+|) = (1-c_M(t))/2.

For fixed nonzero kappa*t and growing M, the error is
kappa^2 t^2/(M-1)+O(M^-2), while ||kappa <Z>Z|| is identically zero.
This proves that the size of the mean-field Hamiltonian ALONE cannot
control finite-copy error. Interaction fluctuations/correlations must be
included. A smaller time mesh does not change this exact physical error.
This does not preclude rigorous mean-field bounds using interaction norms,
stability or other additional hypotheses. No asymptotic claim uses a scan.

There is a separate source-rate normalization issue. A symmetric k-body
binomial average has only fraction k/M of its terms touching a selected
copy; unit-rate mean-field evolution requires multiplication by M/k.
Ordered tuples alter only a fixed k! factor. The source's m in Eq3 must
also be reconciled with Eq2's m contracted copies plus an output operator;
we do not silently identify those arities. For a literal two-body average with pair
coefficient kappa/binom(M,2), the exact coherence instead equals
cos(2 kappa t/binom(M,2))^(M-1); its finite-copy error is still nonzero
while the mean-field norm vanishes. Keep these two clocks separate.
The main text defines E through f(x), while the supplement also calls E a
maximum energy scale. A larger interaction-based interpretation would need
its own proof; we do not refute every possible such interpretation or a
corrected algorithm. The printed first-order Euler/copy assumptions must
not be silently removed when comparing its separate mesh-error formulas.

Single exact convention control completed: M=3,kappa*t=pi/2, pair phasepi/4,
direct cyclotomic amplitudes/partial trace give rho_1=I/2, trace distance1/2
from the Hartree target; terminal0, independent helper run once and full
result/core script parent-read at audits/controls/mean_field_clock/.
The final177-line physical review and source addendum were fully checked.
This test concerns a bounded X/phase observable;
computational occupations remain unchanged, so it is NOT a lower bound on
the original PDE box-mass observable or its explicit Fourier input model.

## Independent arithmetic and cryptographic comparisons

Binary factorial candidate: input odd prime p and 0<=n<p; output n! modp,
target poly(logp) bounded-error time, no class/unit/gamma advice. A normalized
Gross--Koblitz Gauss unit u_n=-G(omega^-n)/pi^n lies in Q_p and has residue
(n!)^-1; this scalar target is not subject to an output-dimension barrier.
But norm from Q_p(pi), degree p-1, returns u_n^(p-1). Multiplication by
ANY Teichmuller root gives the same entire norm and all possible nonzero
residues. Norm compression loses exactly the requested digit. Even granting
an extra consistent global complex-root interface, the retained Gauss-phase
routine has O(1/phase_error) cost; selecting p-1 root factors at errorO(1/p)
costs numerical p. No general arithmetic root-selection lower bound follows.
Tal TR26-211 already uses binary addition chains for compact Jacobi products;
its expanded conductor cost remains. Actual Theorems1.1/1.3 and Eq13--14,
plus vanDam--Seroussi Theorem1, checked against retained primary texts.
Central-binomial residue evaluation is equivalent via one halving chain;
binomial SAMPLING supplies no exact modular coefficient oracle.

Secure supersingular curve candidate: input binary p and a known initial
curve, output a random curve whose endomorphism ring remains unavailable
even with the declared sampler transcript. Proposed simultaneous Hecke
dephasing would require paid joint spectral resolution, explicit curve
oracles, and a valid security reduction under an explicit hardness model.
Classical random walks produce curves together with a known path; deleting
that path is a different trusted-erasure model. No End/Hom advice is free.
The apparent new polynomial source2602.02263 was withdrawn in v3 on
21September2026 for errors needing substantial revision. Actual v2 was
retained ONLY to inspect scope, not as a theorem: its Theorem4.4 ALSO assumes
a strong sup-norm conjecture beyond average-case EndRing hardness.
Status and source: audits/sources/hard_curve_selection/source.json and
withdrawn_v2.{pdf,txt}. https://arxiv.org/abs/2602.02263 is authoritative
for the withdrawal; no claim about which specific error caused it is made.
Its p^-1+o(1)-type marginal bound alone would not imply TV uniformity or
polynomial-density domination needed to preserve negligible failure in
security parameter logp. No replacement proof or native algorithm is admitted.

## Disposition and next gate

All three candidate mechanisms are unadmitted after cheap decisive screens.
The main finite-copy clock question yielded an exact obstruction to the
specified error accounting, not a repaired end-to-end nonlinear solver.
No paid request is justified merely to restate these gaps. Full arithmetic
gamma extraction, uniform-grid nonlinear transport and secure-curve sampling
remain UNKNOWN under their respective declared models. Do not infer hardness,
generic no-go, novelty or speedup. Keep weak-phase/BCS/scattering parked.
The final independent source addenda/exact control are complete. Next select
a NEW concrete native operation by external value rather than extending any
of these conditional interfaces. Any future mean-field admission must pay
interaction fluctuations, normalization, solution stability and the strongest
classical resolution comparator before quantum construction.
