# Uniform Central Measurement Without Source Inversion

2026-10-24. Constructive mathematical audit and executable resource plans.
This is a standard phase-estimation construction specialized to the SAME
Rees input, not a new quantum algorithm, independent review, Lean extension,
or gate-level implementation. The finite controls test interfaces, not
asymptotic advantage. All files live outside the migrating main checkout.

## Question And Answer

Does the abstract central-character instrument in the checked recursive
source proof require an exponential-size Fourier matrix, hidden subgroup
coordinates, a source inverse, or a favorable character? No, under the
explicit prime-field coordinate model: it has a uniform approximate
implementation using public central translations. Crucially, those
translations have efficient powers. Generic black-box phase estimation
does NOT by itself provide polynomial cost in log p.

The construction also supplies terminal abelian measurements and capped
public address preparation. It does not implement the general diagonal
equation solver or synthesize the entire Rees receiver into gates. The
base BCH/Lazard correspondence remains imported mathematics.

## Same Native Input, No Hidden Advice

Input is a verified prime p, explicit genuine Lie structure constants for
an m-dimensional L/F_p of actual nilpotency class c<p, and independent
ordinary mixed coset states in the coordinate basis of its Lazard group.
No description of h=log H is available to any operation below.

Compute gamma_j(L) by span and bracket operations, stopping at the first
zero space. Use the ACTUAL class, not a possibly huge supplied upper bound.
The nonzero descending chain strictly decreases, so this preprocessing is
polynomial field linear algebra. A basis B_j of gamma_j gives the actual
Rees coordinate blocks x_j in F_p^(r_j), r_j=dim gamma_j. These are not
associated-graded dimensions. A stage d is blocks1,...,d; the public section
zero-pads blockd. Its central kernel is exactly blockd.

Because this block is central, in first-kind BCH coordinates multiplication
by z in blockd is ordinary addition in that block and changes no other
coordinate. Thus R(z)|x> = |x*z^-1> subtracts z. For a public basis vector
e_j, R(e_j)^(2^k)=R((2^k mod p)e_j). This is ONE controlled modular addition
of a known constant, not 2^k calls to an unknown unitary. Invalid bit strings
outside0,...,p-1 must be handled by a bijective extension, such as identity
on invalid coordinate words. All arithmetic workspace is uncomputed.

The existing public BCH ODE routine already avoids enumerating free Lie
words. Reversible evaluation of a public arithmetic circuit is different
from inverting the unknown source preparation. This pass neither replaces
that routine nor claims it is a verified quantum compiler.

## Sign And Instrument

Let chi_lambda(z)=exp(2 pi i <lambda,z>/p). The projector is

    P_lambda = p^-r sum_z chi_lambda(-z) R(z).

Its matrix entries give precisely the existing measuredState expression:

    (P_lambda rho P_lambda^*)[x,y]
      = p^-2r sum_(z,w) chi_lambda(z) conj(chi_lambda(w))
          rho[x*z^-1, y*w^-1].

Indeed the range of P_lambda has eigenvalue exp(2 pi i lambda_j/p) under
R(e_j). This matches the positive-character convention in the frozen Lean
instrument. The generator powers below therefore use right subtraction,
not addition or left multiplication.

Let M=2^t. For each of the r commuting generators, apply ordinary binary
phase estimation A_j: Hadamards, t controlled public powers, inverse
power-of-two QFT. Coherently compute

    D(a) = nearest_integer(p*a/M) mod p

into a separate label register, then apply A_j^-1. Use distinct phase
workspace for each coordinate; residual approximate work is not presumed
exactly zero or reused for free. Finally measure all copied labels and
discard phase work. Keep the FULL original target register. No target
copy is prepared, inverted, or discarded by this measurement.

This realizes a complete approximate Lueders instrument. In particular,
it preserves arbitrary coherence within a degenerate character space and
works with an arbitrary entangled reference. Measuring the target's own
Fourier-transformed coordinate and leaving it in the computational label
basis is NOT the same instrument. A finite falsifier below breaks the
subsequent right-translation correlation by modulus one.

