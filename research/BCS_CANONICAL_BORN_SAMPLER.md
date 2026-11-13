# Attractive BCS ground Born sampling: canonical classical construction

2026-11-14. Reviewed WRITTEN classical construction. The full250-line
independent source/composition proof was parent-checked, together with the
actual primary source hypotheses, flow bounds and defect-mass argument.
This is a CLASSICAL comparator for a proposed gap-based quantum preparation,
not a quantum-state simulation or an all-eigenstate Gaudin gap theorem.

## Selection and native hypothesis

After general ternary decision closed, the pass restarted from STATE/TRAPS.
Corpus been-tried and baselines preceded the literature. The catalogue named
tensor-network simulation; the actual literature supplies a stronger rigorous
ferromagnetic XY path-integral sampler. Compare this operation with fixed-
contrast conductivity (no new cancellation-preserving contraction available)
and projected-Slater ancilla feedback (no new paid branch reset). The present
operation can decisively test whether stability-based BCS ground preparation
would yield an unmatched Born readout, so it is selected before quantum code.

Input: N distinct rational energies eps_i, rational g>=0, particle number
0<=M<=N, error tau, and a PAID/PROMISED lower bound kappa on the FINAL
fixed-M spectral gap of
 H=D-g A_J, D(S,S)=sum_(i in S)eps_i,
 A_J the Johnson adjacency (one occupied/unoccupied swap).
Equivalently H=sum eps_i n_i-g sum_(i<j)(sigma_i^+sigma_j^-+h.c.).
Target: a classical sample within TV tau of squared amplitudes of the
unique fixed-M ground state. No Bethe roots, eigenvalues, amplitudes,
prefixes, chemical potential, partition function or sampler is advice.
The final clock is polynomial in native rational bits, N, 1/tau and J/kappa,
where J=max(g,max_i eps_i-min_i eps_i) after discarding a uniform field.
For interior M and g>0 this is positive. Normalizing by J makes the norm
bound K<=N+N^2; all costs are scale-invariant. The gap-based small-g
branch below removes both 1/g and any inverse-level-spacing resource.

Proposed quantum mechanism had been stability of imaginary-time amplitudes,
followed by a Doob-transform/internal-gap theorem and adiabatic preparation.
Its potential exponential coordinate saving is not a separation: the same
final-gap premise now appears sufficient for a classical Born sampler. This
classical route does NOT output the coherent ground state and does NOT cover
arbitrary interacting excited branches, whose joint-gap problem stays open.
No unconditional polynomial gap, hardness, novelty or quantum speedup claim.

## Actual sources and cheapest falsifier

Primary PDFs/text/provenance: audits/sources/bcs_stability_selection/.
BBL0707.2340v2 Proposition5.1 (physicalLF1617--1652) proves stability under
symmetric exclusion. Positive external fields substitute z_i ->a_i*z_i,
so also preserve stability. Trotter and closedness pay their sum.
Wei2609.26802v2 Theorem7.1 (LF2520--2575) proves concavity of sector growth;
the argument below checks it directly. Its full disk-space positive-damping
gap and bounded-degree state-query theorem are NOT fixed-M internal-gap
bounds. Braida etal2606.23614 addresses symmetry-reduced chains, not this
arbitrary-site native gap. No theorem was inferred from its abstract.

Anari log-concave-II coefficient power preservation uses 0<alpha<1, not2.
An exact generic counterexample prevents squaring stable coefficients by
fiat: take v1=(1,0),v2=(1,1),v3=(0,1),v4=(-1,1), and
 f(z)=det(sum_i z_i v_i v_i^T).
Its pair coefficients are all1 except w24=4. f is stable; its Hessian has
inertia(1,2,1). Squaring each coefficient gives Hessian inertia(2,2,0), hence
not Lorentzian. The positive subspace constant on pairs13/24 has matrix
[[1,2],[2,16]], determinant12>0. This is NOT a native BCS ground counterexample.
Exact Sage check controls/bcs_born_stability/{check.py,result.json} additionally
found no Born-Lorentzian failure on three predeclared N4,M2 native instances;
that finite result proves neither closure nor a gap and is not extended.

## Sector curvature without an energy oracle

Let L=sum_(i<j)(SWAP_ij-I) on the coefficient space of multiaffine polynomials.
In degree m, L_m=A_J-m(N-m)I. The generator T=gL-D preserves nonnegative
real stability by BBL and positive external-field Trotter products.
Apply exp(tT) to product_i(1+z_i), and let c_m(t)>0 be its degree-m
coefficient sum. The diagonal restriction is real-rooted with negative
roots, so Newton gives c_m(t)^2>=c_(m-1)(t)c_(m+1)(t) times a fixed binomial
factor. For each fixed N, positive initial coefficients and Perron growth
give lim_(t->infinity) log(c_m(t))/t=r_m, the top eigenvalue of T_m.
Thus 2r_m>=r_(m-1)+r_(m+1). Since
 E_m=-r_m-g*m*(N-m),
we obtain for EVERY rational energy list and g>=0
 E_(m+1)+E_(m-1)-2E_m >= 2g.
