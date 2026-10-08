# Depth-Independent Native Ridge Cancellation

IMPLEMENTED / LOCAL DERIVATION REVIEW PENDING. A source-accounted native
phase-shaping factory, not a full-root decoder, IID source acquisition from
classical data, new asymptotic speedup or cryptographic attack.

## Exact Low Relation At Every Native Depth

Fix n secret components, d data coordinates and retained root q=3^r.
Acquire B distinct original-source programs using the actual even-level2r+2
to odd-level2r+1 packet maps. Each program uses K=n+d odd inputs, obtained
from K disjoint original windows of size(n+1)^2. Measure source pointers,
outer syndrome and surplus free coordinates; accept every outcome. The
first d free coordinates are selected from low Gaussian rows only.

Represent Q_j using the compact native ridge schema at numerator modulus
N=3*q with a SHARED denominator3:

    Q_j,l(z)=(sum_L T_j,L,l(L*z) mod N)/3,
    T(0)=0, T(2)=2*T(1) mod3,
    sum_L a_j,L,l*L=0 over F3, a_j,L,l=T_j,L,l(1) mod3.

Canonical projective directions have their first nonzero coordinate1. The
ambient number is P=(3^d-1)/2. The coefficient-to-vector map a->sum_L a_L*L
has rank d, since the ambient dictionary contains coordinate axes. Therefore
the n-component signatures lie in a vector space of dimension at most
n*(P-d). B=n*(P-d)+1 supplied programs guarantee a nonzero F3 relation c.

Only occupied NONZERO LOW signature keys are stored. For observed k keys of
span rank s, the sharper conditional dimension bound is n*(k-s). This is a
bound for the PRESENT cohort, not a promise that future sources introduce
no new keys. Signature rank, both bounds and every relation row are checked.
The selector chooses a maximum-support nullspace basis vector, ties by
canonical order, and reads no high digits or measured injection outcomes.
This policy exercises nontrivial combinations when possible; it is not an
optimal source/time policy. All acquired programs are charged regardless.

Prepare a known data/reference Bell pair. For each c_j!=0, inject the one
supplied program using SUM-c_j and measure m_j. Every outcome has probability
3^-d even on arbitrary reference-entangled data. Each unknown state is used
once; coefficient2 is a domain sign, not two copies, conjugation or an
unprovided inverse. The new ridge table is

    T_j,L,l(L*m_j+c_j*t)-T_j,L,l(L*m_j).

Its coefficient mod3 is c_j*a_j,L,l, independently of m_j. Consequently
EVERY aggregate ridge table divides by3 for EVERY transcript. Only now may
each table be divided separately. Its values live at the same retained root
q=3^r; the exact local valuation certificate gives global degree<=2r rather
than2r+1. No high-order tensor, exponential data table or secret phase query
is required by the construction. The output Choi program can be un-copied
with known inverse SUM. Large bounded replay tables are calibration only.

## A Source-Law Bound That Does Not Grant A Decoder

Assume independently supplied uniform ORIGINAL full frequency pairs modulo
3^(r+1), across ancestors and secret components. Conditional on all original
curvatures, each nonempty fixed-window support has a pivot at pointer0.
Its pair is uniform on an affine frequency coset; summing the other pointer-
rotated pairs makes the odd child uniform on H={c-2a=0 mod3}. Supports are
disjoint. This is the same conditioned-pivot derivation as the previous
field-root factory, now at the full larger modulus. Pointer outcomes are
uniform independently of phase labels because source amplitudes are flat.

The full odd frequency chart is bijective:

    a=ell+3alpha, c=2a+3delta mod3^(r+1),
    ell in F3, alpha,delta in Z_(3^r), independent uniform.

Condition on low ell rows, delta, actual source outcomes and injection words.
The source frame t_i(z)=b_i+D_i*z is low-defined and has full column rank d.
After kernel division, the phase is

    fixed_low_carry(z)
    +sum_i alpha_i*(t_i(z)-b_i)
    +sum_i delta_i*(1[t_i(z)=2]-1[b_i=2]) mod3^r.

Reducing this CLASSICAL public function modulo3 makes the alpha contributions
purely linear with coefficients alpha^T D mod3. One selected full-rank frame
supplies a uniform independent coefficient vector in F3^d, componentwise.
Low-only relation selection preserves alpha independence; injection outcomes
are uniform independently of every program phase. Its domain sign is
nonzero, so the selected alpha linear map remains surjective. The other
contributions cannot destroy uniformity. After per-key division the complete
Q mod3 is ordinary quadratic (a sum of arbitrary three-entry ridge tables),
whose linear coefficients beta_l are independent uniform conditional on
its quadratic matrices and the stated low/delta transcript.

This conditioning EXCLUDES alpha/full high linear public metadata. It is
an ensemble statement under a physical IID premise, NOT randomness left
after conditioning on every known frequency label. Unique ancestry IDs
prevent known reuse but do not certify physical independence. Seeded controls
and finite censuses do not certify the external source premise either.

The component-frequency family loses phase order q exactly when all Q_l are
identically0 modulo3. Conditional on the quadratic matrices being all0 this
has probability3^(-n*d); if any is nonzero the loss event is impossible.
Thus, under the source premise, the unconditional order-loss probability is
AT MOST3^(-n*d), not necessarily equal. Any bounded unit-frequency word is
an exact certificate that the component family has order q at that instance.
This is NOT injectivity in all n secret coordinates or a full-secret solver.
It is also not a phase-order guarantee for every actual secret: the zero
secret always gives a flat phase, and secrets divisible by3 can have smaller
order even when the COMPONENT frequency family has full order q.

