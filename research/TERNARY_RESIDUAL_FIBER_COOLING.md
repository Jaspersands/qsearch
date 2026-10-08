# Residual-Aware Fiber Cooling: A Warm State Does Not Repair Cold Moves

LOCAL DERIVATION / REVIEW PENDING. Actual conditional parents, not a generic
annealing lower bound, accepted algorithm or novelty claim. This changes
the binary-energy proposal; its earlier uniform-state bound is NOT reused.

## A Different Constructive Hamiltonian

For original full native rows define E_y(x) to be the NUMBER of coordinates
where F(x) differs from y modulo q. With amplitude attenuation0<t<=1,
g_(y,t) is proportional to sum_x t^(E_y(x))|x>. Every k-word conditional
class has normalized vector with these same relative amplitudes. Projectors
onto those class vectors give H_(B,t)=I-Q_(B,t), with g_(y,t) a ground state.

These parents alter unmarked classes throughout the word space. They do not
satisfy the earlier binary-energy small-perturbation calculation. Actual
local tables cost3^k full native evaluations and no whole-fiber oracle.
Complete reference matrices are explicitly capped and exponential.

Investigate cooling from a GRANTED warm coherent Gibbs state at t0=1/2
using only colder parents t<=t0. Arbitrary signed schedules, target/label-
dependent block policies and additional diagonal controls are allowed.
Supplying that warm state is generous, not an implemented preparation.

## All-Word Native Boundary Energies

Every fixed nonzero small-support difference signature is uniform in Z_q^n.
Its number W of nonzero frequency coordinates is Bin(n,1-1/q). For h=floor(n/3),

    Pr[W<=h] <= 2^h E[2^(-W)] = 2^h*((q+1)/(2q))^n.

There are V=(1/2)sum_(j=1..k)binomial(M,j)6^j unoriented signatures.
A union bound gives bad-label mass delta<=min(1,V*2^h*((q+1)/(2q))^n).
On good labels, EVERY small-support move from EVERY full target-fiber word
has residual energy at least h+1. This covers all words, targets and
full-label/word-adaptive policies, without independence among signatures.
For M=poly(n), k=O(log n), delta decreases exponentially for sufficiently
large n. No fixed finite row with delta=1 is called informative.

Inside each block class there is at most ONE target word. Each target-to-
unmarked projector entry is at most t0^(h+1), since its normalizer is>=1.
The cross-block maximum row sum is at most (3^k-1)*t0^(h+1); its maximum
column sum is at most t0^(h+1). Convex block mixtures obey the same sums.
The Schur bound therefore gives

    ||Pi_y H_(B,t) (I-Pi_y)|| <= kappa=sqrt(3^k-1)*2^(-(h+1)).

Delete cross-fiber entries to obtain a block-diagonal reference evolution.
Diagonal controls and either sign of parent coefficient do not change its
fiber probability. The propagator difference has norm<=A*kappa, where
A is integrated absolute parent action. For ANY initial state with target
probability alpha, actual final target probability is at most

    min(1,(sqrt(alpha)+A*kappa)^2).

This is a boundary-coupling/state-transfer bound, not a claim from a small
spectral gap. The original large global signature space is never enumerated
to evaluate its population bound.

## How Much Target Mass Does The Granted Warm State Have?

Draw X uniformly from the ORIGINAL word cube before labels and let y=F(X).
This induces precisely the source's Born weights p_y. Set z=t0^2=1/4,

    Z_X=(1/D)sum_w z^(E_(F(X))(w)), D=3^M,
    mu=((1+(q-1)*z)/q)^n, mu2=((1+(q-1)*z^2)/q)^n.

Every distinct w has uniform difference from X. ANY THREE distinct native
words have a pointed2-by-2 unit minor (the existing batch-fiber argument),
so differences from X to two other words are jointly independent even at
composite q. Their weights are pairwise independent, not mutually IID.
For EACH fixed X,

    E[Z_X]=1/D+(1-1/D)*mu,
    Var[Z_X]=(D-1)/D^2*(mu2-mu^2).

Warm fiber probability is p_(F(X))/Z_X. Split at Z_X=mu/2, apply Chebyshev
to the lower-normalizer event and keep its RAW probability. Since mean
p_(F(X)) equals K=1/G+(1-1/G)/D,

    E_labels,X[alpha] <= min(1,2*K/mu+4*Var[Z_X]/mu^2)=a0.

For D>=G this is at most
4*(4/(q+3))^n+4*((q+15)/(q+3)^2)^n, hence exponentially small for q>=3.
This bound uses the whole IID native law, not empirical balance or a chosen
warm calibration. No source-conditional normalization erases bad labels.

Combining cold transfer with the bad-label event and Jensen,

    E_labels,X[final fiber probability]
       <= min(1,delta+(sqrt(a0)+A*kappa)^2).

Large symbolic ledgers keep rational directed square-root bounds. At the
finite controls some population bounds are vacuous; that is recorded.
Labels may determine the policy after the all-word event is established.
The action cap must apply uniformly to every instance, not only on average.

## Executed Controls And Scope

Exact n2/q9/M5 parents at t=1/2,1/4 use the original seed89881 source.
Full class matrices, residual energies, coherent Gibbs null-vectors and
cross-boundary Schur sums are recomputed. A finite two-step cold evolution
starts from its GIVEN exact warm vector and is checked numerically against
the actual finite boundary bound. It does not claim a compiled quantum
warm state, asymptotic solver or rigorous floating-point certificate.

The separate complete n1/q3/M2 population census checks all81 native label
matrices and all nine fixed ORIGINAL target words per matrix. Its exact
normalizer means and variances are independently checked, including zero
and repeated frequency coincidences. The triple-word unit minor is an
algebraic source property, not conditional independence given y and labels.

Decision: cold residual-parent evolution from this granted warm state is
not a polynomial-action population fiber compiler. This does NOT settle
preparation from t=1 using hot excursions, schedules adding non-parent
hopping, nonlocal moves, different encodings or general collective POVMs.
Hot evolution can change the state throughout the unmarked space and is
NOT covered by the binary-energy argument. A hot-stage constructive
operation with a demonstrable bias is the remaining question for this
proposal; another spectral-gap table would not answer it.

Falsifiers: actual local energy contradicts a complete signature boundary
certificate; a conditional class has two target words on good labels;
cross Schur sums exceed their row/column bounds; exact full label census
violates pointed-pair moments; cold dynamics violate the complete action
bound; a hot schedule inherits a cold-only certificate; warm preparation,
postselection or incoming source copies are left uncharged.

Gemini/Antigravity owns routine registry/CLI integration and production
validation. No accepted candidate, speedup or general quantum lower bound.