This is sector-energy convexity, NOT an internal fixed-M spectral gap.

For g>0 choose a rational K>=||H||, e.g.
 K=N*max_i|eps_i|+g*N^2.
The interval [E_M-E_(M-1),E_(M+1)-E_M] has width>=2g (interiorM), and its
endpoints lie in[-2K,2K]. A grid in[-2K-g,2K+g] with spacingg/4 has
O(1+K/g) entries and contains a chemical potential mu at distance>=g/2
from both endpoints. By convexity, H-mu*Nhat then has its unique global
ground state in sectorM and every other sector's ground energy is at least
g/2 above it. No unknown E_m is evaluated. For M=0,N output the unique
configuration directly.

Take rational beta>=C*(N+log(1/tau))/min(kappa,g) with a fixed sufficiently
large numerical C. At that good grid point the grand-canonical Gibbs state
has target ground weight>=1-O(tau). For EVERY other grid point, conditioning
the unperturbed Gibbs diagonal on Nhat=M gives exactly the SAME canonical
Gibbs law for H_M, independent ofmu. Its distance to the ground Born law is
O(tau), by the final gap kappa and dimension<=2^N. Therefore a grid point
with merely constant observed M probability is sufficient; no energy oracle
or correctness test on unknown eigenstates is required.

## Native grand-canonical sampler and two source repairs

Rayudu--Takahashi2509.21683v1 Eq3 covers arbitrary rational Z-fields and
ferromagnetic XY. Eq8--12 give positive path weights whose fixed-time-slice
marginal is diag((CC^dagger)^L)/Tr((CC^dagger)^L), with
 C=product_l(I-delta*h_l), delta=beta/(2L).
The operator-loop chain samples an enlarged zero/two-defect space; Lemma2
bounds the mass ratio polynomially, so capped rejection yields original
zero-defect paths. Reading their first slice is the desired Trotter marginal.

IMPORTANT: its mixing bound Eq44--45 contains
 c_min^-1, c_min=min_(i<j){a_ij-b_ij,a_ij+b_ij}.
For number-conserving XY a=g/2,b=-g/2, c_min=0. Do not import the printed
bound directly. Instead perturb by -lambda sum_(i<j)X_iX_j, with positive
rational lambda<=c*tau^2/(beta*N^2). The perturbed a=g/2+lambda,b=-g/2
has c_min>=lambda; rescale all fields/couplings to the theorem's bounded
range, scaling beta accordingly. All rescaling and inverse c_min costs are
polynomial in the charged quantities. The perturbation norm is<=lambda*N^2.
For Gibbs states, relative entropy is<=2beta||DeltaH||, so Pinsker gives
trace/diagonal TV O(tau). This also controls the loss of exact number
conservation in the implemented sampler; the IDEAL target remains unchanged.

IMPORTANT: source Theorem1 explicitly bounds partition-function error only.
For sampling, prove a state bound separately. Let B=sum_l||h_l|| and choose
delta*B<=1/10. Product expansion gives
 log(CC^dagger)=-2delta*H_pert+O(delta^2*B^2).
Define H_eff=-log(CC^dagger)/(2delta). The symmetric product is positive
definite and ||H_eff-H_pert||<=C0*delta*B^2. Choose L polynomially large
so beta*C0*delta*B^2<=c*tau^2. Then (CC^dagger)^L=exp(-beta H_eff) and
Gibbs relative entropy/Pinsker gives O(tau) normalized-state error.
No exponential exp(beta||H||) approximation bound is used. This elementary
log expansion follows in the ball ||CC^dagger-I||<1/2, so has absolute
constants; extra numerical slack can be chosen before implementation.

The actual full-source flow bounds resolve the larger-L and small-c_min
questions. Write P=M1+2M2=O(N^2 L), using the source's factor2/P weighting
of two-defect paths. Eqs32/39 give nonzero transition bounds
Omega(delta*c_min/P) from C0 and Omega(delta*c_min) from C2. Eqs28/36 give
base congestion O(P/(delta*c_min)); routing C2-C2 pairs through C0 costs
another O(P), and path length O(P) yields a mixing cap
 O(P^3/(delta*c_min))*(log(1/pi_start)+log(1/epsilon_mix)).
The c_min exponent is ONE; no c_min enters an exponential multiplicity.
Eq47's ambiguity factor is at most exp(O(N^2 L delta^2)); enforce the
additional harmless lower bound L>=16*N^2*beta'^2 after source rescaling.
Thus increasing L for the state error preserves the complete flow proof.

AppendixC's raw two-defect weight ratio is O(P^2), while its weighted
probability ratio is O(P). In C7--C8, s_min(CC^dagger)>=1/2 is needed to
replace exponent L-2 by L; our delta*B<=1/10 supplies it. Let p0>=1/(C1*P)
be the closed-path probability bound. Set mixing/coin TV error <=q*p0/16
to obtain a q-accurate closed-path slice after conditioning. Cap independent
closed-path trials at O(P*log(1/zeta)); then charge the second, constant-
probability M-conditioning separately. No uncharged postselection occurs.

