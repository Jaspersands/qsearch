# Structured EDCP: Off-Fiber Annealing Still Has A Sparse-Block Bottleneck

Date: 2026-09-25. LOCAL DERIVATION / REVIEW PENDING.

## 1. What This Pass Adds

The earlier local-move theorem required exact fiber preservation. Merely
allowing off-fiber states appears to evade it. This pass analyzes that escape
for a natural soft constraint: a graded Gaussian penalty on the modular
residual. The conclusion is still a small reversible-chain spectral gap on
most source-weighted targets, even though the chain CAN leave the exact fiber.

The new argument uses low-energy CELLS, not isolated low-energy states.
Normalizing the first public label to one creates cheap within-block moves;
ignoring them would make the proof false. These moves remain inside a cell
and do not connect the many different conditional witnesses.

This constrains reversible sampling and its gap-based quantizations for the
specified coefficient representation, stationary law and sparse-block move
support. It is NOT a gap theorem for arbitrary quantum Hamiltonians, a lower
bound on every annealing method, or an impossibility result for structured
EDCP. Global arithmetic circuits, different representations and nonstationary
preparations remain open. No independent proof review or novelty claim.

## 2. Soft Conditional States And Their Exact Error Ledger

Let mu(c) be the known product coefficient-Gaussian probability law on
Z^(d*L), with probability width s_G=sigma/sqrt(2), and let

    f(c)=sum_l a_l*E(c_l) mod Q,
    r(u)=Pr_mu[f(c)=u],      Q=q^d+1.

The following probability identities also hold for a finite coefficient
source. Let w:Z_Q->[0,1] satisfy w(0)=1 and define

    S_w=sum_z w(z),
    Z_u=sum_c mu(c)*w(f(c)-u),
    pi_u^w(c)=mu(c)*w(f(c)-u)/Z_u.                           (1)

For r(u)>0, the positive-amplitude soft state sum_c sqrt(pi_u^w(c))|c>
has squared fidelity with the exact weighted fiber equal to

    F_u=r(u)/Z_u.                                          (2)

This is because the weights on the exact fiber are unchanged. Preparing
pi_u^w is the proposed task, not an available sampling oracle.

Set X_u=(Z_u-r(u))/r(u). Averaging over the SOURCE target u~r gives

    E_r X_u <= S_w-1,
    E_r F_u >= 1/S_w,
    Pr_(u~r)[F_u<7/8] <= 7*(S_w-1).                         (3)

The first inequality sums Z_u-r(u) over supported u; omitted zero-r fibers
are nonnegative. Jensen gives the second and Markov gives the third. These
claims need neither uniform r nor independent error rows in the original
classical source. They concern the ideal coefficient phase source itself.

If mu assigns mass at most eta outside the coefficient box Omega_R, then

    E_(u~r) pi_u^w(Omega_R^c) <= eta*S_w.                    (4)

Indeed r(u)/Z_u<=1; sum first over u and then over outside coefficients, and
use sum_u w(f(c)-u)=S_w. This source-weighted argument avoids the incorrect
pointwise tail bound eta/r(u), which is generally much too large.

## 3. The Low-Residual Cells

Assume d>=2 is a power of two, q>=3, 2R<=q-1. Condition the FIRST scalar
label to be a unit and divide all labels and targets by it, so a_1=1 and
a_2,...,a_L are still independent uniform in Z_Q. This defines the residual
coordinate in which the penalty is evaluated. The unit-label selection cost
must be charged in an actual workflow; arbitrary relabeling is not free.

Choose an integer W with 1<=W<Q/4. Let

    B_u={c: ||f(c)-u||_torus<=W},
    N_R=(4R+1)^d-1,       G_R=(4*R^2*d)^(d/2).

The earlier negacyclic norm argument proves
gcd(Q,E(Delta))<=G_R for every nonzero coefficient difference
Delta in [-2R,2R]^d. For a multiblock difference with at least ONE nonzero
block other than the first, a random remaining label makes its residual
uniform on a coset of a subgroup of Z_Q. The chance that it lands in an
interval of 4W+1 residues is at most (4W+G_R)/Q.

Consequently, with failure probability at most

    delta_cell=min(1, ((G_R+4W)/Q)
                       *sum_(j=1)^min(b,L) binom(L,j)*N_R^j), (5)

there are NO <=b-block transitions between two states in Omega_R intersect
B_u that change any block other than the first, simultaneously for EVERY u.
Their residual difference would have torus norm at most 2W, contradicting
the bounded-difference event used in (5). The union bound over differences
already covers all u; an additional factor Q is not needed.