## Error Bound For All Inputs And Records

On eigenphase theta=lambda/p, the phase-estimation amplitude at a is

    alpha_theta(a) = M^-1 sum_(k=0..M-1) exp(2 pi i k(theta-a/M)).

Write d_a=M*dist_circle(theta,a/M). For d_a>0, the geometric sum and
|sin(pi u)|>=2|u| for |u|<=1/2 give |alpha|^2<=1/(4d_a^2).
If D(a) is wrong, d_a>=M/(2p). There are at most two grid points per unit
distance shell. For M>=8p, summing the inverse-square tail bounds the wrong
label probability by 4p/M (a deliberately loose bound). Exact phases,
including lambda=0, have zero tail. Ties can be assigned either way.

For a joint character lambda, the r work registers factor and the wrong
label-vector probability is at most delta=4rp/M. Compare two isometries:

    V: |psi_lambda>|0>|0> -> |psi_lambda>|0>|lambda>
    W: compute A, copy D, uncompute A.

Before uncomputation, correct decoded amplitudes agree exactly. An incorrect
label is orthogonal to the correct label, contributing twice its probability
to squared norm. Therefore ||(W-V)|psi_lambda>||^2<=2 delta. Distinct joint
eigenspaces remain orthogonal throughout, so the same OPERATOR NORM bound
holds for all superpositions and arbitrary reference systems:

    ||W-V|| <= sqrt(8rp/M).

Measurement/discard is contractive. Hence the half diamond distance between
the complete recorded instruments is at most sqrt(8rp/M). There is no
division by Pr(lambda) and no favorable-record conditioning. Zero-mass
ideal records may acquire small error mass; they are part of this bound.

For target error eta choose the least power of two

    M >= 32rp/eta^2.

Then ideal-QFT instrument error is <=eta/2. There are2r QFT blocks; synthesize
each within operator norm eta/(4r), paying at most another eta/2 by
telescoping. Computing inverse circuits from the same synthesized public
circuit is allowed. The total instrument error is <=eta.

Resources: t=O(log p+log r+log(1/eta));2rt controlled modular translations;
2r binary-QFT blocks; r*t*(t-1) controlled rotations before synthesis;
r*(t+ceil(log2 p)) phase/label qubits plus polynomial decoder workspace and
the original target. Standard finite universal-gate synthesis adds
polynomial precision overhead. This is a uniform circuit-existence bound,
NOT a T-count or noise-tolerant implementation. The plans explicitly leave
gate synthesis and arithmetic implementation as separate dependencies.

