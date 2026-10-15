# Public Lattice To Cube Coset Source

This implements the integer public source function and a complete bounded
Born-law reference from Regev's cube construction, not a scalable physical
state-preparation circuit or a new shortest-vector algorithm. The primary
source is `literature_cache/cs_0304005_source/quantum_average.tex`, the
cube lemma before the improved ball construction. The cube reduction has
unique-SVP factor Theta(n^(1+2f)); the improved ball factor is
Theta(n^(.5+2f)). This module does NOT claim to implement the ball source.

## What Is Actually Public

Basis vectors b_j are integer rows. Parameters p (prime), nonzero residue
guess m, coordinate i0, dyadic box M, dyadic width W, and offsets J_i in
1..W are public. No short vector, its basis coefficients, shift, preimage,
clean flag or planted truth is passed to the source constructor.

    f(t,a) = (p*a_i0+t*m)*b_i0 + sum_(j!=i0) a_j*b_j
    F_i(t,a) = floor((f_i(t,a)-J_i)/W)
    t in{0,1}, a in{0,...,M-1}^n.

For integer f_i, independent uniform J_i in1..W give EXACTLY the same
partition law as independent continuous offsets w_i in[0,1), except for
measure-zero endpoints: choose J_i=ceil(W*w_i). Negative values use floor
division, not truncation toward zero. Exact arbitrary Python integers
prevent signed overflow in the evaluator.

Logical quantum preparation starts with a uniform superposition over all
2*M^n inputs, computes F in a clean output register, then measures F.
Every measured cell r has probability |C_r|/(2*M^n), and the remaining
state is the normalized UNIFORM COHERENT superposition of its preimages.
Classical uniform input sampling reproduces cell probabilities ONLY; it
does not prepare these conditional coherent states.

The complete reference enumerates all inputs and all cells, including
singletons and invalid multipoint cells. It is exponential in dimension.
It is not a free preimage oracle and not the claimed efficient quantum
implementation. `UNKNOWN_REFERENCE_CAP` is no evidence against the source.

## Geometry And Failure Accounting

For a correct short-vector coefficient guess, set

    delta_i0=(u_i0-m)/p, delta_j=u_j otherwise.

Then f(1,a+delta)-f(0,a) is the physical short vector u. Sufficient
geometry conditions for at most one preimage of each colour and no other
partner are

    lambda_nonparallel^2 > n*W^2,
    (p-1)^2*lambda1^2 > n*W^2.

These exclude every nonparallel vector and every parallel multiple with
wrong colour congruence inside a cube. They are sufficient, not necessary
conditions. A generic input does not come with a certified uniqueness gap;
the reference can test finite fibres but cannot infer a growing-family
unique-SVP promise, LLL coordinate bound or a correct outer guess.

When the geometry holds, the EXACT good-register mass averaged over
independent fresh offsets and uniformly weighted original inputs is

    product_i max(0,1-|delta_i|/M)
      * product_i max(0,1-|u_i|/W).

The first factor pays box boundaries. The second pays cube overlap. The
offset average is not a guarantee for a particular fixed offset. The
helper computes the specified partner event even without geometry; only
under the shape/common-partner promise is it the full good-source mass.

The primary theorem uses M=2^(4n), LLL coefficient control, suitable width
constants and prime p>n^(2+2f), with polynomially many outer guesses for
fixed f. Passing arbitrary user parameters does not certify that theorem.
Hardware noise, bad-register independence and repeated-offset correlations
remain separate obligations.

## Scalar Phase States And Balanced Bad Registers

Embed positions by x(a)=sum_i a_i*(2M)^i, phase modulus N=(2M)^n.
Good two-point cells have a COMMON vector difference delta, hence common
scalar shift S=sum_i delta_i*(2M)^i modN. Positive position QFT followed
by measuring label k yields the qubit

    (|0>+exp(2*pi*i*k*S/N)|1>)/sqrt2.

Under at most one point per colour, every cell gives uniform k, including
singletons. Multipoint/same-colour cells do NOT inherit this argument and
cannot be relabeled ordinary bad basis registers. They invalidate the
two-point contract and may bias the label distribution.

