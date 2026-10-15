# Next Source Direction: Coherent Sine Windows, Not Easy Polynomial-Gap Cubes

Status: IMPLEMENTED FINITE PUBLIC INSTRUMENT; GROWING REDUCTION AND NOVELTY UNCLAIMED.
See LATTICE_SINE_WINDOW_SOURCE.md, dedicated tests and independent exact replay.
This specification preserves the derivation, not a hardware or hardness claim.
The fixed-call public-phase baseline is complete. This next direction targets
an actual UNKNOWN-phase lattice source, not another known-phase mixer.
Literature comparison is required before claiming a new reduction.

## Why This Is Higher Leverage

The present planted q-ary controls use gap G=n^3 and are all LLL-recovered.
Making their bases look random does not fix this. A smoother PUBLIC localization
instrument can reduce the gap needed for the noisy coset-state promise without
assuming a free discrete-Gaussian state on a hard lattice. The receiver and
computational-hardness gaps remain; this proposal supplies neither.

## Known Coherent Packet With No Exponential Postselection

For K=2^w prepare the integer noise packet

    psi_K(x)=sqrt(2/K) sin(pi*x/K), x=0,...,K-1,

zero outside. A PUBLIC unitary W prepares a uniform x register and |+> flag,
applies exp(2*pi*i*x*flag/K), then H on the flag. Its flag1 probability is
EXACTLY1/2. Do not postselect all n packets at probability2^-n.

Instead apply S_good(i), then S_psi(i)=W S_zero(i) W^dag. In the good/bad
plane psi=(g+b)/sqrt2, this maps psi to(i-1)g/sqrt2, with NO bad component.
The full preparation is W S_zero(i) W^dag S_good(i) W, in matrix order.
Apply the known linear phase exp(-pi*i*x/K), global phase exp(-pi*i/4),
and X on the now-fixed flag to get REAL positive psi_K with flag/work ZERO.
Three W/W^dag uses, a known zero reflection and their inverses must be charged.

Use a clean Toffoli AND ladder for the zero reflection: w-1 work qubits,
one controlled pi/2 phase and uncompute. Do not accept an exponential
ancilla-free multi-controlled-phase decomposition as a polynomial gate cost.
Packet width is w data bits; total logical footprint2w including flag/AND work.
All rotations, binary64 encodings, query amplification and workspace cleanup
need the same precision discipline as the existing source/QFT compiler.

## Compact Support And Quadratic Visibility Loss

Let A_K(t)=sum_x psi_K(x) psi_K(x-t). It is nonnegative, A_K(0)=1,
A_K(1)=cos(pi/K), and A_K(t)=0 for |t|>=K-1. Translation telescoping on
ell2(Z) gives

    1-A_K(t) <= t^2 (1-cos(pi/K)) <= pi^2*t^2/(2K^2).

For n independent packet coordinates, affinity is

    kappa_K(v)=product_i A_K(v_i),
    1-kappa_K(u) <= pi^2 ||u||^2/(2K^2).

Any nonzero affinity requires ||v||<sqrt(n)*K. Thus compact support removes
far aliases EXACTLY, rather than asserting an unproved Gaussian tail sum.

## Public Lattice Source Instrument

Let B be a full-rank integer ROW basis, unknown primitive shortest vector
u=dB of length ell, and every nonparallel lattice vector have norm>=lambda2.
Choose PUBLIC split coordinate j, odd prime p, residue g in[1,p-1], parent
side M=2^m, and D_p=diag(1,...,p,...,1). Prepare colour b and a uniform
a in[0,M)^n. Compute the PUBLIC point

    x_b(a)=(a D_p + b g e_j) B.

Prepare n packet registers, ADD x_b(a) into those SAME noise registers, then
uncompute physical-point/constants/carry workspace. There must be no copied
original-noise or point garbage. Choose signed output widths from complete
public point+noise bounds so modular register representation cannot introduce
spurious physical collisions. Trace/discard the resulting y registers.

The remaining colour/position density has the EXACT Gram kernel

    rho[(b,a),(b',a')]=kappa_K(x_b(a)-x_b'(a'))/(2M^n).

No lattice Gaussian, CVP/preimage oracle, hidden u, or private source seed is
used in preparation. Initial noise packets are known product states, not a
conditional lattice distribution that would already find the short vector.

## Alias Conditions And Actual DCP Law

For a CORRECT trial d_j=g modp with g nonzero, require

    lambda2^2 > n K^2,
    (p-1)^2 ell^2 > n K^2.

Nonparallel differences then have zero affinity. Same-colour parallel
differences are multiples p u. Cross-colour differences have multiplier
1 modp; the ONLY possible nonzero-affinity one is u. The(p-1) condition
is essential: checking p alone misses the cross-colour alias(1-p)u.

The paired parent displacement is

    h_i=d_i (i!=j), h_j=(d_j-g)/p.

