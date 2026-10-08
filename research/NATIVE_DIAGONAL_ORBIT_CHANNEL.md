# Native Word-Orbit-Preserving Readouts Collapse To One Quantum Copy

LOCAL DERIVATION / REVIEW PENDING. This is a source-specific channel
simulation, not classical dequantization, a new quantum algorithm, or a
lower bound on arbitrary collective receivers. Exact controls use the
original [native cyclotomic source](https://arxiv.org/html/2609.34996v1),
not new oracle problems. External mathematical/literature review is required.

## The Restriction Is Observable, Not A Rank Assumption

For M originals with public frequency vectors a_i in A=(O/pi^r)^n,
write each computational word uniquely as x_i=v_i+j, v_1=0, all modulo3.
The simultaneous-rotation orbit has three words indexed by j. Its projector
Pi_v is public and secret-independent. The synchronized action

    R_a(g)=tensor_i R_(a_i)(g)

shifts ALL word coordinates by the same rotation and adds diagonal phases.
It preserves every Pi_v. Arbitrary auxiliary/group unitaries, group
measurements, public-label-dependent group filters, the known relative
orbit preparation and its inverse also preserve them. Adaptive group
measurement transcripts do not undo this conservation.

More generally the result applies when every complete operation preserves
these orbit subspaces and the final observable does not interfere them.
The observable may read the orbit label and its within-orbit qutrit. It does
NOT apply to independent per-copy rotations, seed operations mixing offsets,
or a final measurement with cross-orbit matrix elements. Such operations
are allowed in the actual quantum model; the theorem does not forbid them.

If the original seed is finally discarded, the surviving auxiliary channel
is unchanged by initially pinching it into its Pi_v blocks. That is equality
of the specified OUTPUT channel, NOT equality of the original input states.

## Exact Original-Source Factorization

Set lambda_0=0, lambda_1=1, lambda_2=1+zeta. The identity

    lambda_(v_i+j)=lambda_(v_i)+zeta^(v_i)*lambda_j

gives an effective public frequency

    u_v=sum_i zeta^(v_i)*a_i.

The original phase batch restricted to orbit v is its native qutrit psi_(u_v)^s,
embedded as j -> (v_i+j)_i, with an irrelevant secret-dependent GLOBAL phase
and raw weight 3^(-(M-1)). No simulator computes that global phase. The same
embedding intertwines the full known tensor group action with R_(u_v)(g).
Every group-only instrument therefore acts on a mixture of these qutrit
branches. It cannot use their discarded relative phases.

## A REAL One-Copy Simulator, Preserving All Public Labels

A mixture formula alone would not supply conditional quantum states for free.
The simulator instead takes ONE actual original native sample with observed
uniform frequency u. It chooses v uniformly with v_1=0 and chooses M-1 fresh
UNIFORM CLASSICAL auxiliary rows a_2,...,a_M. Set

    a_1=u-sum_(i>=2) zeta^(v_i)*a_i.

This is a bijection for each v. Thus the synthetic (a_1,...,a_M,v) has EXACTLY
the original full-uniform IID frequency record and orbit-weight distribution,
including their correlations with u. No original labels are discarded or
averaged away. Prepare v as classical ancillas and map j -> (v_i+j)_i with
public ternary additions; run the original preserving readout on that encoded
qutrit. No copies of psi_s, unknown inverse, postselected branch supply or
secret-dependent global phase are needed. Auxiliary-row arithmetic and the
embedding cost polynomially in M,n,r, apart from the original receiver cost.

This equivalence is for the actual full-uniform IID frequency prior. Given an
arbitrarily preselected frequency cohort, the branch formula still holds but
the one-fresh-copy simulator does NOT magically supply its required u_v.
Biased/selected/noisy sources or correlated labels require separate admission.

## Consequence For Full Secret Recovery

Conditional on all public data, the simulator has only a three-dimensional
secret-dependent quantum input; the public data distribution is independent
of the secret. For a uniform prior on K possible secrets and any decoder,

    mean correct <= min(1,3/K).

Indeed rho_s<=I and sum_s M_s=I give sum_s Tr(M_s rho_s)<=3. Public randomness,
ancillas, adaptive operations and unlimited runtime cannot enlarge this
information bound. Full ring secrets have K=3^(nr); integer-embedded secrets
have K=3^(n*ceil(r/2)). The bound applies to the specified preserving receiver
regardless of how many original copies it was nominally given. It is not a
bound on the original unrestricted batch, which can retain much more information.

For a joint original-input trace-distance error eta, the raw success bound
increases by at most eta through contraction. Marginal error bounds alone
do not certify eta. Gate/compiler approximation needs its own aggregate
complete-channel budget. Neither hardware compilation nor noise certification
is supplied by these finite exact controls.

## Explicit Escape And Research Decision

At secret0 the original M-qutrit batch is |+>^tensorM. A seed Fourier
measurement asking whether all qutrits are |+> accepts with probability1.
The orbit-pinched state accepts with probability3^(-(M-1)). That elementary
countercontrol distinguishes the states and deliberately breaks the readout
restriction. It proves this is not an unrestricted impossibility argument;
seed mixing itself is possible and cheap, but this contrast is not a decoder.

STOP optimizing a single synchronized orbit-register receiver whose final
readout never accesses cross-word-orbit coherence. Neither deeper relative
reflections, more original copies, adaptive group filters nor synthetic
high-rank projectors solve its missing information. A constructive proposal
must specify a seed operation or collective readout that ACTUALLY couples
different offsets, or use genuinely independent per-copy group actions.
Then charge its source access, error and full growing-parameter decoding cost.
Consult the existing weighted-fiber-erasure, ridge and native path results
before recycling an already-tested seed-mixing proposal.

The producer checks four original-source cohorts, including vector dimension2,
larger roots, and M3/M4. It verifies ALL words/orbits and selected public
induced actions, then runs three rounds of a label-dependent group unitary,
coordinate reflection and relative orbit reflection. The independent
Q(zeta_9) checker reconstructs both whole output channels exactly, including
every complex density entry, without reading producer matrices as premises.
General theorem review, novelty review and a useful nonpreserving receiver
remain open.