Crucially, a CLASSICAL quadratic Q mod3 is NOT supplied as the quantum phase
omega_3^(<s,Q mod3>) when r>1. The actual program uses omega_(3^r). Raising
its unknown phases to3^(r-1) is not a free operation, and identical program
copies/preparation inverses are unavailable. The source law prevents silent
information loss; it does not make the field-root receiver applicable.

## Supply, Complexity And Expected Ceiling

Worst-case original input cap:

    [n*((3^d-1)/2-d)+1]*(n+d)*(n+1)^2.

It is independent of r except integer bit arithmetic, polynomial at constant
d or d=O(log n), and exponential at d=poly(n). Present-cohort occupied-key
linear algebra is polynomial in the charged dictionary/cohort size, not in
an unbounded future dictionary. There is no claim of practical small costs.
At d1 the signature space is zero-dimensional: one standardized qutrit
already has degree<=2r. The producer explicitly calls that control TRIVIAL.

This removes one degree bottleneck WITHOUT recursive fresh cohorts at every
root, but has not removed the decoding bottleneck. A d-coordinate program
has at most d trits of accessible information per copy, not n*r answers.
No complete sample/error/time comparison beats known sieves. Upstream
approximate DCP/LWE supply and aggregate channel error remain separate.
The optional even-top SDE stage in `NATIVE_RIDGE_CANCELLATION_TARGET.md` is
not implemented; do not build it merely to reach degree2r-1. That is the
minimum full-order degree, not an ordinary character at root3^r.

## Try To Kill The First Readout Proposal

For a program-only receiver seeking s0=s mod3, assume the higher secret digits
b in Z_(q/3)^n are uniform and UNKNOWN, shared across all outputs. Averaging
over b gives the exact density matrix

    rho_s0(z,z')=omega_q^(<s0,Q(z)-Q(z')>)/D
                 *1[Q(z)=Q(z') mod H], H=q/3, D=3^d.

Different coarse fibers are orthogonal. Within a fiber f choose a base and
fine labels lambda=(Q(z)-Q(base))/H mod3; let N_f(lambda) be their counts.
Uniform-prior abelian discrimination gives exact optimal program-only success

    P_opt = sum_f (sum_lambda sqrt(N_f(lambda)))^2 /(3^n*D).

This is a bounded ideal reference, NOT an efficient coherent fiber compiler.
The formula is both a PGM value and a dual optimum: for each normalized pure
fiber state with amplitudes u_lambda=sqrt(N_lambda/|f|), diagonal dual entries
y_lambda=(sum u)*u_lambda/3^n have trace(sum u)^2/3^n, and rank-one constraint
sum_lambda(u_lambda^2/3^n)/y_lambda=1. Weight by |f|/D. The known connection
between optimal coset measurements and efficient implementation is discussed
by [Bacon, Childs and van Dam](https://arxiv.org/abs/quant-ph/0501044); the
specific conditional-digit formula here is the local derivation above.

Let K count ordered distinct pairs in the same coarse fiber. Since integer
counts obey sqrt(N_lambda*N_mu)<=N_lambda*N_mu,

    P_opt-3^-n <= K/(3^n*D).

For two DISTINCT data words, one selected program's full-rank physical frame
has at least one physical digit change that is nonzero modulo3. Its coefficient
of a conditional independent alpha_i in Z_q is an integer unit(+/-1,+/-2).
Condition on low policy, delta and all other alpha values. Therefore EACH
component frequency difference is independent uniform modulo q; vector coarse
collision probability is H^-n. This is true after signed injections because
m is uniform and the relation is LOW-only. Consequently

    E[P_opt-3^-n] <= min(1-3^-n,(D-1)/q^n).

For B output programs from independent original cohorts sharing the SAME
secret, use the sum of their frequency maps and dimension D_B=3^(d*B).
Any distinct joint word differs in one block, so the same unit-pivot argument
applies. The mean bound becomes min(1-3^-n,(D_B-1)/q^n), covering arbitrary
collective measurements on those B outputs. Do NOT tensor the individual
high-secret averages: that would incorrectly refresh the same unknown higher
secret on every copy. This bound does not cover other retained original
registers, extra outputs, a nonuniform high-secret prior after other evidence,
or an externally selected high-dependent source ensemble. It is a population
bound, NOT an upper bound for every fixed public-label instance.

For d=O(log n), a single isolated output thus has exponentially small average
advantage in the growing-dimensional regime, despite full component phase
order. A polynomial collection can cross this information threshold around
d*B comparable to n*r; the bound then becomes vacuous. That is NOT a
computational lower bound or a full-factory no-go. It redirects the next
research task to a source-aware COLLECTIVE coarse-fiber receiver, rather than
pretending the uniform modulo3 coefficient law supplies a cheap readout.

## Controls And Falsifiers

The producer uses prespecified actual native cohorts at retained roots3/9/27,
including d1 trivial, d2 and n2/d3 controls. It records every acquired source,
unused program, branch mass, low matrix/relation, compact phase, local degree
certificate, bounded frequency-family order and unit witness when present.
Selected programs undergo actual SUM replay for every injection outcome on
maximally reference-entangled data. A full original high-pivot census at root9
verifies that relation/quadratic part stay fixed while every linear change
mod3 is attained uniformly. These are virtual controls, not extra samples.

Reject relation mistakes, reused ancestors, malformed cohorts, failed
divisibility, high-dependent selectors, omitted nonzero outcomes, or a
dictionary bound that ignores new source directions. A unit-family-order
claim must include a verified original-root witness. Quadratic transfer at
higher roots remains independently falsifiable with the compact identity
workbench; one top-degree drop does not close its decoder debt.

```
python theorems/ternary_ridge_cancellation.py --write
node research/certificates/ternary_ridge_cancellation_crosscheck.js
python -m pytest -q tests/test_ternary_ridge_cancellation.py
```