All path data and local weights are rational of polynomial bit length.
Round transition coins with a telescoping deterministic-step error budget.
Even the crude finite-state count bounds log(1/pi_start)=O(N*P+log(P)):
there are at most exp(O(N*P)) configurations, local weights are <=3/2,
and the all-zero closed path has weight >=2^(-P). No exact Boltzmann
real-number oracle, unknown partition function or unbounded retry is used.

## Selection, conditioning, and clock

For each grid point use independent approximate Gibbs samples to estimate
Pr(Nhat=M), with additive error e.g.1/16 and union-bounded failure probability.
Use enough samples that any accepted empirical probability>=1/2 implies
true ideal mass>=1/4, while the good grid point is accepted with high
probability. A sampler at TV accuracy c*tau uniformly at every grid point
pays these margins and the eventual conditioning amplification. Take fresh
samples at an accepted point and reject unless their Hamming weight isM;
cap the geometric repetitions. If none succeeds or no grid is admitted,
return ABORT, charged to the same tau error budget. Conditioned sample
error is at most a constant multiple of the unconditional sampler error.
The mixture over accepted grid points remains the SAME canonical target.

All quantities in the grid construction can first be normalized by J.
Before the following branch, runtime is polynomial in native coefficient
bits,N,1/tau,J/g,J/kappa, including the grid, beta, c_min^-1,
Trotter length, chain mixing, path rejection and confidence amplification.
No polynomial dependence on log inverse tau is claimed.

At g=0, distinct sorted eps give the unique M-lowest-energy monomial.
For g>0 let v=||g*A_J||<=g*N^2/4 and let gamma>=kappa be the PROMISED true
final sector gap. Weyl gives Delta>=kappa-2v for the g=0 sorted gap.
If g*N^2<=tau*kappa/8 (take 0<tau<=1/4), then Delta-v>=kappa-3v and
the isolated-eigenvector angle is at most v/(kappa-3v)<tau/16. Measuring
the lowest-M monomial is therefore tau-accurate. This uses the final-gap
promise, not a separately promised native site spacing.
Otherwise 1/g<8*N^2/(tau*kappa), hence J/g is polynomial in N,1/tau,J/kappa.
The complete resource statement is poly(native bits,N,J/kappa,1/tau).
False kappa promises are not detected or certified. Optional failure eta
is paid with log(1/eta); all error/failure budgets use min(eta,tau).

## Paid attack dispositions

Run audits/claude_runs/2026-11-14-bcs-canonical-attack completed/end_turn;
all8850bytes read. Usage estimate0.405924USD, not invoice or balance. Process
gone with exec handle lost is NOT labelled reaped. No retry or OpenAI call.
Its sector/grid, two Gibbs-state repairs and conditioning deductions check.
R1 improves the original explicitly charged inverse-spacing clause to the
gap-only branch above; the original clause was not a false bit-polynomial
claim. O1/O2 are resolved against actual full-source Eqs28--47, as above.
The C7/C8 minimum-singular-value condition and first conditioning factor
are explicitly included. Its acceptance label is not mathematical evidence.
Only the claimed Born output is compared; precision dependence alone is
not a proved complexity separation in either direction.

## Independent review and final boundary

Full250LF proof: audits/reviews/2026-11-13-post-ternary-constructive-selection.md,
completedNov14 (filename retains assigned date). Every step was parent-read.
It additionally removes reliance on the source's terse Eq34 summation: a
trace with k<=4 fixed X insertions has magnitude <=8^k*Tr(U^L), U=CCdagger,
by bounded partial-period products and Schatten Holder. Summing head positions
supplies the safe, looser computable mixing cap
 O(P^4/(delta*c_min))*(N*P+log(P/xi)).
The actual weighted closed-path bound is rho0=(1+128P)^(-1); choose
xi=q*rho0/64. Source's sharper P^3 clock is unnecessary for the endpoint.
The normalized Trotter cap can explicitly be
 L>=max(8*beta'*b0,4096*beta'^2*b0^2/q^2,16*N^2*beta'^2,8),
where b0>=max(1,sum||h_l||), q<=min(1/64,tau/256). Log expansion constant10
and Gibbs Pinsker pay the two state errors; capped independent sampling and
min(eta,tau) failure allocations pay BOTH conditionings and every branch.

Established: a bounded randomized classical Born sampler with native input,
final fixed-M gap lower bound kappa, and poly(native bits,N,J/kappa,1/tau,
log(1/eta)) clock. No inverse-g, site-spacing, energy or root advice remains.
Falsified: generic stable coefficient squaring, and the inference that a
polynomial-gap ground-preparation proposal alone supplies an unmatched
occupation readout at inverse-polynomial accuracy. The latter is a scope
comparison, not a lower bound or exclusion of every quantum advantage.
Assumed: the promised FINAL internal gap and retained primary loop theorem;
no uniform gap proof or promise certification is supplied. Sector curvature
is proved separately and does not establish this internal gap.
No implementation, coherent-state classical simulation, arbitrary excited
Gaudin branch, novelty, hardness or Shor-level result is claimed.
Next: compare independent high-upside constructive routes. Do not extend
native Born log-concavity, gap scans, or XY implementation by inertia.
