# Single-source lattice Green sampler: independent finite-clock proof

Date: 2026-11-13. Reviewed STATE, the native sparse-wave contract, and the
terminal `claude_runs/2026-11-13-wave-lattice-shell/response.md` in full.
No other live report, API, network, Git, implementation, or sweep was used.

**Disposition: the SINGLE-source theorem survives with the repairs below.**
For every n>=2 and 0<epsilon<1, the native spatial Born law for a single
nonzero source has a written quantum sampler with deterministic polynomial
BIT/gate/space cost in n, input bit length, and log(1/epsilon). It always
outputs a legal site. The proof pays finite arithmetic, chart and offset
erasure, full Fourier tails, inverse QFT, and a capped success clock.
It supplies neither a multiple-source theorem nor a classical spatial
sampler, advantage, implementation, or novelty claim.

The report's optional five-source corollary C2 is not used. Nor is its
unverified classical conditional-sampling sketch imported.

## 1. Notation, precision, and deterministic labels

Write L=2^n, eta=1/L, and

    D(k)=2cos(2pi k_x/L)+2cos(2pi k_y/L)-3,
    a(k)=D(k)+i eta,
    T_L=sum_k |a(k)|^(-2),   Z0=T_L/L^2.

Thus T_L is the unnormalized Fourier sum; Z0 is the contract's single-source
squared spatial norm. They differ by L^2. Initially assume n>=4 and
0<epsilon<=1/4; larger error requests can use epsilon=1/4.
Choose

    p=n+ceil(log_2(256/epsilon)),   delta=2^(-p).

Use one fixed deterministic dyadic cosine routine c(k), clipped into
[-1,1], with error at most delta/4. Set

    Dtilde(k)=2c(k_x)+2c(k_y)-3.

All operations defining Dtilde and subsequent comparisons are exact
operations on the computed dyadic words. In particular

    |Dtilde-D|<=delta<=epsilon/(256L)<eta/12.                (1)

Use centered integer representatives in (-L/2,L/2]. Chart A means
|k_y|>=|k_x|, including ties; chart B is its complement. In each chart the
major coordinate is the larger absolute coordinate, and its sign is + for
zero and - otherwise when negative. Let J=n-2 and t_j=2^j/L, 0<=j<=J.
The deterministic label b(k) is (chart,sign,j) when

    |Dtilde|<=eta                  for j=0,
    t_(j-1)<|Dtilde|<=t_j         for j>=1;

it is F when |Dtilde|>1/4. These rules partition every finite-grid point,
including threshold ties. The same word-level routine is used to erase the
label later. No exact-real sign or equality oracle is present.

## 2. Total window routine and the repaired width bound

For a near branch, call its free coordinate k_f and its major coordinate
k_m. Define, using the same clipped cosine routine,

    c0=3/2-c(k_f),  s_j=t_j+3delta,
    c_hi=min(c0+s_j/2,13/16+delta),
    c_lo=max(c0-s_j/2,3/8-delta).

Only c_hi is used by the implemented start routine. Since c0 is in [1/2,5/2],
for EVERY free-coordinate input, including empty clipped intervals,

    1/2<=c_hi<=13/16+delta<=157/192<0.82.                    (2)

Compute a dyadic xlo approximating L arccos(c_hi)/(2pi) to absolute
error <=1/4, and put S=floor(xlo)-1. The floor is the exact floor of this
computed dyadic word, not a demand to decide the floor of an unknown real.
Set the power-of-two window length

    W_j=2^ceil(log_2((7/20)2^j+4)).                          (3)

It is computed by integer/rational comparisons. W_0=8,
W_j<=8*2^j, and W_j<=L for n>=4, j<=n-2. In fact W_j<=L/2.
The window is S,...,S+W_j-1, with sign and reduction modulo L applied
when writing the major coordinate. Empty clipped intervals need no special
inverse-trigonometric call: the same total start routine remains valid.

Here is the containment proof. If k has this near label, the actual cosines
satisfy cos(theta_m)<=cos(theta_f) and |D(k)|<=1/4+delta. Hence

    3/8-delta/2 <=cos(theta_m)<=13/16+delta/4.

Also |cos(theta_m)-c0|<=t_j/2+3delta/4<=s_j/2. Thus its actual major angle
lies in [arccos(c_hi),arccos(c_lo)]; that interval is nonempty for every
point assigned this label. On its clipped cosine range,

    |sin(theta)|>=sqrt(1-(157/192)^2)>4/7.