The eigenvalue-measurement principle is prior art, not project novelty:
[Kitaev, Quantum measurements and the Abelian Stabilizer Problem](https://arxiv.org/abs/quant-ph/9511026).
The formulas and conservative complete-instrument bound above are derived
here to match the repository's exact sign, access and reference contract.

## Public Addresses Without Arbitrary-Modulus QFT

A fresh p-coordinate can be prepared by Hadamards on n=ceil(log2 p) bits,
reversibly computing the comparison x<p, measuring that flag, and retaining
only a successful public attempt. Success is p/2^n>1/2 and its state is
EXACTLY the uniform superposition on F_p. The flag is constant on the
success space and its workspace is cleared. Failed attempts contain no
hidden information and are discarded before native targets are acquired.

Cap each of D coordinates at T=ceil(log2(D/eta)) attempts. The probability
that any coordinate aborts is at most D*(1-p/2^n)^T<=D*2^-T<=eta. Successful
records all produce the same pure uniform address, so the full flagged
preparation differs from ideal by at most eta in half diamond distance.
This is bounded-runtime public rejection, not free hidden postselection.
One address uses at most DT comparisons/Hadamard blocks, O(D log p) output
qubits and polynomial workspace. Source errors and later aborts stay paid
separately. Addresses for different recursive nodes are fresh.

## Terminal Recovery And Whole-Tree Accounting

At stage1 the group is ADDITIVE L and the source is rho_h for the entire
hidden subspace, including its original derived coordinates. Use the same
character extraction with r=m and translations by the public coordinate
basis. Ideal labels are independent uniform elements of h-perp. Gaussian
elimination returns their common nullspace. On full rank this is all h;
under the imported Lazard correspondence a vector-space basis generates H.

For k samples and unknown codimension s<=m, the failure probability is at
most ((p^s-1)/(p-1))*p^-k. The resource plan uses s=m, never a hidden rank.
The exact spanning probability, used as a check, is
product_(i=0..s-1)(1-p^(i-k)). Quantum measurement and source errors are NOT
included in this classical rank bound and must be added separately.

For arities M_j, L=product_(j=2..c) M_j, and
N_j=product_(ell=2..j-1) M_ell, k terminal outputs use:

    native copies: c*k*L
    fresh addresses: k*(L + sum_(j=2..c) N_j)
    stage-j character measurements: k*N_j*M_j  (ALL targets)
    terminal character measurements: k.

All N_j*M_j targets are measured even when selected scales are zero.
Each has central rank r_j and its own complete-instrument error budget.
Allocate the allowed error across the actual counted operations; the
telescoping sum contains no hidden-branch probability denominators. At
fixed c the known sufficient arities are polynomial in m; log of their
product only increases t and T polynomially. No growing-class efficiency
claim follows. c=1 permits direct terminal readout, bypassing the cover.

The classical moment solver must accept EVERY observed label tuple and
verify nonzero support and moment cancellation before any controlled
action. Approximate measurements can produce labels forbidden by the ideal
hidden source; those are not a license to leave behavior undefined. The
published SDE guarantee applies to arbitrary label lists at sufficient
arity, not only the ideal label distribution. Its implementation remains
outside this pass:
[Ivanyos--Santha, Theorem3](https://arxiv.org/html/1503.09016v2).

## Adversarial Verdict And Remaining Blockers

This closes the alleged exponential-Fourier-table/source-inverse obstruction
at the level of a constructive uniform algorithm with an explicit complete
error bound. It does not extend the checked Lean theorem counts. It also
does not establish a new advantage: eigenvalue measurement and central
state conversion are known tools. The bounded-prime scope of the related
[Imran--Ivanyos algorithm](https://arxiv.org/html/2304.08376v1) remains intact.

Ways the construction fails if assumptions are weakened:

- Only U access, without efficient powers: the t power gates can cost
  Theta(M) repeated calls. The claimed poly(log p) bound is then unsupported.
- No valid central coordinate basis or noncommuting chosen generators:
  the common eigenspace proof and modular-translation shortcut do not apply.
- Wrong translation sign: labels are negated relative to the formal plan.
  A complete instrument comparison detects this even if cancellation happens
  to be sign-invariant when every label is reversed consistently.
- Leaving the target in its measured Fourier basis: subsequent arithmetic
  acts on the wrong state, despite correct output-label frequencies.
- Counting only active scales: source, measurement and memory costs are
  understated. Counting normalized positive branches only: error can be
  amplified by an uncharged rare outcome.
- Merely correct one-copy marginals: independent recursive source guarantees
  do not follow. No part of this pass removes that source premise.

The numerical controls use literal binary-controlled permutations, binary
Hadamards and FFTs to emulate the QFT, never the expected projectors inside
the operational routine. The comparator separately constructs the formal
projectors. Spectator/reference coherence, complete recorded outputs,
wrong signs, and wrong retained bases are tested. Large-prime plans use
exact integers without field enumeration; those are resource certificates,
not a large quantum simulation.

Next research decision: do NOT spend further passes proving standard QFT
facts or enlarging these controls. The highest-value unresolved questions
are novelty of the assembled theorem and a natural non-oracle application
surviving classical attacks. Full gate wiring and general solver integration
can be specified for Gemini after migration is verified; they should not
consume a separate long GPT theory pass unless they reveal a concrete gap.
