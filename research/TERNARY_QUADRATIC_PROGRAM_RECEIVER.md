# One-Use Quadratic Phase Programs Give Exact Secret Equations

LOCAL DERIVATION / REVIEW PENDING. A constructive conditional receiver,
not an unconditional native algorithm or a full-depth speedup. Gate
teleportation is established prior art; see
[Gottesman--Chuang](https://arxiv.org/abs/quant-ph/9908010) and
[Zhou--Leung--Chuang](https://arxiv.org/abs/quant-ph/0002039).

## The Missing Copy Assumption Can Be Removed

Suppose ONE supplied phase program is

    |psi_s> = 3^(-d/2) sum_z omega^(sum_l s_l g_l(z)) |z>,
    g_l(z) = z^T M_l z + beta_l*z, M_l symmetric over F3.

All M_l,beta_l are public; s in F3^n is unknown. Programs may have DIFFERENT
public functions on each use. No identical copies, controlled unknown phase
oracle, source inverse or free coherent evaluation of g_s is supplied.

Basis copying into d known zero qutrits produces

    |J_s> = 3^(-d/2) sum_z omega^(g_s(z)) |z>|z>.

This is the Choi program for diagonal U_s, not cloning |psi_s>: the two
marginals are maximally mixed. Bell measurement of an arbitrary input and
the first Choi half has unnormalized output

    K_(a,b)|phi> = 3^-d U_s X^a Z^(-b)|phi>.

Every a,b in F3^d has probability3^(-2d), even for data entangled with an
external reference. Both halves of the program are consumed by this one-use
procedure. This does NOT give a reusable oracle or the desired U_s with
known correctable byproducts on arbitrary data: U_s X^a U_s^dagger is unknown.

## Choose An Input That Does Not Need Unknown Correction

Find a public nonzero v satisfying v^T M_l v=0 for EVERY component l.
Prepare |line_v>=(sum_(j=0..2)|j*v>)/sqrt(3). For every Bell shift a,

    g_l(a+j*v) = g_l(a) + j*lambda_l(a),
    lambda_l(a) = beta_l*v + 2*a^T M_l v.

The teleportation output lies on the KNOWN shifted line a+j*v. Subtract a,
apply a public invertible F3 chart to turn j*v into j on one pivot wire, and
remove the known Z^(-b) phase with Z^(b*v). All other output wires are zero.
The pivot is omega^(j*<s,lambda>)/sqrt(3); its inverse Fourier measurement
gives the EXACT equation

    answer = <s,lambda(a)> mod3.

All Bell outcomes are useful for this equation. Nothing is postselected.
The direction is chosen after the public program is known but BEFORE the
random Bell shift. Quadraticity makes it isotropic for ALL shifts; choosing
a direction only after seeing a would not implement this protocol.

Let B_v have rows2*M_l*v. Then lambda=B_v*a+beta*v is uniform on a known
affine image. It is uniform on all F3^n IFF rank(B_v)=n, a PUBLIC certificate.
An exact equation still holds at smaller rank; claiming full uniform labels
then is false. In particular rank(B_v)<=d-1 for an isotropic v, so d>=n+1
is necessary for this full-rank version.

For independent supplied programs each passing this rank certificate, m=n+k
fresh Bell experiments give a full-rank equation system except probability
at most(3^n-1)/(2*3^m), by a union over projective secret differences.
This is a CONDITIONAL sample ledger, not proof those programs are available.

There is a second sufficient SOURCE law: if every beta_l is independently
uniform in F3^d conditional on the matrices and other transcript, and v is
chosen from the MATRICES ONLY, beta_l*v is uniform for every nonzero v.
Fresh program equation labels are then uniform even when B_v has deficient
rank. This does not contradict the fixed-program rank criterion. The live
source-law census checks all81 offsets for n2,d2,zero matrices and obtains
each of the nine labels nine times. A beta-dependent isotropic policy can
instead force beta*v=0; that is a falsifier of a careless uniformity claim.

## A Guaranteed Wide Common-Isotropy Construction

Set k=(n+1)^2. At d>=n*(k-1)+k=(n+1)^3-n, construct k independent vectors
e_i pairwise orthogonal under ALL n quadratic forms. At step j there are
at most n*j linear constraints M_l*e_i; their joint kernel has dimension
at least d-n*j>j, so a vector outside the earlier span exists and is found
by exact linear algebra. All cross terms vanish on their span.

Apply the repo's known F3 diagonal zero-sum support finder to the vectors
(e_i^T M_l e_i)_l. Its nonempty support gives v=sum_i e_i with every
quadratic value0. Independence gives v!=0. This is polynomial public field
arithmetic, not secret access. Full gradient rank is NOT guaranteed.
At smaller d, the implementation allows exhaustive CALIBRATION only at
d<=6; it does not relabel that search as a scalable algorithm.

## Actual Original-Native Bridge

The module also constructs quadratic programs from level3 carry packets,
which themselves are acquired from provided even level4 ORIGINAL samples.
A public frame W in the packet kernel must pass the actual mixed cubic
restriction gate in every component. Complete W to an invertible logical
basis; a supplied SWAP/SCALE/SUM gate recipe changes coordinates, then
measure the complementary coordinates. Every outcome is accepted.

The retained public phase is

    g_l(u) = [F_original(lift(base+W*u))-F_original(lift(base))]/3 mod3.

Top admission proves this is quadratic for every complement outcome.
Its matrices and linear terms are recovered by2d+binomial(d,2) public
frequency evaluations, not a3^d unknown-phase table. Branch global phases
are dropped only after the original and logical pointer measurements.

The live calibrations use27 physical odd rows indexed by x in F3^3.
Their low residue rows are x1 for n1, or x1,x2 for n2; the three physical
frame directions are x1,x2,x3. Their kernel and cubic constraints vanish
by complete field sums: every tested monomial has degree<=4, whereas a
nonzero F3^3 sum needs all three variable exponents positive even, at least6.
High native labels vary independently in this ENGINEERED low pattern.

Each odd input is realized by the known curvature-zero first parent in its
own(n+1)^2 original window. All original inputs are charged:108 for n1,
243 for n2, with27 active and81/216 untouched. The complete Gaussian packet
has26/25 free wires, then retains3 under the admitted frame. Fixed observed
zero syndromes/complements have raw program probability3^-24; this is a
CALIBRATION branch, not a free zero-branch factory. All branches of the
restriction instrument are allowed, but useful isotropy/rank need not hold
on every branch. Its coverage and IID-source construction are NOT proved.

The n1/n2 pinned programs have full gradient ranks1/2. ALL729 Bell outcomes
per program are replayed, and every readout gives the correct equation.
An additional complete Bell tensor replay checks arbitrary data entangled
with a two-dimensional reference. All27 native program frequencies are
derived from actual original labels. The original/parent packet word cubes
are not enumerated. The independent checker verifies the native charts,
ancestry, kernel restriction, public quadratic functions, Bell probabilities,
all equation labels and uniformity, and conditional rank-failure bounds.

These engineered low matrices are NOT an IID native population experiment.
No acceptance rate for a random-source factory or cryptographic reduction
is inferred. The construction recovers only s mod3; earlier measured high
secret digits and the untouched sources have their own accounting.
One observed source-plus-program-plus-Bell branch has probability3^-30;
the Bell probabilities above are conditional on the supplied program.

## Why It Matters, And Why It May Not

This supplies a concrete receiver for suitable quadratic programs without
identical-copy stabilizer tomography. The unknown random Pauli correction
is avoided by a translation-stable input line, not by an assumed unknown
Clifford inverse. Fresh programs with different public functions are legal.

It does not solve the main source transition. Existing matched-cubic or
Schur restrictions do not automatically produce enough informative programs
under IID growing-depth inputs. Disjoint native restrictions may reduce to
the KNOWN sieve, not improve it. No transfer of this field-root calculation
to higher roots is asserted: random shifts of cubic/deeper phases introduce
new line curvature. A reusable unknown-gate oracle is also not supplied.

The prior packet Pauli gate is not contradicted: this is a different
multi-register instrument following a measured quadratic restriction and
high-label-informed isotropic choice; its live sources are engineered.
Do not cite it as an escape from a gate whose source/menu premises are unmet.

NEXT CONSTRUCTIVE TARGET: charged factory-independent cubic cancellation
or an IID source-adapted quadratic restriction producing full-rank-gradient
programs at useful throughput. Signed top-tensor cancellation could combine
different programs using one-use injections, but must charge all sources
and measurement-dependent lower terms; a matching factory or full-depth
polynomial relation is not granted. Alternatively extend translation-stable
queries to higher-depth native functions with a genuinely costed construction.

Falsifiers: nonzero line curvature; wrong Bell byproduct orientation;
nonuniform raw branch mass; missing source ancestors; measured zero outcomes
counted free; gradient-rank deficiency called uniform labels; repeated use
of one consumed program; or unsupported extension to growing-depth phases.

```
python theorems/ternary_quadratic_program_receiver.py --write
node research/certificates/ternary_quadratic_program_receiver_crosscheck.js
python -m pytest -q tests/test_ternary_quadratic_program_receiver.py
```

Gemini/Antigravity owns routine CLI/registry wiring, full production checks
and Git. No accepted breakthrough candidate or novelty claim.