The inverse-cosine Lipschitz constant is therefore <=7/4. Since
s_j<=5t_j/4, the angular width is <=35t_j/16. Using pi>25/8,
its width in grid-index units is strictly less than

    (35/(32pi))2^j < (7/20)2^j.                             (4)

This repairs the report's unsafe intermediate rounding to 2.2. The
computed start is at most the true lower endpoint and at least that
endpoint minus 9/4. Equations (3)-(4) give more than enough room for every
integer in the interval: S+W_j-1 exceeds its upper endpoint.
As W_j<=L, the offset representing such a point is unique modulo L.
The proof applies to either chart and either sign.

## 3. Proposal amplitudes and the exact analysis target

Use branch weights

    q_(chart,sign,j)=2^(-j),  q_F=1/L,
    Q=sum_b q_b=8-15/L<8,   p_b=q_b/Q.

Prepare the branch state sum_b sqrt(p_b)|b>. There are 4(n-1)+1 labels.
Conditional on b, prepare a uniform free coordinate and a uniform offset
in [0,W_b), with W_F=L. For a near branch write the signed major coordinate
S+offset modulo L; for F just write the second coordinate. Chart B swaps
the two coordinate roles. The proposal amplitude for this path is

    e_b=sqrt(q_b/(Q L W_b)).

Compute g=[b=b(k)]. On g=1 retain the path with controlled good amplitude

    r_b(k)=C_b/[M a(k)],
    C_b=sqrt(Q L W_b/q_b),  M^2=320L^3.                     (5)

Equation (5), with the TRUE a, is an analysis-only ideal rotation. It is
not an exact-real operation offered to the circuit. It is a valid rotation:
for j>=1, |D|>t_j/2-delta>=(11/24)t_j, and consequently

    |r_b(k)|^2 < (576/121)*8*8/320 =576/605<1.

For j=0 the squared magnitude is <1/5. For F, |D|>1/4-delta>=47/192,
and the squared magnitude is <1/2. Thus this ideal comparison has uniform
slack and is well defined even when a label lies near a threshold.

Each k has exactly one surviving proposal path, its own label and unique
offset. Since e_b C_b=1, erasing the path data gives the ideal good vector

    v=(1/M) sum_k a(k)^(-1)|k>|0_work>.                     (6)

No count of shell points or value of T_L was used. Summing the squared
amplitudes in (6) also proves T_L<=320L^3 from the already established
pointwise rotation bounds; this is not an input normalizer assumption.

## 4. Implemented amplitudes, total functions, and erasure

The implemented arithmetic replaces a by
atilde=Dtilde+i/L. Its squared rotation magnitude is the exact rational

    rho^2=Q W_b/[320 q_b ((L Dtilde)^2+1)].                  (7)

On g=1 this is <4/5 for j>=1, <1/5 for j=0, and <2/5 for F, directly
from the Dtilde label thresholds. Thus the IMPLEMENTED rotation has still
more slack than (5). On g=0 define its angle outputs to be zero. Invalid
padding labels have the same harmless default. A clip of (7) into [0,81/100]
makes the numeric subroutine total even on unreachable inconsistent words;
it changes no valid good-path value. Take rho=sqrt(rho^2) and

    phi=arctan(L Dtilde)-pi/2.

An R_y(2arcsin(rho)) followed by the phase diag(1,exp(i phi)) on its flag
has good amplitude C_b/(M atilde). All numeric work is then uncomputed.

The path erasure is essential. Conditional on g=1, recover the offset from
k and b as (sign*k_m-S_b(k_f)) mod L (or the second coordinate for F),
and XOR this n-bit word out of the offset register. Next compute the same
b(k) and XOR it out of b, then uncompute the temporary label. The coordinates
already occupy their final k_x,k_y registers; no duplicate free coordinate
is retained. Every start, comparison, magnitude, and phase work register is
uncomputed before acceptance. These are reversible XOR/addition operations;
uniqueness of the matching path is what makes the supported registers zero.
Rejected paths retain arbitrary work and are discarded on failure.

The rotation flag can be 1 only on a matching path. Flip g with that flag,
so g is also zero in the accepted branch. Measuring only the rotation flag
therefore leaves the clean, coherently summed vector

    vtilde=(1/M) sum_k atilde(k)^(-1)|k>|0_work>.            (8)

In particular no chart or source-path label is measured or traced out
before these amplitudes are combined.

The inverse error is especially simple:

    |1/atilde-1/a| <=L delta |1/a|,
    ||vtilde-v||<=L delta ||v||.

