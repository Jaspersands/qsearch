# One-Use Packet Line Instruments

LOCAL DERIVATION / REVIEW PENDING. This tests a concrete shortcut around the
unmatched cubic factory. It is not a general quantum receiver lower bound.
Teleportation and state injection are established primitives
([Gottesman--Chuang](https://arxiv.org/abs/quant-ph/9908010),
[Zhou--Leung--Chuang](https://arxiv.org/abs/quant-ph/0002039)). The existing
quadratic-program receiver consumes one supplied program and accepts every
Bell outcome when its public line is isotropic. We ask whether a native
CUBIC packet can meet the corresponding condition directly.

REVISED AFTER SELF-REFUTATION: rare componentwise affine admission is NOT a
bound on all useful output information. Non-affine lines can carry noisy
information. The stronger result below compiles the COMPLETE known-line
teleportation instrument into ordinary quantum packet projection. No classical
simulation or general quantum complexity claim follows from this equivalence.

## Actual Packet And Exact Line Identity

Use the charged original level4 acquisition in
`TERNARY_CORRELATED_PACKET_ACQUISITION.md`. After the measured pointer and
syndrome, odd level3 frequency pairs satisfy a_i,c_i in Z_9^n and
c_i=2a_i mod3. For K physical odd sites let

    C_i = a_i mod3, kappa_i = (a_i+c_i)/3 mod3,
    t(z)=t0+D*z mod3, C*D=0, sigma=C*t0.
    Q(z)=[F(t(z))-F(t0) mod9]/3 in F3^n.

The retained supplied state is flat with phase omega^(s.Q(z)). It is not
a tensor product of fresh native samples and does not grant U_s or U_s^-1.
RREF metadata may use a unit-scaled low chart: sigma is recomputed from the
ACTUAL first frequencies and physical t0, not confused with that chart.

Choose nonzero logical v before the current Bell shift, allowing ALL public
high labels and the already observed source syndrome. Put d=D*v and
S=supp(d). At each changed physical site, the three translated trits visit
0,1,2 exactly once; their frequencies sum to a_i+c_i. Unchanged sites
contribute three copies. Subtract the original base phase before dividing3.
Using C*t(z)=sigma gives the exact componentwise identity

    sum_(j=0)^2 Q(z+j*v)
      = sum_(i in S) kappa_i - C_S*t0 - C_S*D*z mod3,

where C_S=C*diag(1_S). No polynomial interpolation, unknown phase query or
field replacement of Z_9 is used. For a function on one F3 line, sum of
its three values vanishes iff its quadratic coefficient vanishes. Therefore
the direct one-use line protocol is affine for EVERY translated line and
EVERY secret precisely when

    C_S*D=0, sum_(i in S) kappa_i = C_S*t0.

This criterion is public polynomial arithmetic. Exhaustive direction tables
in bounded controls validate the identity; they are not a scalable search.
An admitted line need not produce a nonzero or uniformly distributed equation.

## Coupled Codes Give An Exact Admission Bottleneck

Form the n*h by K matrix A with entries A_(l,j),i=C_l,i*D_i,j. Its kernel
contains the all-ones mask. If rank(A)=K-1, ONLY constant diagonal masks
preserve the packet kernel. A nonzero v therefore can be admitted only if
S is every physical site and

    sigma = sum_i kappa_i.

This necessary condition allows arbitrarily expensive HIGH-informed direction
search. It is not the older low-defined Pauli-menu gate. A full-support
kernel vector is not automatically available or efficiently found; omitting
that additional requirement makes the admission bound conservative.
Conditional on fixed full labels, source syndromes are uniform on im(C).
At full rank n the prescribed sigma occurs with probability3^-n, irrespective
of how a direction is selected after seeing the source syndrome. Postselection
cannot turn the raw branch probability into free program supply.

## IID Low-Matrix Population Accounting

The charged acquisition's source theorem gives IID C columns under its
original IID native premise. Distinct source IDs do not establish this premise.
For C uniform in F3^(n by K), charge rank failure by
(3^n-1)/(2*3^K), and the existence of a zero column by K/3^n.

For full row rank with no zero columns, a nonconstant invariant diagonal mask
induces an endomorphism of row space. Its F3 spectral projectors yield a
nontrivial idempotent P of rank r, 1<=r<n, whose image and kernel contain
every C column. Conversely any such invariant support is a direct-sum
separator. The proof only needs this implication, not a hardness assumption.
There are EXACTLY

    N_r = GaussianBinomial_3(n,r)*3^(r*(n-r))

rank-r idempotents, and |im(P) union ker(P)|=3^r+3^(n-r)-1. A union bound is

    delta = min(1, rank_failure + K/3^n
      + sum_(r=1)^(n-1) N_r*((3^r+3^(n-r)-1)/3^n)^K).

Hence the raw probability that some nonzero line meets the exact admission
criterion is at most min(1,delta+3^-n). For K=4n this bound decreases
exponentially with n; small-n clipping is retained. The producer supplies
exact rational projection counts and bounds, not fitted exponents. Original
level4 supply is K*(n+1)^2 per packet, BEFORE any rare syndrome filtering.
This is not a success lower bound or the cost of acquiring original states
from a classical hard problem.

For completeness, GaussianBinomial_3(n,r)<=2*3^(r*(n-r)), since the
denominator product is greater than1/2. For r< n/2, the union fraction is at
most(4/3)*3^-r. At K=4n each such projection contribution is at most
2*(4/3)^(4n)*3^(-2*r*n-2*r^2). The symmetric ranks have the same bound;
the even midpoint is at most2*2^(4n)*3^(-3*n^2/2). Summing these and charging
zero columns/rank proves the exponential decrease, not just a numerical trend.

## Complete Instrument Compilation: The Actual Research Decision

For ANY supplied packet density matrix, even entangled with an external
reference, use the known uniform input line sum_j |j*v>/sqrt3. Basis-copy
the packet to a blank wire and perform the Bell instrument. After public
byproduct cleanup and line-coordinate extraction, the Kraus operator for
classical shift a and phase b is exactly

    K_(a,b) = 1/sqrt(3*N) sum_(j=0)^2 |j><a+j*v|, N=3^h.

It is independent of b after cleanup. This does NOT implement a reusable
unknown unitary, nor does it require that any phase be affine. Complete the
fixed public v to a field basis (v,B), and uniquely write a=t*v+B*w.
The SAME instrument has the following direct implementation on the original
packet, without a Choi ancilla, Bell data or source copies:

1. Apply the public inverse linear chart z -> (j,w).
2. Measure ONLY the h-1 quotient coordinates w, retaining the j qutrit.
3. Sample public t uniform in F3 and b uniform in F3^h.
4. Shift the retained coordinate by -t; report a=t*v+B*w and b.

The quantum projection's selection rows become <a+j*v|. Public randomness
contributes squared factor1/(3*N), so the complete measured instrument is
IDENTICAL, including raw probabilities, every a,b, curved states and an
external reference. At flat amplitudes the individual Bell outcomes are
uniform1/N^2; that is not assumed for arbitrary density matrices. No unknown
global phase is erased before a real measurement, and no failed branch is
discarded. Clean known field arithmetic/gates and randomness are charged.

This equivalence covers a direction chosen using ALL current public labels
and previous source outcomes, but fixed before the current Bell outcome.
It does not cover arbitrary unknown data, coherent superpositions of several
lines or a different programmable measurement. It is a QUANTUM instrument
compiler, NOT classical dequantization of the source or an efficient decoder.

### Why The Rare Gate Alone Would Mislead

Write a line's three component phases as Q(a)+j*L+j^2*H. Here
L=Q(a+2v)-Q(a+v), H=2*sum_j Q(a+jv). If s.H=0, inverse F3 gives the exact
linear equation answer=s.L. If s.H!=0, the quadratic Gauss sum has equal
output probabilities1/3. Componentwise H=0 is sufficient for deterministic
equations for EVERY secret, but is not necessary for information or for
secret-dependent exact cancellation. Such gated records are precisely the
existing final-field incidence/MUB readout family, not a reason to discard
all non-affine lines. The native odd-to-even pointed-line source law already
exists in `TERNARY_INCIDENCE_DECODER.md`.

Decision: do not pursue this known-line teleportation as an extra collective
mechanism or declare cubic packets useless from affine rejection. It merely
reexpresses an existing packet restriction. A receiver must retain multiple
logical directions coherently, change its known data/input support or supply
a source-aware decoder beyond this baseline to escape the compiler.

## Exceptions And Ways To Escape

- Decomposable low codes can admit proper supports and several useful
  syndromes; an explicit two-block native countercontrol preserves this.
- Zero columns and deficient rank are charged, not silently excluded.
- Restricting logical coordinates changes D; this full-packet result does
  not cover the older restricted quadratic programs.
- A direction chosen after the current Bell shift is a different protocol.
- Approximate, non-affine or stochastic readouts can still carry information.
- Multiple unmatched programs can cancel cubic terms: the implemented
  factory is outside this one-use gate and must not be ruled out by it.
- Other collective receivers, retained pointer interference, higher roots
  and measurements of untouched original inputs remain open.

Falsifiers: the original-root line identity fails; direct tables disagree
with rank/constant admission; a fully coupled packet admits a proper support
or wrong syndrome; decomposable controls are falsely excluded; or raw source
branches or projection counts are omitted. External proof review is required.

The independent exact verifier rebuilds9,288 direction/shift checks, native
original-source ancestry, code ranks, every population projection count and
243 affine Bell readouts. Python also executes complete actual Bell tensors
for arbitrary reference-entangled packets at h=1,2,3 and compares compiled
Kraus amplitudes. The compiler's support/scaling identities are checked
separately with exact field arithmetic; finite tensor replay is not a growing
hardware-error certificate.

```
python theorems/ternary_packet_line_receiver.py --write
node research/certificates/ternary_packet_line_receiver_crosscheck.js
python -m pytest -q tests/test_ternary_packet_line_receiver.py
```

Gemini owns CLI/registry/UI integration and full production validation. Register
this as a scoped exact admission test, not an accepted speedup candidate.