Every good cell removes one input of each colour. Initial colour totals
are equal, so the singleton bad0 and bad1 populations are exactly equal
after discarding cell side information. For bad rate p_bad the marginal
phase qubit is

    (1-p_bad)*|phi_k><phi_k| + p_bad*I2/2,

equivalent to Z flips at p_bad/2 on the equatorial good state. This only
certifies the abstract marginal in this source model. A receiver using
public offsets/measured cells has additional information; reusing a
global random offset may correlate source errors. Neither is a general
independent-noise theorem for all Regev sources.

The unknown shortest vector is constrained by the PUBLIC basis and promise;
its embedded scalar shift is not assumed uniform over Z_N. Uniform-secret
twirling arguments from an abstract DCP model cannot be transferred here
without a proved distributional reduction. This does not supply an efficient
prior-dependent receiver, but it prevents an unjustified global exclusion.

Signed differences satisfy |delta_i|<M. Adding the base-(2M) offset with
all digits M before decoding yields digits delta_i+M in1..2M-1, so no
carry ambiguity occurs. The decoder rejects out-of-contract digits and
rechecks the modular encoding.

## Known Parent Inverse Is Not A Conditional Inverse

Let U prepare the full clean source. For a specified measured cell C_r,
U^dag sends its normalized conditional state back to all-zero with
probability |C_r|/(2*M^n), NOT1. Including a specified measured Fourier
label adds the1/N factor when the source geometry makes labels uniform.
The controls' good-cell prices are1/65536 and1/17179869184 respectively.
These prices do NOT apply to sampling any unspecified good cell, whose
probability is close to1 in this example. Different coherent algorithms
using public F, its inverse and lattice geometry remain open.

Clean scalable computation must copy the cell label and uncompute ALL
physical lattice-point, signed arithmetic, carry and remainder workspace.
Leaving f(t,a) in garbage distinguishes the two partner points and destroys
their coherence. Integer evaluation alone does not prove a clean reversible
adder/divider circuit. That physical implementation is explicitly absent.

The source exposes a clean-arithmetic compilation plan with exact signed
widths. Bound each coordinate of f-J by sum_j |b_ji|*c_j_max+W, where
c_i0_max=p*(M-1)+m and the other maxima are M-1. Choose a signed width
w_i with2^(w_i-1) STRICTLY above this bound and w_i>=log2W+1. The
upper w_i-log2W bits of the two's-complement point encode floor((f-J)/W),
including negative values. Copy those bits to the cell register and run
the complete arithmetic backward. The low remainder bits are NOT retained
garbage. Exhaustive finite tests verify the widths/high-bit floor rule;
they do not substitute for a coherent reversible gate implementation.

The base-2M position embedding also needs n zero padding qubits; the phase
register has n*(log2M+1) wires. Those are separate from the initial
1+n*log2M uniformly superposed source bits and the signed cell workspace.

## Controls And Matched Classical Attack

The public unreduced basis (10000,1000),(9999,1000) generates Z x1000Z.
The control p389,m1,i0=0,M256,W128 has common coefficient difference
(0,-1), physical displacement(1,0), and scalar shift-512 mod262144.
Its nonparallel squared norm is at least1,000,000, above cube squared
diameter32768; the next wrong-congruence parallel multiple is at least388
long, also excluded. Three fixed offsets census every131072 source input.
Fresh-offset average good mass is(255/256)*(127/128); bad mass is below
the f1 budget1/log2N=1/18. The finite promise is directly checked, not
silently inherited from the basis being LLL-reduced (it is not).

Public LLL reduction returns a norm-one integer vector WITHOUT truth.
Every nonzero integer vector has norm at least1, so this solves the control
globally. The source works, but the calibration is classically easy and
is NOT a new algorithm candidate. A p3,W64 countercontrol produces invalid
multipoint fibres and is correctly refused as an abstract two-point source.

Next high-impact work: compile clean scalable public source arithmetic;
retain public-geometry/offset/cell access in the receiver contract; develop
a robust collective decoder; test growing dimensions against paid lattice
baselines. Do not substitute a phase oracle or conditional inverse for any
of those missing capabilities.