Consequently their normalized vectors differ by at most 2L delta
<=epsilon/128. This comparison allows labels and windows to depend on p:
for EACH chosen p, containment and uniqueness prove (6), and the one fixed
computed partition is erased exactly. There is no limiting-label promise.

## 5. Deterministic finite-bit arithmetic and finite gates

All requested scalar operations have deterministic polynomial BIT circuits.
Here are explicit constructions, not supplied elementary-function oracles.

* Compute pi by Machin's identity
  pi=16 arctan(1/5)-4 arctan(1/239). The alternating series for each arctan
  has geometrically decreasing terms and a remainder bounded by its next
  term. O(h) terms and O(h+log h) fixed-point guard bits give h certified
  bits. Exact rational accumulation is also polynomial-bit.
* For cosine, range-reduce the angle into a bounded interval, or simply use
  |angle|<=7. Its Taylor remainder is bounded by the next derivative bound
  7^(2N+2)/(2N+2)!. O(h) terms suffice, with rounding guards O(log h).
  Multiplying the certified pi interval by k/L introduces no exponential
  conditioning. This constructs the c(k) required in (1).
* Arccos on [1/2,157/192], and on [0,9/10] for the magnitude rotation, is
  computed by interval bisection with certified cosine evaluations. The
  root is in [0,2], and the relevant sine is bounded away from zero. If a
  midpoint's cosine interval contains the input, that interval already
  bounds the angle error by a fixed multiple of its width; return it or
  refine. Otherwise the sign comparison safely halves the bracket. O(h)
  stages give h angle bits without an undecidable equality test. Computing
  L arccos(c_hi)/(2pi) to error 1/4 needs n+O(1) such bits.
* Rational products, quotients, and (7) have O(n+p) bit length before output
  rounding. Their denominators are explicitly nonzero. Square roots are
  found by dyadic bisection, comparing squared trial values with the exact
  rational argument. This gives absolute output accuracy even near zero;
  no derivative bound for sqrt at zero is assumed.
* For the phase, use arctan h=sign(h)(pi/2-arctan(1/|h|)) when |h|>1.
  For |h|<=1 use arctan h=2 arctan(h/(1+sqrt(1+h^2))). The new argument has
  magnitude at most sqrt(2)-1<1/2, so its alternating series converges
  geometrically. The sign and zero of h=L Dtilde are exact dyadic tests.
  Thus the phase is uniformly computable even when Dtilde is tiny.

These fixed-length arithmetic algorithms are made reversible by storing
and then uncomputing their intermediate words. Every loop has a prescribed
polynomial iteration bound; bisection equality cases have the certified
termination rule just described. Boolean gates can be Toffoli/CNOT/X.

For branch preparation use a binary probability tree on the O(n) labels:
all prefix masses are exact rationals, and each internal rotation has
squared amplitude equal to a ratio of two prefix masses. Empty prefixes
are assigned the identity. Their square roots and angles can be computed
to any prescribed polynomial number of bits. At endpoints the inverse
trigonometric function is only Holder-continuous, which is harmless: use
O(h) extra bits (e.g. 2h+O(1)) in its squared amplitude to obtain h angle
bits, or bisect the angle directly with its squared sine/cosine criterion.
This avoids claiming a uniform derivative bound at probability 0 or 1.

Fix a finite universal gate palette, for example H, controlled-H, X,
CNOT, Toffoli, T and T^dagger. The sole standard circuit compilation fact
used is constructive Solovay--Kitaev for constant-dimensional rotations.
Its input matrices are computed by the routines above, and its finite
constant starting net is independent of the native input. No arbitrary
real-angle gate is supplied. A variable rotation is the product of O(h)
fixed dyadic-angle rotations controlled by its computed angle bits.
Controlled rotations/phases use the ordinary CNOT decompositions into
uncontrolled half-angle rotations; compile those complete pieces with
tracked global phase. Higher Boolean controls are reduced to a clean AND
ancilla. Compile the complete unconditional half-angle pieces, using actual
inverse sequences where appropriate; each residual global phase is then a
single input-independent phase. In particular a discarded global phase of
an uncontrolled gate is not silently promoted into an input-dependent
controlled phase. All norm comparisons may align this one overall phase.

For clarity, an explicit noncircular error allocation is available. Put

    Pstar=1/124800,  nu=Pstar*epsilon/100,
    h=p+10ceil(log_2(n+p+2))+100.

