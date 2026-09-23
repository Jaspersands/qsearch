# Thermal Two-Witness Search: Useful Equilibrium, Obstructed Local Mixing

Status: LOCAL DERIVATION / REVIEW PENDING, 2026-09-24. No independent review,
formal verification, novelty claim, fast Gibbs preparation, or new algorithm.
This is a theory audit with bounded mathematical controls, not a production
annealing subsystem. Gemini owns any implementation and registry integration.

## 1. Candidate Tested And Revised Decision

The measured-fiber reduction needs an ordinary two-witness subset-sum solver,
not a coherent uniform witness sampler. Test the following concrete proposal:
compute a polynomial-size residual-bit energy, prepare its low-temperature
Gibbs distribution, and draw two independent verified witnesses. A quantum
walk or Zeno annealing procedure might seem to supply the preparation.

POSITIVE: the exact Gibbs distribution at inverse temperature log r has
constant source-average probability of supplying a DISTINCT witness pair.
There is no information-theoretic lack of solutions or exponential precision
requirement in the energy evaluator.

NEGATIVE: on almost every natural instance that has two solutions, any
reversible Gibbs chain with the declared bounded-Hamming-radius transitions
has a superpolynomially small terminal gap at useful temperatures. The usual
square-root-gap quantum improvement does not supply a polynomial rapid-mixing
guarantee. There is also an actual warm-start escape bound, not just a loose
annealing runtime estimate.

IMPORTANT REVISION: a small gap is NOT an arithmetic hardness theorem or a
lower bound on every quantum annealing path. An explicit, classically easy
subset-sum family below has even smaller local gaps. Direct preparation,
nonlocal operations, cold-start nonequilibrium search, auxiliary-space paths,
and symmetry-restricted evolution are not eliminated by the local-gap result.
Do not convert it into a generic adiabatic or DCP no-go claim.

Research decision: do not build another local-Metropolis/QSA wrapper on the
assumption that rapid mixing is available. A surviving proposal must specify
how it avoids the derived bottleneck and charge that operation. An ideal
Gibbs matrix or a formal ground-state Hamiltonian is not such an operation.

## 2. Arithmetic Source And Energy

Use the exact distribution in `DCP_MEASURED_FIBER_COLLIMATION.md`:

    Q=2^r, m=r-1, M=2^m, lambda=M/Q=1/2, r>=2;
    l_i independently uniform in Z_Q, t independently uniform in Z_Q;
    f_l(b)=sum_i l_i*b_i mod Q;
    E_(l,t)(b)=HammingWeight(f_l(b) XOR t).              (1)

XOR in (1) is bitwise XOR of the r-bit residues, not modular subtraction.
E is an integer from 0 through r, computable by modular addition, XOR and
population count using polynomial-size reversible arithmetic. Its zero set
is exactly the required subset-sum fiber. The coefficients remain the public
natural labels; no new oracle problem or engineered candidate family is used.

For finite inverse temperature beta>=0 put u=exp(-beta)>0 and

    D=|{b:E(b)=0}|, Z=sum_b u^E(b), pi(b)=u^E(b)/Z.

The proposed classical output is two INDEPENDENT preparations/samples from
pi, returning them only when both solve the target and are distinct. Its
per-instance success is D*(D-1)/Z^2. Two copies are not obtained by cloning
a Gibbs state or reusing a measured sample.

At beta=log r, unnormalized weights are r^-E. They have O(r log r)-bit
rational descriptions. This does not make Z, sampling, or the quantum square
root state easy; it separates a genuine preparation issue from a false
exponentially-many-precision-bits objection.

## 3. Exact Moments And A Positive Equilibrium Bound

For any fixed b, f_l(b) XOR t is uniform. For distinct b,c, these two
residuals are pairwise independent uniform r-bit strings. To see this,
nonzero distinct Boolean rows b,c have a unit 2-by-2 minor, so their two
modular sums are independent conditional on t. If one row is zero, t and
the other nonzero modular sum give the same conclusion. This is only
PAIRWISE independence; higher energies are not a random oracle.