There CAN be transitions changing only the first block. For example, changing
its lowest coefficient by one changes f by one. Thus partition Omega_R
intersect B_u into cells indexed by the coefficients of blocks 2,...,L.
The surviving low-residual transitions remain inside individual cells.

Each cell contains at most ONE exact-fiber state in Omega_R, because a_1=1
and E is injective on [-R,R]^d. This injectivity is why the pivot block can
be treated as a cell, rather than incorrectly declared immobile.

## 4. A Gap Bound For Every Reversible Chain On This Support

Fix good labels from (5) and a target satisfying:

    F_u>=7/8,
    max_c Pr_mu[c | f(c)=u] <=1/8,
    pi_u^w(Omega_R^c)<=gamma_tail<=1/8,
    r(u)>=tau>0.

The soft mass of each low-residual cell is at most 1/4: its one possible
exact-fiber atom contributes <=1/8, and all non-fiber states together
contribute <=1-F_u<=1/8. The total mass of these cells is at least
F_u-pi_u^w(Omega_R^c)>=3/4. A greedy union A of whole cells therefore has
pi_u^w(A) in [1/4,1/2].

Let

    alpha_W=max_{||z||_torus>W} w(z).

A <=b-block chain cannot cross from A to another low-residual cell inside
Omega_R. All crossing flow enters Omega_R^c or B_u^c. By stationarity,

    flow(A,A^c) <= pi_u^w(Omega_R^c)+pi_u^w(B_u^c)
                 <= gamma_tail+alpha_W/Z_u
                 <= gamma_tail+alpha_W/tau.

For ANY reversible discrete-time chain with stationary law pi_u^w and that
move support, the indicator Rayleigh quotient proves

    spectral_gap <= 8*(gamma_tail+alpha_W/tau).              (6)

No Metropolis proposal, detailed acceptance formula or prior-reversible
proposal assumption is needed. The chain may use label-dependent moves and
may leave the exact fiber. It is the move support and stationary probability
of crossing between cells that impose the obstruction.

## 5. How Often The Premises Hold

Let mu_max=theta(s_G)^(-d*L), the largest untruncated prior atom. For any
labels, simple source-weighted counting gives

    Pr_(u~r)[r(u)<tau] <= Q*tau,
    Pr_(u~r)[max_c Pr[c|u]>1/8] <=8*Q*mu_max.

The second follows from max_c Pr[c|u]<=mu_max/r(u). Combine these with
(3), (4) and Markov. Outside a joint exception of probability at most

    delta_cell + Q*tau + eta*S_w/gamma_tail
      +8*Q*mu_max +7*(S_w-1),                               (7)

all the premises of (6) hold, provided gamma_tail<=1/8. Cap probabilities
at one, retain failed premises, and do not confuse a mean source guarantee
with a pointwise guarantee for every u.

For the Gaussian prior,

    eta <= d*L*s_G^2/(pi*R)*exp(-pi*R^2/s_G^2).

Use theta(s_G)>=s_G if an explicit prior-atom upper bound is preferable to
evaluating an infinite Gaussian sum. Physical source contamination and errors
in comparing finite/untruncated phase sources are additional obligations.

## 6. A Graded Gaussian Penalty At The Audited Parameters

Take

    w_beta(z)=exp(-beta*||z||_torus^2),
    S_w <= 1+2*exp(-beta)/(1-exp(-3*beta)),
    alpha_W=exp(-beta*(W+1)^2).                             (8)

The first is a finite-modulus upper bound using the infinite Gaussian tail;
it does not double-count the even modulus midpoint as an exact equality.

At q=nextprime(d^12), R=d, sigma=sqrt(d), L=288, choose

    tau=exp(-d)/Q,
    gamma_tail=sqrt(eta*S_w),
    beta=d,
    d*W^2 >= bit_length(Q)+5*d.                             (9)

The last inequality is an EXACT integer sufficient certificate. Since
bit_length(Q)>=ln Q, it implies alpha_W/tau<=exp(-4d).
Equation (6) is then exponentially small in d, while (7) is dominated by
about 15*exp(-d). This does not rely on a prime approximation for Q.

110-digit analytic references, not interval-certified decimal enclosures or
executed high-dimensional chains:

| d | W | log10 delta_cell, b=2 | log10 Gap Upper | log10 Total Exception Upper |
|---:|---:|---:|---:|---:|
| 64 | 9 | -881.3993 | -84.6833 | -26.6188 |
| 256 | 11 | -4850.1785 | -346.3425 | -110.0033 |
| 1024 | 12 | -24655.5439 | -1393.8825 | -443.5415 |

### This Is Not An Artifact Of Exponentially Accurate Preparation