Use internal elementary-function tolerance 2^(-(2h+40)), then round output
angles to h fractional bits. The displayed series need at most 2h+100
terms; exact rational summation followed by one directed rounding avoids
accumulated-rounding ambiguity. Bisections have at most 2h+100 stages,
with padding after early certified completion. These constants also pay
the global square-root modulus of continuity at branch-angle endpoints.
Thus every output angle has error at most 2^(-h). The branch/variable-angle
numeric error is at most 64(n+h+1)2^(-h)<nu/4. To check the last inequality,
put S=n+p+2>=16; then n+h+1<=10S, 2^(-p)<=epsilon/(256L), and
Pstar>2^(-17). No success probability is estimated to select these bits.
Compile each of the at most 64(n+h+1) elementary rotation pieces to operator
error nu/[256(n+h+1)]. The reversible integer work and palette gates are exact.
The resulting full attempt differs by at most nu from the ideal circuit
with exact rotations for the computed Dtilde. The sizes and precision are
fixed before running an attempt, not chosen from an observed success rate.

## 6. A deterministic success clock and the full spatial law

A finite-grid lower bound requires no asymptotic shell count. For every
k_x=0,...,floor(L/6), choose the nearest grid k_y to the angle solving
cos(theta_y)=3/2-cos(2pi k_x/L). Then |D(k)|<=2pi/L. These are at least
L/6 distinct grid points, giving

    T_L>=L^3/[6(4pi^2+1)]>=L^3/390.

The ideal probability in (6) is therefore at least Pstar. From (1) and
(8), the exact-Dtilde probability is at least (1-L delta)^2 Pstar,
which exceeds 3Pstar/4. A norm error nu changes a flag probability by at
most 2nu, so the actually compiled attempt succeeds with probability
at least Pstar/2. Its conditional accepted state differs from the
exact-Dtilde normalized state by at most

    2nu/sqrt(Pstar/2) <epsilon/32.

Run at most

    s_epsilon=ceil(log_2(4/epsilon)),
    Ntry=249600 s_epsilon=(2/Pstar)s_epsilon                (9)

fresh attempts, stopping at the first accepted flag. The ceiling is obtained
by exact comparisons of the rational error input with powers of two. On
exhaustion output a fixed legal site. Exhaustion probability is at most
exp(-s_epsilon)<=2^(-s_epsilon)<=epsilon/4. Each accepted attempt has the
same conditional law; taking the first success does not change that law.
Thus the per-attempt conditional-error bound suffices without multiplying
it by the retry count. This supplies a deterministic worst-case clock,
not merely the report's expected repeat-until-success claim.

Apply the two inverse QFTs to an accepted state and measure its coordinates.
The ordinary binary-QFT circuit uses O(n^2) fixed controlled phase gates;
compute their pi-dependent angles as above and compile the whole inverse
QFT to operator error <=epsilon/32. The ideal inverse QFT of the normalized
vector in (6) is exactly G/||G||, because the single-source Fourier transform
has the factor 1/L and Z0=T_L/L^2. This retains every Fourier mode.
The conditional state errors, QFT error, and exhaustion probability sum to
less than epsilon in spatial total variation, including residual work by
measurement contraction.

For a source w delta_(x0), its nonzero scalar w cancels from the Born law.
After sampling the origin-source law, add x0 modulo L to the measured
coordinates, using exact n-bit arithmetic. This avoids even a variable
source phase; equivalently one may implement the translated quantum state.
All these costs are polynomial in n, source bit length, and log(1/epsilon).

## 7. The n=2,3 cases and scope

For L=4 or 8, use a uniform Fourier proposal and good amplitude
L/(M atilde), keeping the SAME M^2=320L^3. Its squared magnitude is at
most L/320<=1/40, so it has uniform slack. The accepted vector is again
(8). The finite-grid lower bound in Section 6 holds at these sizes as well,
so its exact-Dtilde success probability is at least
(1-L delta)^2 Pstar. The same finite arithmetic, relative inverse-error
argument, accepted-work erasure, inverse QFT, and cap (9) apply directly.
Thus all n in the native contract are covered with the same public scale
and clock; no finite numerical control or extrapolation is needed.

The proposal also gives a bounded-clock CLASSICAL sampler of the Fourier
probabilities by classical rejection. An inverse quantum Fourier transform
is not a classical transformation of one frequency sample. Accordingly no
classical spatial sampler follows from that observation. Multiple-source
normalization and interference remain separate, as illustrated by the
already proved five-source and positive-array counterexamples. This review
closes only the written single-source quantum compiler at the stated scope.