Writing A=(1+u)^r and B=(1+u^2)^r gives the exact formulas

    E Z = lambda*A,
    Var Z = lambda*B - (M/Q^2)*A^2,
    E D = lambda,
    E[D*(D-1)] = M*(M-1)/Q^2.                         (2)

These expectations include empty targets and the zero assignment. There is
no planted-target or legal-only replacement of the distribution.

The preceding measured-fiber note proves two-element Born mass >=1/4. Its
conversion to a UNIFORM-target probability gives Pr[D=2]>=1/16. At u=1/r,

    E[Z-D] = lambda*((1+1/r)^r-1) < 1.

Markov's inequality implies

    Pr[D=2 AND Z-D<=32] >= 1/16-1/32 = 1/32.

On this event Z<=34, so two independent ideal Gibbs samples have pair success
at least 2/34^2=1/578. Thus over the complete arithmetic source,

    E[D*(D-1)/Z^2] >= 1/18496.                        (3)

This loose constant is enough for the research question. The measured-fiber
construction would translate (3) to merge probability >=1/4624 if the Gibbs
sampler were efficiently supplied. It has NOT been supplied. Total-variation
error epsilon per independently prepared sample changes the pair probability
by at most 2*epsilon; a sufficiently small constant accuracy would suffice.
An average error guarantee must be under the same full source distribution.

## 4. Useful Temperature Cannot Stay High

The solution probability of one ideal Gibbs draw is D/Z. On Z>=E[Z]/2,
its contribution to the source average is at most 2*E[D]/E[Z]=2/A. On the
complement use D/Z<=1 and Chebyshev with (2). No independence of D and Z is
assumed. Therefore

    E[D/Z] <= 2/(1+u)^r
              + 8*((1+u^2)/(1+u)^2)^r
            <= 10*exp(-r*u/2),  0<u<=1.              (4)

For the second inequality, log(1+u)>=u/2 and
log((1+u)^2/(1+u^2))>=log(1+u)>=u/2. Cap a bound above one at one if used
numerically. The upper bound need not be sharp at small r.

Pair success is at most one-sample solution success. Consequently a
deterministic temperature schedule claiming source-average pair probability
at least r^-c, for fixed c>0, must satisfy

    r*u <= 2*c*log r+2*log 10,
    beta >= log r-log(2*c*log r+2*log 10).              (5)

This is a necessary condition for THIS Gibbs sampling proposal. It is not a
lower bound on arbitrary optimization. It does not directly apply when the
temperature itself is chosen instance-adaptively using extra information;
that would require a separately audited weighted-source argument.

## 5. Joint Assignment/Residual Isolation

Let k be an allowed Hamming move radius on the m assignment bits, and h an
energy threshold on the r residual bits. Define

    V_in(m,k)=sum_(j=1..k) C(m,j),
    V_out(r,h)=sum_(j=0..h) C(r,j).

Count ordered pairs (b,c) with E(b)=0, 1<=distance(b,c)<=k, and E(c)<=h.
The pairwise residual law above gives EXACT expected count

    M*V_in*V_out/Q^2 = V_in*V_out/(2Q).               (6)

The probability that even one such pair exists is at most (6). Except on
that source mass, EVERY solution is separated from EVERY allowed distinct
neighbor by energy at least h+1. Proposal selection can use the entire
public instance adaptively; the event already covers all such neighbors.

For k=floor(m/16), h=floor(r/8), the usual Boolean-ball entropy estimate gives

    Pr[isolation fails] <= (1/2)*2^(-a*r),
    a=1-H_2(1/16)-H_2(1/8)=0.11914549018... >0.       (7)

Conditioning on D>=2 multiplies this bound by at most 16 because that event
has probability at least 1/16. The exact finite bound (6) is often stronger.
Small r with k=0 is vacuous for actual transitions and must not be presented
as a useful finite local-walk test.

At h=0 this is related to the repo's existing Boolean-witness separation
result. The extra residual-energy radius is what lets it test thermal paths,
not just the final solution graph. It is NOT independence of all neighborhoods
and says nothing about large, implicitly computed jumps.

