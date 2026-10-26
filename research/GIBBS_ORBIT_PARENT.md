# Spectral Repair Of A Gibbs Decoder: The Real Remaining Cost

2026-10-20. LOCAL DERIVATIONS REVIEW PENDING. Known PGM, singular-value
transformation and stochastic-Hamiltonian mechanisms; no novelty, efficient
span reflection, classical hardness or quantum speedup is claimed.

## Question And Portfolio Choice

Can a local parent Hamiltonian repair the orbit-span leakage of cyclic BPQM,
and thereby provide an efficient Gibbs sampler that is not classically matched?
This is a SPECIFIC proposed algorithm, not another dimension-based no-go.

The previous pass removed two false nonabelian exclusions. That reopens search
space but supplies no GI receiver. DCP still lacks a uniform finder; canonical
moment search has a classical falsifier. The new character-transform paper
operates on central data and does not supply an orientation receiver
([Muchane, Sections IV--V](https://arxiv.org/html/2610.16827v1)). The existing
cyclic Gibbs experiment instead has a precise obstruction: its root projectors
leave the actual codeword-state span. This pass tests a public repair of THAT
obstruction before paying for a large quantum implementation.

Result: spectral normalization DOES repair the measurement algebra, with a
uniform root gap. But implementing the span projector through the proposed
local parent inherits EXACTLY a matched classical heat-bath spectral gap.
Locality and frustration-freeness do not make the global projector free.

## Input And Exact Orbit Span

Input: public binary H with M columns and R rows, including dependent/zero
rows, and explicit signs J. Let C=ker H, dimension k=M-rank(H), and
W=rowspan H=C-perpendicular. The native Gibbs spin law is

    pi_J(x) proportional to product_j [1+c*(-1)^(J_j+(H^T x)_j)],
    0 <= c < 1, with c a public rational.

There is no planted secret, supplied PGM, partition oracle or free state.
The prospective upside is polynomial Gibbs sampling in a regime beyond
matched classical samplers IF the missing reflection has a new efficient
construction. No such advantage or classical complexity lower bound is known.
Retain affine-cluster, replica-exchange and exact factor-contraction baselines
from AFFINE_CLUSTER_NATIVE_PROBE.md on the SAME public source and output law;
the heat-bath comparison below adds a structural competitor, not the only one.
Use the same actual product-channel source as COHERENT_LOCAL_GIBBS.md.
In its Fourier data basis put

    w(y)=2^-M product_j [1+c*(-1)^y_j], phi(y)=sqrt(w(y)),
    psi_d(y)=phi(y)*(-1)^(d.y), d in C.

Codeword characters distinguish exactly the cosets s+W. Therefore their
span has the orthonormal basis

    v_s = sum_(y in s+W) phi(y)|y> / sqrt(q_s),
    q_s = sum_(y in s+W) w(y) > 0.

Let P=sum_s |v_s><v_s|. Its rank is 2^k, not the dimension of one Gibbs
sector. No q_s table is being supplied to the proposed scalable algorithm.
At c=1 positivity/invertibility fails and the rank can collapse: that endpoint
is explicitly rejected, not reached by continuity in an implementation claim.

## Constructive Repair: Normalize A Compressed Physical Bit

For systematic information coordinate i, let X_i flip Fourier bit i and set
C_i=P X_i P. In the v_s basis it pairs s with t=s+e_i+W:

    C_i v_s = alpha_(s,i) v_t,
    alpha_(s,i) = sum_(y in s+W) phi(y)phi(y+e_i)/sqrt(q_s q_t) > 0.

This is NOT an arbitrarily assumed well-conditioned decoder. Its gap has a
simple uniform proof. Remove the i-th product factor; let A0,A1 be the sums
of the remaining weights on sector words with bit i equal to0,1. Then

    q_s = [(1+c)A0+(1-c)A1]/2,
    q_t = [(1-c)A0+(1+c)A1]/2,
    numerator(alpha) = sqrt(1-c^2)*(A0+A1)/2.

Since q_s*q_t <= [(q_s+q_t)/2]^2 = [(A0+A1)/2]^2,

    sqrt(1-c^2) <= alpha_(s,i) <= 1, FOR EVERY code and syndrome.

Thus sign(C_i), restricted to P, is exactly the unweighted swap v_s<->v_t.
These signs COMMUTE, although the original compressed C_i generally do not.
Their common character eigenbasis is the code's global PGM basis. Extend
each sign as identity on P-perpendicular to obtain a clean reflection S_i.
Nondemolition readout uses H on a record, controlled-S_i, then H on that
record. Sequential information-root readout is therefore the global PGM,
not an independence approximation or a cloned computation tree.

**Access and costs:** if an efficient controlled reflection R_P=2P-I were
available, H-controlled-R_P-H block-encodes P. Two separate ancillas plus
physical X_i block-encode C_i with normalization ONE, using two controlled
span-reflection calls. Known sign/polar singular-value transformation uses
O((1-c^2)^(-1/2) log(1/epsilon)) such calls, up to standard clean-implementation
details. That is a conditional query cost, NOT an implemented circuit.
[QSVT](https://arxiv.org/abs/1806.01838) and
[quantum PGM/Petz implementations](https://arxiv.org/abs/2006.16924) are prior
art for spectral measurement synthesis; no new general PGM algorithm is claimed.

For k information coordinates, the full decoder/XOR/decoder-adjoint sampler
uses 2k controlled repaired-root reflections. If each has a UNIFORM clean
operator error <=epsilon on the relevant span, the hybrid contribution to
output TV is <=2k*epsilon, plus source/error budgets. Span-reflection error,
QSVT ancillas, synthesis, garbage cleanup and every failed flag must be paid.
The dense reference is not that implementation.
Positivity of these binary product amplitudes is essential to the gap/sign
argument; it does not give a DCP decoder for arbitrary phase-state sources.

## Actual Complete Sampling Experiment

`gibbs_orbit_parent.py` builds P by diagonalizing the explicit LOCAL parent
below on bounded controls. It does NOT obtain a normalized-coset mass table
or call an ideal PGM. Dense diagonalization is exponential and explicitly
limited to six clauses/four information bits. It is a physical reference only.

It executes the full program on the actual retained state:

    source -> A -> XOR record into source label -> A^dagger -> final Z/H.

Every record and original source label is kept; no cleared-label postselection
is used. In the stored Fourier basis the final Z/H is y->y XOR J. Uniform
affine lifting maps valid Fourier words back to original spins, including
all gauge fibers. ALL signs are checked against independently normalized
integer product weights, not energy or marginal-only comparisons.

The native cyclic control H=(25,26,12), M5, and the dependent/zero-row control
H=(25,26,12,25,0) each run at c1/5 and c13/20 over all32 signs. The report
stores every unconditional TV, abort, data purity, residual-label probability
and word error. Positive word error is compatible with exact Gibbs sampling;
the source label does NOT clear with probability1. This reproduces the known
global-PGM law through a different explicit spectral construction, not a
sampling advantage on these classically tractable finite graphs.

Actual numbers at c13/20: word error0.03939222593, raw compressed-root
commutator norm0.1157038193, repaired commutator below numerical tolerance,
and worst unconditional Gibbs TV below8e-16 across all128 complete controls.
These floating diagnostics verify the bounded representation, not exact
arithmetic, asymptotic gate costs or superiority over the existing global PGM.

## The Local Parent And Its Classical Counterpart

For each nonzero check h, pair y with y'=y+h. Define the local orthogonal
projector, on each pair, by

    L_h = 1/[w(y)+w(y')] * [[w(y'), -sqrt(w(y)w(y'))],
                            [-sqrt(w(y)w(y')), w(y)]].

All factors outside support(h) cancel, so L_h is check-local. Zero checks
contribute zero. A CNOT relabeling and controlled real Ry readout implement
each bounded local projector; an independent QR construction from the actual
deformed even-parity code agrees. Explicit rotation tables are only small
calibrations, not polynomial gate counts for growing check weight.

The normalized parent is L=(1/R) sum_h L_h. Its joint kernel is exactly
span{v_s}; it is stoquastic and frustration-free. NORMALIZATION by R matters.
Each sector s+W is invariant and has one positive ground vector.

Now define a legal classical walk on that SAME sector: uniformly choose an
original check h, then heat-bath between y and y+h with probabilities
w(y)/[w(y)+w(y+h)] and w(y+h)/[w(y)+w(y+h)]. Only local product ratios are
needed; no partition sum or exponentially sized table is evaluated.
Let K_s be this row-stochastic matrix, pi_s its stationary conditional law,
and D_s=diag(pi_s). Directly on every pair,

    L restricted to s+W = I - D_s^(1/2) K_s D_s^(-1/2).

This is an EXACT all-n identity, not a correlation between fitted gaps.
The quantum parent gap in that sector equals the classical walk gap.
Dependent checks change generator frequencies, and zero checks are lazy
steps. They must NOT be discarded to make an independent-generator proof fit.

For sign J, the map x->J+H^T x has equal fibers of size2^(R-rank H).
The quotient walk is the lumping of original random-scan spin heat bath.
Sample a uniform affine fiber at the end to recover the FULL Gibbs spin
law. The full spin chain can have extra gauge modes; its entire spectrum
must NOT be identified with the quotient-parent spectrum when rows depend.

This is the familiar stochastic-Hamiltonian correspondence in this specific
orbit-span setting. [Quantum simulated annealing](https://arxiv.org/abs/0712.1008)
already gives quadratic inverse-gap improvements. The broader stoquastic
literature, e.g. [Bravyi--Terhal](https://arxiv.org/abs/0806.1746), needs its
own assumptions; no blanket classical simulation theorem is imported here.

## What A Polynomial Gap Would Actually Imply

Put rho=(1-c)/(1+c), r=rank H, and d=max support(h). In every sector,
pi_min >= rho^M/2^r. The standard reversible-chain L2 bound gives

    TV(K_s^t(y,.),pi_s) <= (1/2)pi_min^(-1/2)*exp(-Delta_s*t).

Thus an inverse-polynomial Delta_s, with polynomial-bit rational c, gives a
POLYNOMIAL classical sampler on that sector as well. A uniform parent-gap
bound gives it for every sign. An average/typical-sector argument must retain
the actual sector distribution and charge bad-sector mass separately.

A conservative all-input bound exists but is usually useless:

    Delta_s >= rho^(M+d)/R, when r>0.

At c0 the nonconstant quotient characters have energy at least1/R. At c>0,
stationary min/max is at least rho^M and each flip rate is at least rho^d
times its c0 rate. Dirichlet-form comparison gives the displayed bound.
It is not obtained from a numerical eigenvalue. A singleton sector has zero
mixing cost, with NO positive excited-parent-gap assertion.

The exact rational budget certifier uses b=ceil(log2(1/rho)) and
t=ceil[(r+M*b+2f)/(2*Delta_lower)] to guarantee TV<=2^-f under true uniform
coins. A HUGE sufficient budget is not a lower bound or a slow-mixing proof.

The actual unfiltered(3,6) socket input at64 spins/128 clauses, seed29, runs
256 paid classical quotient updates and an independently verified affine
lift. It does not enumerate any sector, execute128 quantum wires, initialize
at stationarity, or claim a Gibbs/TV guarantee after that short budget.
The much larger uniform comparison budget is saved separately and NOT run.

## A Concrete Alternative: Source-Aware Gram Inversion

Follow-up2026-10-20, same producer, schema v2. The local-parent route is not
the only possible way to construct P. Let Phi have columns psi_(Gu), each
of norm1, N=2^k, and Gamma=Phi^dagger Phi. Then

    Gamma_(u,v)=c^wt(G(u+v)), P=Phi Gamma^(-1) Phi^dagger.

This is a proposed PUBLIC Gram-inversion implementation, not a supplied PGM.
Could recent source-aware linear solvers remove its cost? The primary
[Dalzell--Li--Su paper, Sections1.2--2 and4](https://arxiv.org/html/2607.07691v2)
retains the actual normalized block encoding. Its filtering cost expression
contains ||A^(-dagger) x||/(||x|| epsilon), not just a scale-invariant matrix
condition number. An improved solver does not itself construct a better
encoding or an affine dilation for this source.

Two actual public encodings are compared:

- Product-channel LCU: write the one-wire channel matrix as T=aI+bX,
  a^2+b^2=1,2ab=c. Its LCU normalization is a+b=sqrt(1+c). Restricting
  T^tensor M to computational code columns and multiplying by its adjoint
  block-encodes A_T=Gamma/(1+c)^M.
- Source purification: prepare N^(-1/2) sum_u |u>|psi_(Gu)>, SWAP its label
  with a logical target, and unprepare. The signal block is A_C=Gamma/N,
  NOT Gamma. The bounded program actually executes these gates on every
  logical input column and independently checks the LCU top block as well.

### Uniform All-Code Bound, Not A Finite Spectral Guess

The nonnegative Gram matrix has constant row sum

    W(c)=sum_(u in F2^k) c^wt(Gu) = ||Gamma||.

Systematic information coordinates, obtained by public Gaussian elimination
rather than promised special input structure, give wt(Gu)>=wt(u); hence

    W(c) <= sum_u c^wt(u) = (1+c)^k.

This proof needs NO code weight-enumerator oracle or exponentially sized
Gram table. Consequently, with r=M-k,

    ||A_T|| <= (1+c)^(-r),
    ||A_C|| <= [(1+c)/2]^k.

For every fixed0<c<1, k>=eta*M and r>=eta*M, BOTH norms decay exponentially.
Even choosing the better of these two encodings leaves this suppression.
There is no high-eigenvalue source window above an inverse-polynomial cutoff:
for sufficiently large M that cutoff removes the ENTIRE encoded support.

For every nonzero solution x, norm submultiplicativity yields

    ||A^(-dagger)x||/||x|| >= 1/||A||.

Thus the newer filtering solver's SPECIFIED COST EXPRESSION still grows
exponentially for these encodings, regardless of right-hand-side alignment.
This is NOT a runtime lower bound inferred from an upper bound, nor a general
quantum-query/circuit lower bound. It means that the cited resource theorem
does not certify a polynomial implementation by substituting this Gram access.
Rescaling a matrix in algebra is not a free stronger block encoding.

At c13/20 and half rate M=2k, purification is the better of these two:

    ||A_C|| <= (33/40)^k,
    ||A_C^(-dagger)x||/||x|| >= (40/33)^k.

The actual128-clause source has k64, giving a conservative coefficient
floor222304 before accuracy factors, repeated calls or synthesis. Larger
k16/64/256/1024 rows are ANALYTIC certificates only; no corresponding Gram
matrix, linear solver or quantum source was executed.

### Countercontrol Against An Overbroad No-Go

Take k disjoint equality pairs, C={(u1,u1,...,uk,uk)}. Then
W(c)=(1+c^2)^k exactly; the purification encoding's coefficient is
[2/(1+c^2)]^k, already about2.96e9 at k64,c13/20.
Nevertheless, the orbit span is a tensor product of known TWO-WIRE spans.
Apply each local readout, phase +1 when ALL pivot flags are zero and -1
otherwise, then reverse the local gates. Reversible AND gives a direct O(k)
reflection construction with O(k) workspace and paid rotation precision.
The bounded matrices at k1,2,3 verify that this is precisely2P-I.

The associated Gibbs model also has an exact independent-spin CLASSICAL
sampler. For the four pair-sign patterns its spin-one probabilities are
49/1138,1/2,1/2,1089/1138 at c13/20. So neither this easy control nor its
poor generic encoding is a candidate breakthrough or a hardness theorem.

The c0, k0 and r0 controls correctly have coefficient bound1 under the better
encoding. Do not extend the exponential claim to those endpoints or to a new
preconditioned/dilation encoding that has actually been constructed.

**Decision:** the two explicitly tested generic Gram routes do not remove the
reflection cost, even with the newer source-aware solver. Retain direct-native
constructions as live possibilities, but demand their actual circuits. Do
not add generic Gram/parent variants or pretend the paper supplied one.
A normalized solution-state routine also does not automatically implement a
coherent support reflection on arbitrary superpositions with clean work.

## Attempts To Prove This Wrong And Research Decision

- Check the sign/gap lemma on EVERY sector, not just typical q_s. Tests compute
  its squared coefficient as an exact rational and compare to1-c^2. Tiny
  q_s are not assumed away; constructing P can still encode hard normalization.
- The data actually stays in the span after repaired reflections; raw
  compressed bits need not commute. The full sampler, source labels and
  adjoint are executed, not reconstructed from successful word guesses.
- Exact rational detailed balance, full-spin lumping and uniform gauge lift
  are independently checked, including duplicate and zero checks.
- Whole-parent and sector spectra are finite NUMERICAL diagnostics only.
  Exact finite powers separately verify a conservative worst-start TV budget.
- The parent-gap equality does NOT prove an exponential circuit lower bound
  for R_P. A different algebraic/reflection construction might avoid this
  gap dependence. It also does NOT dequantize all BPQM or noncommuting Gibbs
  methods. Only the proposed gap-based local-parent route is classically matched.

Retain the constructive root-normalization lemma and exact comparator. Do NOT
build a large QPE/QSVT span filter merely because its terms are local. The
next genuine re-entry needs an explicit public span reflection/transport that
does not merely assume away the classical gap, or a different noncommuting
receiver with a natural hard sampling task. Otherwise pivot; do not generate
adjacent parent/gap variants or larger statevectors by inertia.

Reproduce with `python theorems/gibbs_orbit_parent.py --write` and
`python -m pytest -q tests/test_gibbs_orbit_parent.py`. Source-bound artifact:
`phase_workbench/gibbs_orbit_parent.json`. No central candidate/negative/proof
promotion or GPT commit/push. Optional CLI wiring belongs to Gemini.

Verification after the Gram-access pass:97 focused tests within246 connected
tests pass (86.20s). The connected
suite includes the actual coherent local/tree/erasure decoders, native classical
probe, exact factor reference and CLI parser. Existing Qiskit deprecation
warnings remain; no RuntimeWarning occurred. This is NOT the full repository
suite. Python compilation,12 site/root JavaScript syntax checks, site checks
and `python qsearch.py validate` pass; central registry counts are unchanged.