Embed original a wires into a SINGLE base-2M cyclic register of dimension
N=(2M)^n, with zero gap bits; do not substitute a tensor-product Fourier
transform. J(h)=sum_i h_i(2M)^i. Measure its positive cyclic QFT label k.
Labels are uniform, colour populations are1/2, and the conditional off-diagonal
is v exp(-2*pi*i*k*J(h)/N)/2, where

    v=kappa_K(u) product_i max(0,1-|h_i|/M).

This is exactly equivalent, when y is NOT supplied to the receiver, to good
DCP qubits with weight v and balanced bad basis qubits with weight1-v.
There is no clean flag. Independent fresh preparations give a conditional
product law; disjoint IDs alone are not its proof.

## Public Promise And Outer-Guess Accounting

Supply a PUBLIC norm interval ell_lower^2<=ell^2<=ell_upper^2 or pay length
guesses. A promised unique gap G permits the check G^2 ell_lower^2>=nK^2.
Choose p using ell_lower, not a privately known exact plant norm. Bound d
from PUBLIC B^(-1): |d_i|<=ceil sqrt(ell_upper^2 sum_r B^(-1)[r,i]^2),
using exact rational square comparisons. Tighten only with declared FAMILY
priors, e.g. ternary plants/free RREF coordinates; do not inject private d.
Use these bounds to choose M and pay all coordinate/residue/length trials.
Wrong trials need not satisfy the receiver promise; run a bounded circuit,
verify resulting vectors publicly, and never grant a correct-trial flag.

With public ||h||1 bound C and target bad rate epsilon, a sufficient budget is

    (242/49) ell_upper^2/K^2 + C/M <= epsilon,

using pi<22/7. This suggests G of order sqrt(n/epsilon), up to norm-interval
and dyadic constants, rather than n^3. If epsilon=1/f1(logN), its dependence
and the circular M/logN choice must be solved and charged. Constant-noise
sources give lower gaps ONLY IF an efficient constant-noise receiver exists.
Information-theoretic PGM robustness is not that receiver.

Mask J(h) uniformly with a common public random shift if the decoder requires
a uniform secret prior, using charged known phase rotations on measured labels;
do NOT infer such a prior from the lattice source. Signed radix decoding must
reject boundary digits and publicly verify the recovered lattice vector.

## First Implementations And Falsifiers

1. Deterministic packet compiler/inverse, exact affinity, resource and angle
   ledger. Test inverse roundtrips on arbitrary coherent data/flag inputs with
   clean AND work. The flag is zero for the KNOWN-ZERO preparation input;
   clearing it for every arbitrary input would contradict unitarity.
2. Public smeared-point source/reference Gram, no copied garbage; small complete
   label instrument agrees with the paired-shift law only under alias conditions.
3. Integrate actual cyclic readout and opaque UNKNOWN-qubit backend. A full
   parent inverse acts on y/label/colour together, NOT a free reflection about
   a sampled mixed qubit. Selected labels/y still pay their Born probabilities.
4. Generate lower-gap planted kernel sweeps with public LLL/BKZ and low-alphabet
   attacks BEFORE any hardness or quantum-signal claim. No filtering on recovery.

Critical countercontrol: n2, B=((17,0),(16,1)), u=(1,-1), d=(1,-1), split j0,
p7,g1,M2,K4. h=(0,-1); visibility=1/4. This is classically easy and should
validate only the instrument, never an advantage. Wrong residue, alias
threshold, cyclic/tensor QFT substitution, retained noise/point garbage,
free postselection or incorrect inverse must fail appropriate tests.

Initial NUMERICAL derivation checks passed: the matched pi/2 amplifier gives
the intended real packet and zero flag for w1..5, and the public reference
Gram matches all16 cyclic labels in the n2 countercontrol at visibility1/4
(tolerance1e-12). These are finite algebra checks, not an implemented source
circuit, full reduction, hardness certificate or quantum algorithm.

Do not misapply the fixed-call MPO baseline here. The source's reduced
density has short-shift structure, but its compact tensor entries depend
on UNKNOWN h. Public computation of individual Gram entries does not give
a polynomial tensor reconstruction: finding the sparse off-diagonal support
may itself find the short vector. Local position marginals can lose the
cross-colour coherence when another shifted coordinate is traced. A proposed
classical small-bond reconstruction from B must actually run and be priced;
neither unknown tensor cores nor a free source preimage/representative can
be inserted as inputs. This is an essential dequantization falsifier.

Most likely failures: lower-gap families remain classically easy; the
receiver remains exponentially costly despite good information; conditional
side information invalidates the chosen DCP model; geometry/norm guesses
are secretly calibrated; or preparation/precision prices destroy the claimed
reduction. Prioritize these falsifiers. No speedup, hard source, new reduction
or novelty is currently established.