## 6. Local Chains, Quantum Gaps And A Genuine Escape Bound

Consider any Markov chain on the Boolean ASSIGNMENT space with stationary
distribution pi and transitions of Hamming distance at most k. At a solution b,
stationarity alone gives pi(b)*P(b,c)<=pi(c), hence

    P(b,c)<=exp(-beta*E(c)),
    epsilon_b=1-P(b,b) <= V_in*exp(-beta*(h+1)).        (8)

The bound applies on the isolation event and can be capped at one. It even
covers nonreversible chains on this declared space. Auxiliary-state lifts
need a separate argument. Symmetric-proposal Metropolis has the sharper
epsilon_b<=exp(-beta*(h+1)), without V_in, since the proposal row sums to one.
An extra laziness factor can improve it further.

At beta=log r, (8) is V_in*r^(-(h+1)). With the radii above it is
exp(-Omega(r log r)). The same asymptotic conclusion holds for any fixed
temperature family meeting (5), since beta>=log r-O(log log r). Label-adaptive
local proposal weights do not erase this stationary-flow bound.

For a REVERSIBLE chain, let gamma=1-lambda_2(P) be its spectral gap. On D>=2,
each solution has pi(b)<=1/2. The Rayleigh quotient of the centered indicator
of {b} yields

    gamma <= epsilon_b/(1-pi(b)) <= 2*epsilon_b.       (9)

