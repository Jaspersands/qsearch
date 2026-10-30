# Native Noisy-Linear Records: Oracle-Sketch Transfer Audit

Status: LOCAL DERIVATION / SELF-CHECKED FINITE CONTROLS / REVIEW PENDING.
This is a rejection of one proposed polynomial-time recovery route. It is
not a lower bound for all native quantum algorithms, a refutation of the
source paper, a new hard problem, or an admitted speedup candidate.

## Question And Primary Source

Can streaming quantum oracle sketching turn the project's ORIGINAL noisy
linear records into a useful full-domain phase oracle at polynomial cost
in the native input parameters, without QRAM or an ideal inverse?

Primary source: Zhao et al., [arXiv:2604.07639v2](https://arxiv.org/abs/2604.07639v2),
revised 2026-10-01. Read Algorithm 1 (p.50), Theorem D.12 and its expected
channel interpretation (pp.53-55), and the correlated-data assumptions of
Theorem D.16 (pp.60-62). The IID Boolean theorem charges O(N/epsilon)
samples per phase query for a uniform N-point domain. Fresh-query composition
costs O(N Q^2/epsilon), not poly(log N). Its benefit concerns small quantum
memory and suitable data tasks, not arbitrary polynomial-time recovery of
static secrets. Theorem D.16 does not make frozen-bank replay IID.

PDF SHA256: b6b34b46e241c842e82d2576aff893fe46ec1f46fa4c15bec9a564a981c13f2f.
Our noisy matrix blocks need not commute at a repeated address. The proof
below is a direct adaptation, not an assertion that D.12 already proves it.

## Preserve The Original Input

Authority: `theorems/native_noisy_phase_input.py:prepare_inputs` and
`research/NATIVE_NOISY_PHASE_INPUT.md`, inspected read-only on 2026-10-24.
An original is (a,b), where a is uniform in (Z/qZ)^n, q=3^r, and

    b = <a,s> + E mod q.

The fixed unknown s is an integer-vector secret. Errors are IID, symmetric,
and independent of a. The usual native construction consumes two DISJOINT
originals per qutrit. Values and preparation inverses stay reduction-side;
the receiver gets only qutrits and public frequency labels. This audit uses
the ORIGINAL classical records reduction-side. It does not grant their
values, a replay oracle, or an ideal inverse to the copy-only receiver.

Write chi(u)=exp(2*pi*i*u/q) and kappa=E chi(E). The constructive simulation
and classical concentration comparison below assume 0<kappa<=1. Known
kappa at charged angle precision, or a separately justified robust
calibration, is needed for the displayed simulation time. A moment promise
does not supply its exact value. The support obstruction needs neither
known visibility nor a noise promise. At zero/complex visibility the
displayed positive-real simulation is not asserted.

Unique source IDs do not certify IID. Reusing one source ID with a new name
cannot evade the source-law promise. The local record adapter matches the
original fields but does not execute or replace `prepare_inputs`.

## Constructive Mean-Hamiltonian Route And Its Cost

Let D=q^n. Use an address register a and a single ancilla. For a record z:

    h_z = |a><a| tensor [[0,chi(-b)],[chi(b),0]],
    J_s = sum_a |a><a| tensor [[0,chi(-<a,s>)],[chi(<a,s>),0]].

Direct expectation gives E h_z=(kappa/D)J_s, E h_z^2=I/D, and J_s^2=I.
With t=pi*D/(2*kappa), exp(i*t*E h_z)=i*J_s. Applied to
|+_D>|0>, it produces the linear phase state on branch 1; inverse QFT
over (Z/qZ)^n then returns s. This is an IDEAL target, not supplied access.

Process M fresh independent originals using U_z=exp(i*theta*h_z),
theta=t/M. The mean one-step unitary is exactly

    B = [1+(cos(theta)-1)/D] I + i*kappa*sin(theta)/D J_s.

Independence, not commutativity, gives E[U_M...U_1]=B^M. The mean CHANNEL
is E[U_total rho U_total^dagger], not B^M rho (B^dagger)^M.

For a Hermitian norm-one block, the exponential's first-order remainder
has norm <=theta^2/2. Each address is hit with probability 1/D, so

    ||B - I - i*theta*E h_z|| <= theta^2/(2D),
    ||exp(i*theta*E h_z)-I-i*theta*E h_z|| <= theta^2*kappa^2/(2D^2).

Telescoping M contractions against M ideal unitaries yields

    delta := ||E[U_total] - i*J_s||
           <= pi^2*(D+kappa^2)/(8*kappa^2*M).

For completeness, if V is unitary, W=V^dagger U, and
A=E W-I, the channel difference is A*rho+rho*A^dagger plus the CP map
E[(W-I)rho(W-I)^dagger]. The CP map's diamond norm equals
||E[(W-I)^dagger(W-I)]||=||2I-EW-EW^dagger||<=2||A||.
Thus the full diamond distance is <=4delta and HALF diamond distance is

    <= min(1, pi^2*(D+kappa^2)/(4*kappa^2*M)).

The same estimate holds for an inverse or a coherently controlled call
with fresh originals; the identity control block has zero error. For Q
adaptive ideal calls, fresh independent blocks and ordinary channel
telescoping give sufficient total samples

    Q * ceil(pi^2*(D+kappa^2)*Q/(4*kappa^2*epsilon)).

The ledger replaces pi^2 by the strict upper bound 10. This is an upper
bound on sufficient samples for the construction, NOT a sample lower
bound for native recovery. It assumes discarding samples after the update
and no subsequent adaptive selection of future originals by their values.
Angles and controlled equality tests require polynomial work in n*log(q)
and gate precision per update. Gate synthesis errors, QFT errors and source
rounding are ADDITIONAL budgets; the implementation executes no gates.
Per-gate operator error <=epsilon/(Q*M) buys at most another epsilon of
half-diamond error, not the same already-consumed budget.

## Decisive Output-Level Support Obstruction

This argument is stronger than simply noticing a large sufficient bound.
Start at |+_D>|0> and use only address-local updates, each supported on a
sampled address. Their angles/order may be arbitrary. No address-mixing
step or ancilla flip on unvisited addresses is included. If v distinct
addresses have been visited, every unvisited branch-1 amplitude is zero,
and the norm at each address remains 1/sqrt(D). Therefore branch 1 is

    D^(-1/2) sum_(a visited) z_a |a>|1>,  |z_a|<=1.

Consequently:

1. P(branch 1) <= v/D.
2. P(Fourier outcome s AND branch 1) <= v^2/D^2.
3. Conditional on a nonzero branch-1 herald, the probability of ANY fixed
   Fourier outcome is <=v/D, by Cauchy-Schwarz.

The second inequality follows by bounding the Fourier amplitude by v/D.
The third uses |sum z_a chi(-<a,s>)|^2 <= v sum|z_a|^2. It is valid for
every realized bank, every noise value and even nonlinear observed phases.
No IID expectation or asymptotic hardness assumption enters this proof.

Noiseless distinct-address quarter turns attain both Fourier bounds:
z_a=i*chi(<a,s>), so the joint correct-herald probability is v^2/D^2 and
the conditional probability is v/D. This is an equality control in the
original model, not a new oracle benchmark or evidence of hardness.

Repeatedly replaying the same frozen bank cannot increase v. Amplifying
ONLY the branch-1 herald without changing its conditional state cannot
increase its v/D Fourier concentration. This observation does NOT rule
out new amplitude transformations, address mixing, classical processing
of b, other readouts, or all algorithms using the original records.
Constant single-trial correct-herald probability requires v=Omega(D).
The literal local-sketch-plus-Fourier construction is therefore not a
polynomial native decoder when log D=n*log q grows.

Resetting and repeating this same readout does not fix the cost. For runs
with M_j local updates, the union bound on ever directly outputting the
correct heralded answer is at most sum_j min(M_j,D)^2/D^2, which is at
most (sum_j M_j)^2/D^2. Thus constant success by direct repeated readout
still requires Omega(D) total updates. Combining many outcomes in a new
inference algorithm is outside this statement, not implicitly forbidden.

## Does Linear Address Compression Preserve The Signal?

Consider a fixed, secret-independent surjective homomorphism
L:(Z/qZ)^n -> (Z/qZ)^k and retain only u=L*a. A fiber is a0+ker(L), so

    E[chi(b) | L*a=u]
      = kappa * chi(<a0,s>) * mean_(x in ker L) chi(<x,s>).

The last factor is one when s annihilates ker(L) and zero otherwise.
By finite-group character duality, that annihilator is im(L^T), of size
q^k. For a uniformly masked secret independent of L, the first-harmonic
signal therefore survives with probability q^(k-n). This fact does not
require q to be prime. For coordinate projection it is simply the
condition that every omitted coordinate of s is zero modulo q.

This kills the direct idea of shrinking the address domain while retaining
the SAME first-harmonic mean rotation for arbitrary native secrets. It
does not rule out adaptive maps learned from the records, nonlinear
statistics, or higher harmonics. Those need their own algorithms and costs.
In particular, at q=9, s=(2,3), and u=a0, the first harmonic vanishes but
the third harmonic is chi(6*u). Calling the compressed record completely
uninformative would be false; a finite exact regression retains this case.

## Matched Classical Baseline

On the SAME IID originals, enumerate t in (Z/qZ)^n and compute

    T(t) = M^(-1) sum_j cos(2*pi*(b_j-<a_j,t>)/q).

E T(s)=kappa and E T(t)=0 for t!=s. Character orthogonality holds over
Z/qZ even when t-s is nonprimitive: some nonzero coefficient gives a
nontrivial character whose sum over all residues is zero. No finite-field
assumption is used. Hoeffding and a union bound over D candidates give

    P(any score error >= kappa/4) <= 2D exp(-M*kappa^2/32).

M >= 32*kappa^(-2)*ln(2D/delta) suffices. Compute each cosine with absolute
error <=kappa/8. On the good event, the true computed score is >=5kappa/8
and every wrong score is <=3kappa/8, hence the maximizer is unique.
Store the M records and evaluate candidates sequentially: polynomial
space and D*M*poly(n,log q,log(1/kappa)) time. This is an exhaustive
correlation attack, NOT a new efficient LWE solver. Rational arithmetic
or sufficient precision must be charged; the exact q=3 control avoids it.

For inverse-polynomial kappa, the classical attack uses polynomially many
originals and has the SAME D leading exponential factor as the necessary
number of local updates for constant correct-herald success. The literal
sketch route cannot provide a Shor-level time separation from this upper
bound. This is not a classical lower bound, and stronger lattice attacks
can only make this route less competitive. If kappa is exponentially small,
neither displayed algorithm obtains a polynomial native recovery claim.

For the previously considered q=3^(2n), D=3^(2n^2). Large-n ledger rows
use kappa=1 as a favorable limiting cost, NOT as a hard source instance;
noise-free records themselves admit much faster algebraic recovery.
The same support bound remains valid for the actual noisy input.

## Adversarial Checks And Remaining Escape Routes

- Could the published generic lower bound prove native hardness? No. Its
  data/problem promises cannot be imported to a fixed linear secret.
- Could small quantum memory alone be a breakthrough here? No evidence:
  the matched exhaustive classical attack already uses polynomial space.
- Could the source's second moment normalize the mean rotation exactly?
  No. Known visibility is an additional premise or calibration cost.
- Could expected-unitary convergence imply a nearly pure realized state?
  No. The mixing bound concerns the mean physical channel with discarded
  fresh randomness; it does not certify each frozen realization.
- Could unseen labels be covered by replay or postselection? Not under
  the stated local updates/herald. The support proof is realization-wise.
- Could a fixed linear compression simply reduce D? Only when the secret
  annihilates its kernel for this harmonic; higher-harmonic leakage is not
  ruled out and does not by itself give complete native recovery.
- Could arbitrary quantum processing evade the support proof? Yes. It
  would need a NEW specified constructive mechanism, not this argument.
- Is this an independent proof review or formal proof? No. These are local
  deductions with exact finite controls and numerical channel checks.

Do not extend this line with larger occupancy sweeps or a new generic
oracle family. Reopen it only for a concrete native algorithm that changes
the information-processing mechanism: e.g. address mixing with a proved
poly(n,log q) recovery and complete source/error accounting. Otherwise
return to actual source construction or a different live algorithmic route.

## Verification And Integration

`native_sketch.py` provides exact sparse quarter-turn/cyclotomic controls,
the support/resource ledger, an exact ternary exhaustive baseline, and a
capped actual mean-channel calculation. `test_native_sketch.py` tests their
mathematical identities, limits and access guards. `replay.py` emits the
negative source-transfer receipt. Finite fixtures include deterministic
balanced-noise records and are labeled as such, not IID performance runs.

These files are outside the unverified migrating checkout. No CLI, UI,
registry, source/staging, Git or migration state has been changed. See
HANDOFF.md for bounded mechanical integration after a verified local copy.