The same gap conclusion already holds at FIXED beta=4*pi. Then
7*(S_w-1)<=0.000048822793, independently of d. Choose the integer W by

    12*W^2 >= bit_length(Q)+5*d,

using 4*pi>12. W=21,47,104 at the three points. The gap still obeys the
same exponential-scale bound, now on a source fraction at least roughly
0.999951 after the other explicit losses. Thus accepting constant preparation
error does not rescue this sparse reversible annealer.

This theorem is about the stated graded residual penalty, not every possible
continuation path. A generic algorithm whose polynomial guarantee assumes an
inverse-polynomial gap for these stationary distributions fails that premise.
An upper bound on a chain gap is NOT by itself a universal quantum runtime
lower bound. Avoid that extrapolation.

## 7. Controls And Attempts To Break The Argument

No production integration or full-suite run. Seed 20260925.

1. Four exact approximate-difference ensembles used d=2,R=1,L=2,W=1,
   a_1=1 and q in {17,31,67,257}. Bad second-label counts were respectively
   234/290,250/962,250/4490,250/66050. The first three union bounds were
   vacuous. The last bound was 0.11336866 versus actual 0.00378501.
   Independent coefficient-pair enumeration at all 5,742 second labels in
   the first three moduli exactly matched the congruence construction.
2. Seventy-two arbitrary finite source/weight cases checked (3)-(4), including
   sources with empty fibers. The average tail charge, fidelity bound and
   fidelity-failure bound all held. No near-uniform-r premise was smuggled in.
3. Twelve full state-space cut checks used q=17,d=2,L=4,R=1,W=1 and labels
   [1,10,21,31]. The prior was UNIFORM on the 6,561 coefficient states:
   this is a probability/graph control, not the large-d Gaussian source.
   At beta in {3,6}, targets {0,1,17,53,101,200} all passed the fidelity and
   diffuse-atom premises. Each greedy union had mass between 1/4 and 1/2;
   there were no crossing edges within the band. Direct reversible Metropolis
   flow and its Rayleigh quotient respected (6). For beta=6,u=0, the cut
   quotient was about 8.87e-13 versus upper bound 1.17e-7. This quotient is
   an UPPER bound on the gap, not a measured eigenvalue. Underflowed reference
   weights were below a total unnormalized 6561*exp(-700); Z stayed bounded
   below by the nonempty exact-fiber mass.
4. Three growing reports checked integer W, the bounded-difference count,
   the source-tail/atom terms, the low-r exception and both penalty choices.

The failed idea was treating all low-residual states as isolated. The unit
first label supplies an immediate counterexample: change c_(1,0) by one.
The cell partition repairs this, and the finite cut checks explicitly retain
those moves. Also, small support may give singleton fibers and invalidate
the diffuse-atom premise; those instances must not be declared slow by (6).

Nonlocal transitions, an alternative coefficient basis, a different potential
with a different low-energy geometry, nonstationary or non-reversible quantum
preparation, and direct discrimination without these conditional states are
not excluded. A speedup must explain the specific escape, not just rename
the same Metropolis chain as quantum annealing.

## 8. Handoff And Next Research

Gemini: implement this only as a source-weighted annealing diagnostic. Retain
the pivot normalization, approximate-difference event, cells, stationarity,
tail ledger and failed-premise controls. Do not label (6) a general Hamiltonian
gap or state-preparation lower bound. Count a Rayleigh quotient as a gap
UPPER bound. Do not run large local-walk sweeps to rediscover the obstruction.

The mathematical target has narrowed to a genuinely different nonlocal map
or nonstationary coherent construction. The companion
`STRUCTURED_EDCP_POLAR_NORMALIZATION_AUDIT.md` audits generic polar/QSVT and
projection-based escapes. A cheap formula for a soft state is not a cheap
preparation or reflection about it.

## Sources And Dependencies

- Somma, Boixo and Barnum, *Quantum Simulated Annealing*,
  [arXiv:0712.1008](https://arxiv.org/abs/0712.1008). Their inverse-square-root
  stochastic-gap dependence motivates checking the ACTUAL chain gap. This
  note's source-specific cell theorem is not a theorem attributed to them.
- `STRUCTURED_EDCP_LOCAL_MOVE_OBSTRUCTION.md`: integer negacyclic norm and
  exact-fiber predecessor. The current argument permits off-fiber moves.
- `STRUCTURED_EDCP_CONDITIONAL_CORE_BARRIERS.md`: the conditional-state target
  and why a succinct arithmetic circuit is not excluded by large tensor rank.
- Source and width premises remain those of the upstream/joint-source notes,
  including their review-pending status and numerical implementation audit.