A reducible chain simply has gap zero. For quantum-walk comparisons first
make the chain lazy so its eigenvalues are nonnegative. The associated
Szegedy phases include +/-2*arccos(1-gamma), of order sqrt(gamma) for small
gamma. [Somma et al.](https://arxiv.org/pdf/0804.1571) construct quantum
annealing using this square-root-gap relationship and gap-resolving operations.
Here their usual inverse-gap-dependent certificate does not become polynomial.
This is NOT a lower bound on every state-specific implementation of annealing;
small-gap eigenmodes may be irrelevant to a specially chosen path or input.

There are direct DYNAMICAL statements in a narrower setting. Starting a
classical chain at a known witness b, the probability of leaving b within T
steps is at most T*epsilon_b. For the symmetric Gibbs-parent Hamiltonian

    H=I-diag(sqrt(pi))*P*diag(1/sqrt(pi)),              (10)

reversibility gives H(c,b)=-sqrt(P(b,c)*P(c,b)) for c!=b. Thus

    Var_b(H)=sum_(c!=b) P(b,c)*P(c,b) <= epsilon_b,
    1-|<b|exp(-i*t*H)|b>|^2 <= t^2*epsilon_b.         (11)

For the last inequality subtract H(b,b)I, apply Duhamel to the initial basis
vector, and bound the norm of its departure by t*sqrt(Var_b(H)). This proves
an Omega(epsilon_b^-1/2) time requirement for constant escape under THIS
normalized Hamiltonian starting from a witness. Merely using quantum dynamics
to obtain a second solution from the first does not remove the bottleneck.
Polynomial rescaling only changes polynomial factors; exponentially rescaling
the generator is a resource cost, not a free speedup.

Equation (11) does not cover fresh cold starts, time-dependent excursions to
high temperature, extra noncommuting controls, nonlocal drivers, nonreversible
quantizations, or different Hamiltonians encoding the same solutions. A gap
upper bound alone must not be reported as a general search-time lower bound.

## 7. Countercontrols That Prevent An Overbroad No-Go

GLOBAL RESET: P(b,c)=pi(c) has gap one and samples Gibbs in one step. Its
parent Hamiltonian is I-|sqrt(pi)><sqrt(pi)|. It violates the locality
assumption; implementing its transition IS the unsolved Gibbs preparation.
Writing this dense matrix is not a polynomial algorithm or an addressing
oracle. This positive countercontrol checks the theorem's scope.

HIGH TEMPERATURE: at beta=0 the lazy single-bit hypercube walk has gap 1/m.
Its source-average witness probability is exactly 1/Q. Easy mixing without
solution weight does not satisfy the arithmetic interface.

SMALL GAP DOES NOT IMPLY HARD ARITHMETIC: use actual modular subset-sum
instances with all m=r-1 labels equal to an odd c and target t=c. Because
m<Q and c is invertible, solutions are exactly the weight-one assignments.
Two witnesses are trivial to output. More strongly, the entire Gibbs law is
classically samplable in polynomial time: sample weight j with probabilities
proportional to

    C(m,j)*u^HammingWeight((c*j mod Q) XOR c),

then choose a uniform j-subset. At u=1/r these are rational weights of
polynomial bit length, so ordinary exact random-bit sampling has polynomial
expected cost. No subset-sum or Gibbs oracle is hidden in this procedure.

Nevertheless, for alternating-bit c and even r, a single-bit move from a
weight-one solution has energy r/2 or r. Its local Metropolis escape is tiny.
The r=8 example has local spectral gap about 4.73e-8 despite its immediate
two-witness algorithm. It is a structured calibration, NOT a natural-source
positive result; equal-label instances have exponentially small prevalence.
It refutes interpreting (9) as hardness of the subset-sum instance itself.

Related small-gap behavior in random number partitioning has established
[adiabatic literature](https://arxiv.org/abs/quant-ph/0202155), but that model
and Hamiltonian are different. No theorem from it has been silently imported
to prove the modular residual-bit result here.

## 8. Executed Controls And Falsification Status

All controls below used independent bounded reference calculations, not a
scalable thermal solver. No fitting of an asymptotic exponent was performed.

For r=2,3,4 all 16, 512 and 65536 UNCONDITIONED (l,t) instances were exhausted.
The exact integer-scaled partition sums gave:

| r | E Z | Var Z | Ideal two-draw distinct-pair probability |
|---|---|---|---|
| 2 | 9/8 | 19/128 | .03125 |
| 3 | 32/27 | 244/729 | .0308535767468 |
| 4 | 625/512 | 945711/2097152 | .0297723066353 |

The partition moments, D factorial moment, and nine joint-neighborhood count
identities matched exact fractions. Three thresholds per size used
(k,h)=(min(1,m),0), (min(1,m),1), (min(2,m),0). All ideal pair probabilities
exceeded (3); good D=2,Z-D<=32 fractions were 1/16,21/256,357/4096.
Only the source identities are exhaustive here, not the asymptotic gap claim.

Seven explicit spectral controls used lazy single-bit Metropolis at u=1/r.
Six were sampled from the natural source CONDITIONED on D=2 solely to test
matrix identities; they are not unconditional success-rate estimates:

| r | labels l | target t | spectral gap |
|---|---|---|---|
| 6 | 0,19,37,2,12 | 37 | .00263248356 |
| 6 | 44,62,48,13,57 | 55 | .00282466440 |
| 7 | 71,110,15,42,51,59 | 92 | .000297266766 |
| 7 | 26,110,3,26,109,33 | 43 | .00129017438 |
| 8 | 182,80,164,107,50,238,117 | 247 | .000235488161 |
| 8 | 187,10,143,69,152,159,102 | 162 | .000259613455 |
| 8 | seven copies of 85 | 85 | 4.72749777e-8 |

The last row is the easy countercontrol. All seven matched detailed balance,
the Gibbs ground vector (maximum residual 7.74e-17), the indicator Rayleigh
bound, and the variance bound. Twenty-eight full matrix-exponential controls
at times .1,1,4,.2/sqrt(epsilon_b) obeyed (11). Seven global-reset matrices
had gap one; seven high-temperature hypercubes had gap 1/m. The easy family's
cardinality sampler exactly reconstructed its Gibbs probabilities.

The first r=6 control has adjacent solutions and zero energy barrier. It
correctly does NOT pass a positive-barrier gate. No instance was relabeled
isolated merely because the asymptotic natural bound is small eventually.

Exact binomial FORMULA evaluations, not large simulations, at
r=32,64,128,256,512 gave log2 bounds (6) of approximately
-12.71,-17.39,-25.98,-42.21,-73.70, and log2 escape bounds (8) at beta=log r
of -20.05,-38.65,-82.54,-184.85,-419.99 respectively.

Falsified proposed claim: a polynomial rapid-mixing Gibbs implementation for
this natural energy/source follows from cheap residual evaluation and the
usual quantum square-root-gap improvement. Neither sufficient sampling mass
nor polynomial precision supplies the missing nonlocal preparation.
Still open: a concrete arithmetic-aware sampler or quantum path outside the
declared local stationary dynamics, with natural-source coverage and cost.

## 9. Gemini Handoff And Research Filter

1. Integrate as a scoped arithmetic baseline/negative within the existing DCP
   solver workflow, not a new accepted candidate or a general annealing ban.
   Keep equilibrium pair probability, sampler runtime, quantum spectral gap,
   and actual measured two-witness success as DISTINCT evidence fields.
2. Reproduce the exact moment and neighborhood counts, then independently
   assemble the small Markov/Hamiltonian matrices and evolve basis states.
   Include all three positive scope countercontrols and the zero-barrier row.
3. A source certificate must name the residual-bit energy, uniform labels AND
   targets, move radius, temperature policy, stationary distribution, and
   reversibility. Do not apply (5) to arbitrary instance-adaptive temperatures
   or (9)-(11) to auxiliary-space/nonlocal/unrelated quantum dynamics.
4. Charge construction and coherent row access for every proposed transition.
   A supplied dense reset matrix, Gibbs state or full fiber table cannot pass
   the polynomial preparation gate. Local updates that are easy to compute
   do not pass the mixing gate solely because the state count is finite.
5. Run focused/full validation after implementation and preserve prior negative
   scopes. No production code, registry refresh or bulk tests were performed
   by this theory pass. Its notes join the infrequent bundled theory backup.
   Report discrepancies instead of adjusting
   tolerances or broadening conclusions to manufacture a successful report.

The next serious positive attempt needs a specific nonlocal arithmetic move,
a direct sampler, or a different collective measurement. Do not spend another
main-model pass retuning local cooling constants or interpreting a small gap
as proof that all such alternatives are impossible.

## 10. Nonlocal Restarts: Extract The Proposal Before Quantizing It

Follow-up derivation and checks, 2026-09-24. Still LOCAL DERIVATION / REVIEW
PENDING. This section tests the apparent nonlocal escape instead of assuming
that appending global restarts solves the preparation problem.

### 10.1 Independence Metropolis Has An Exact Gap

Let q be any fixed proposal distribution on the assignment space, independent
of the chain's CURRENT state. It may depend on the complete public instance.
For strictly positive pi, the independence Metropolis off-diagonal entries are

    P(x,y)=min(q(y), pi(y)*q(x)/pi(x)), x!=y,
    kappa=min_x q(x)/pi(x).

On a finite state space with at least two elements, its exact spectral gap is

    gamma=kappa.                                      (12)

This is established independence-sampler spectral theory, not a novelty claim;
see [Wang's exact convergence analysis and its finite-spectrum references](https://arxiv.org/pdf/2008.02455).
A short self-contained proof suffices here. Every entry satisfies
P(x,y)>=kappa*pi(y), including the diagonal since P(x,x)>=q(x). Minorization
gives gap >=kappa. At a minimizing state x, every off-diagonal transition is
kappa*pi(y). Its centered-indicator Rayleigh quotient is exactly kappa,
giving the reverse inequality. If q misses a state, kappa=0 and that state
is absorbing; no irreducibility claim survives. At q=pi the gap is one.

For the uniform global proposal q=1/M and any instance with D>=1, (12) gives

    gamma=Z/M.                                        (13)

Thus uniform global jumps remove the local r^(-Omega(r)) barrier, but leave
an exponentially small gap when Z is polynomial. At beta=log r, E Z<3/2,
so Markov bounds the source mass with D>=1 and gamma>=r^-c by
(3/2)*r^c/M. There is no inverse-polynomial source fraction with a polynomial
gap. The square-root-gap scale is the familiar exponential search scale, not
a new polynomial algorithm. This statement even grants the needed coherent
row access; implementing it must still be charged.

More generally q(x)>=gamma*pi(x) pointwise. If sampling q is classically
efficient and a polynomial gap is justified, directly sampling q already
has useful witness weight. The quantum annealing stage is not where a new
exponential advantage in this arithmetic task can be credited.

### 10.2 State-Dependent Choice From A Fixed Proposal Dictionary

Consider K distributions q_1,...,q_K, fixed after public-instance preprocessing,
and qbar=K^-1*sum_j q_j. The choice of j may depend arbitrarily on the current
assignment. Suppose the final reversible transition matrix has, for x!=y,

    P(x,y)<=sum_j w_j(x)*q_j(y),
    w_j(x)>=0, sum_j w_j(x)<=1.                       (14)

This includes properly Hastings-corrected state-dependent mixtures; ordinary
energy-ratio acceptance alone is generally WRONG for asymmetric proposals.
It also allows additional rejection/laziness. No individual component needs
to be reversible. Because the right side is at most K*qbar(y), stationarity
and the centered-indicator Rayleigh test at b imply

    pi(b)*(1-P(b,b))
       =sum_(x!=b) pi(x)*P(x,b)
       <=K*qbar(b)*(1-pi(b)),
    qbar(b)>=gamma*pi(b)/K  for EVERY b.               (15)

If each proposal is uniformly classically samplable, so is qbar: choose a
uniform j and draw once. A polynomial dictionary and a polynomial gap imply
a classical two-witness procedure without simulating the chain or computing
Z. All instance preprocessing, model training and proposal sampling costs
remain charged. A table containing solutions is not a cheap proposal.

### 10.3 Adding Local Moves Does Not Hide The Arithmetic Gain

Allow the more general off-diagonal domination

    P(x,y)<=L(x,y)+sum_j w_j(x)*q_j(y),                (16)

where 0<=L(x,y)<=1 is supported on distances 1,...,k. Ordinary mixtures of
local and dictionary proposals followed by correct MH acceptance satisfy this
condition. The full chain must still be reversible with stationary pi.

On the isolation event in Section 5, put

    tau=V_in*exp(-beta*(h+1)).

For any solution b, the incoming local stationary mass is at most tau/Z.
Repeat the argument for (15), retaining that extra term. Since D>=2 implies
pi(b)=1/Z<=1/2, it gives

    gamma <= tau/(1-pi(b)) + K*qbar(b)/pi(b),
    qbar(b) >= alpha*pi(b) for all solutions,
    alpha=max(0,gamma-2*tau)/K.                       (17)

The same proof allows the tighter per-instance cap
tau=max_(b solution) sum_(x:1<=distance(x,b)<=k) exp(-beta*E(x)); using this
cap computationally requires a CHARGED witness/neighbor calculation. The
analytic tau from Section 5 does not require enumerating unknown witnesses.

On the natural isolated source at the useful fixed temperatures, tau is
superpolynomially small. If gamma is inverse polynomial and K polynomial,
the nonlocal proposal collection ALREADY carries inverse-polynomial weight
on the witnesses. Local assistance cannot conceal this in a fast-mixing
certificate. This is a constraint on the declared thermal/proposal interface,
not on arbitrary state-dependent nonlocal moves.

### 10.4 An Executable Classical Extraction Rule

Let h_pi=D*(D-1)/Z^2 be the ideal Gibbs two-draw probability, not the energy
threshold h. Whenever qbar(b)>=alpha*pi(b) on all solutions,

    Pr[two independent qbar draws are valid and distinct]
        >=alpha^2*h_pi.                               (18)

A streaming solver is stronger than repeatedly discarding a valid first
witness. Draw from qbar, verify the modular sum, keep the first valid answer,
and continue until a DIFFERENT verified answer arrives or a charged cap is
reached. If h_pi>=h0>0, total valid proposal mass is at least alpha*sqrt(h0).
After one valid answer, the mass of the OTHER answers is at least
alpha*(D-1)/Z>=alpha*sqrt(h0)/2. Therefore, with

    L=ceil(2*log(2/delta)/(alpha*sqrt(h0))),            (19)

2L independent draws suffice for success at least 1-delta. Bound failure by
no first witness in the first L draws plus no different one in the last L.
The solver itself does not need to know D, Z, the witnesses, or whether the
instance satisfies h_pi>=h0. Its fixed cap uses the proved lower parameters.

If gap >=g, h_pi>=h0 and isolation all hold on source mass rho, use
alpha=max(0,g-2*tau)/K. The streaming solver succeeds on the full source with
probability at least rho*(1-delta), with the cost in (19). Inverse-polynomial
rho,g,h0 and polynomial K/cost give a polynomial CLASSICAL arithmetic solver.
Approximate proposal sampling with TV error epsilon per draw adds at most
2L*epsilon to the failure bound; accuracy is charged, not assumed exact.

Do NOT multiply a mean gap by an independently averaged Gibbs success. They
must hold on the SAME instances, or retain the exact weighted bound
E[alpha^2*h_pi]. A scope counterexample on the complete r=3 source sets
q=pi only when D<2, and uses a point mass on one solution when D>=2. Its
mean gap is 469/512, but all direct pair success and gap-weighted Gibbs pair
success are ZERO. Computing D here uses an exponential reference table;
the example is a logical countercontrol, not a proposed solver.

This is dequantization of a claimed THERMAL ARITHMETIC advantage only. A
genuinely polynomial classical subset-sum pair solver would itself be a
major development and would still feed the QUANTUM DCP phase readout.
Nothing here classically simulates that unknown phase source. If proposals
can be prepared only quantumly, the same extraction rule gives a quantum
arithmetic solver, not a classical one; the claimed novelty and cost belong
to that proposal preparation, not to an unneeded cooling stage.

### 10.5 Controls, Limits And Gemini Extension

The seven arithmetic instances in Section 8 were reused for bounded matrix
controls. Thirty-five independence chains used uniform, Bernoulli(.2),
Bernoulli(.8), exact Gibbs-table, and first-witness-biased proposals. Equation
(12) matched numerical gaps with maximum error 2.56e-15. The Gibbs-table and
witness-biased proposals are explicit reference controls, NOT available
polynomial samplers on the natural source. Seven missing-support controls
correctly had gap zero.

Fourteen state-dependent three-proposal dictionary chains matched (15) and
(18). Fourteen local/dictionary hybrids matched (17), including six with a
nonzero certified pair bound; detailed-balance residual was at most 1.74e-18.
All fourteen deliberately incorrect energy-ratio-only acceptances violated
detailed balance. This prevents accidentally testing a different stationary
distribution when state-dependent proposal choices are introduced.

For r=3,l=(1,7),t=0, sixteen exact streaming checks enumerated 1360 sequences
under four rational proposal laws. They matched the probability of seeing
at least two distinct witnesses:

    1-sum_(b solution)(1-qbar(F)+qbar(b))^T
         +(D-1)*(1-qbar(F))^T.

Four larger stream caps from (19) were evaluated using that exact probability
formula, NOT executed as long sample streams. Their failure probabilities
were below 2.6e-5 for the requested .05 error. The high-mean-gap/zero-pair
countercontrol was checked on all 512 r=3 natural instances.

Gemini: add the exact independence-gap certificate, proposal-dictionary and
hybrid domination checks, and streaming direct-proposal baseline to the SAME
thermal audit flow if implemented. Include the missing-support, wrong-Hastings
and disjoint-gap/coverage controls. Do not interpret reference q=pi as supplied
Gibbs access. Do not create another candidate merely for this extraction.

Uncovered mechanisms include genuinely state-dependent nonlocal arithmetic
with no polynomial fixed-proposal domination, sufficiently large implicit
proposal families, quantum-only proposal preparation, auxiliary-space or
nonequilibrium paths, and state-specific algorithms that do not require the
full spectral gap. A change of assignment coordinates can turn a local move
into a nonlocal move in the ORIGINAL variables; locality must be checked there.
These remain research questions, not presumed efficient escape routes.
