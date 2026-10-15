# Coherent Sine-Window Lattice Source

This implements the saved sine-window specification: a deterministic packet
unitary, public point-addition compiler, complete finite Gram/readout reference,
actual cyclic Fourier samples and opaque destructive physical operations.
It supplies neither a hard lattice family nor an efficient noisy receiver.

CLI: `python qsearch.py lattice-sine-window-source`.
Artifact: `research/phase_workbench/lattice_sine_window_source.json`.
The original derivation remains in LATTICE_SINE_WINDOW_SOURCE_SPEC.md.

## Existing Literature And Scope

The cached Regev source `research/literature_cache/cs_0304005_source/quantum_average.tex`
already implements the SAME added-localization-register pattern using balls:
Section "An Improved Algorithm", `improved_main_lattice_lemma`, adds the public
lattice point into a prepared spatial packet. Its guarantee and norm/residue
guesses must not be ignored when comparing reductions. This implementation
uses a different compact known packet and explicitly traces its localization
register. No new reduction exponent, cryptographic hardness or novelty is claimed.

The current q-ary n^3-gap controls were all LLL-recovered. A source with a
better noise-versus-gap budget is useful research leverage, not evidence that
the resulting lower-gap instances resist classical algorithms. New families
still need public LLL/BKZ/SIS baselines. Constant noise only helps IF a robust
efficient decoder exists; information-theoretic PGM robustness is not one.

## Deterministic Packet, Not Exponential Postselection

For K=2^w, the known packet is psi(x)=sqrt(2/K)sin(pi*x/K) for x0..K-1.
The flag1 branch of W has probability1/2. Matched pi/2 amplification uses
W S_zero(i) W^dag S_good(i) W, followed by a known linear phase, a global
phase and flag X. Its KNOWN-ZERO parent gives exactly the desired packet and
zero flag/work in the ideal circuit. AND workspace clears on arbitrary
data/flag superpositions; the flag itself is not claimed clear on arbitrary
inputs. Inverse roundtrips are tested separately.

The compiler uses a clean Toffoli AND ladder, NOT an exponentially synthesized
ancilla-free reflection. Width w uses2w qubits,3 W/W^dag calls,2(w-1) Toffolis
and11w+9 logical instructions. Counts are checked against the compiled circuit.
Angles/global phase have total absolute pi weight33/4-7/K. Machin pi enclosures
bound binary64 parameter error. Retained-angle parameter error and total
distance from an ideal full QFT (including omission) are separate ledgers;
hardware, arithmetic synthesis and simulator
roundoff remain explicitly uncertified. Unsupported normal-angle encoding and
resource limits fail as UNKNOWN, never as an impossibility theorem.

## Public Source And Clean Arithmetic

Inputs are an integer ROW basis B, splitting prime p, residue g, coordinate j,
parent side M and packet side K. The splitting prime has an exact recursive
order certificate. No short vector, shift or preimage list enters compilation.

Prepare uniform colour b and a in[0,M)^n and product packets. Compute
x_b(a)=(a D_p+b g e_j)B in shared signed workspace, ADD it into the SAME
packet registers, then uncompute point/constants/carry. Original packet
positions are not copied. Signed widths certify injective physical output
encoding, including negative B entries. Qiskit's CDKM fixed adder supplies
the arithmetic. Original a wires plus gap bits are a SINGLE cyclic position
register N=(2M)^n; no copied-a garbage or tensor-QFT substitution is allowed.

Trace localization y, apply positive cyclic QFT and measure ONLY its label.
Conditional snapshots retain y unmeasured, so the colour density is genuinely
mixed. Whole-register feed-forward plus per-shot key/multiplicity checks reject
deferred or averaged snapshots. All emitted states/preparations and packet
W calls are charged; solver receipts contain labels/ancestry, not private states.

## Ideal Instrument And Promise Boundaries

The reference computes ALL parent-pair Gram entries from PUBLIC points:
rho[(b,a),(c,z)]=product_i A_K(x_b(a)_i-x_c(z)_i)/(2M^n), where A is packet
autocorrelation. Exact dyadic cyclotomic arithmetic gives the complete label
Born law, not a selected fibre or normalized guessed state. Dense references
are explicitly capped diagnostics, never polynomial preimage or receiver APIs.

Under a primitive shortest vector u=dB, correct residue d_j=g modp, and
lambda2^2>nK^2 plus(p-1)^2||u||^2>nK^2, only desired cross-colour shifts survive.
The second inequality must use p-1: the alias(1-p)u is otherwise missed.
The parent displacement is h_j=(d_j-g)/p, h_i=d_i otherwise. Every label is
uniform; the colour off-diagonal is v exp(-2*pi*i*k*J(h)/N)/2, with

    v=product_i A_K(u_i) product_i max(0,1-|h_i|/M).

This marginal is equivalent to good DCP qubits of weight v plus balanced
bad-basis qubits of weight1-v. There is NO clean flag. Keeping/disclosing y
changes the conditional model and is not silently allowed.

Public norm intervals and B^(-1) give conservative coefficient/box bounds.
The sufficient loss bound is(242/49)||u||^2/K^2+||h||1/M. Gap/norm/correct-trial
premises are ASSUMPTIONS unless separately certified; the public budget function
does not infer them from B. Coordinate/residue/length guesses remain paid.
The conditional gap scale sqrt(n/epsilon) is a research target, not a proved
algorithmic speedup or a claim superior to all existing reductions.

Truncated QFTs have a separate complete finite instrument reference, computed
from the retained H/CP gate kernel. Their phases need not be characters of
the cyclic hidden shift. Approximate physical batches are permitted, but
neither their private template audit nor their metadata grants an exact-DCP
promise. Actual QFT usage is capped and charged before sampling.

Private forward templates run AFTER sampling. They are never used to choose
source parameters or screen trials for the receiver. Wrong residues and aliases
are explicit falsifiers; even an exact finite match does not establish the
growing reduction or its required inverse-logN noise budget.

## Backend And Inverse Access

SinePhysicalBackend reuses existing destructive CNOT/Pauli operations and
ancestry/no-reset guards. It deliberately has NO DCP-promise/trial selector:
off-promise and approximate samples remain physical inputs, not certified
DCP algorithms. A batch is claimed once; no duplicate roots, unpaid retries
or copying. RNG seeds belong to the diagnostic harness, not a solver oracle.

Only the FULL compiled parent has an inverse, including localization and
label registers. Tracing y does not grant an inverse/reflection for a mixed
colour qubit. Projecting a specified label while retaining the full pure
environment pays its Born mass (1/N in valid controls). Gate-error bounds are
JOINT-channel statements, not rare-conditional accuracy without a mass bound.

## Live Controls And Remaining Work

Signed1D controls check arithmetic and known shift0. A nontrivial2D public
control B=((17,0),(16,1)),p7,g1,M2,K4 yields h=(0,-1),visibility1/4 and all16
cyclic labels. It is classically easy and too noisy for the current inverse-logN
budget. A p3 alias control MUST fail the single-shift template. The large
public source is compiled, not simulated, not claimed hard or a receiver.

The live workflow charges34 actual preparations: four full-QFT controls with
eight shots each and one cutoff-zero control with two shots. The independent
JavaScript checker reconstructs sine-product autocorrelations, EVERY public
Gram entry and label density, a gate-order QFT kernel, signed resource counts,
prime certificates, Machin angle enclosures, private forward templates and
every emitted conditional density. It does not independently execute Qiskit,
certify simulator roundoff, or prove the public gap promise.

Dedicated tests check width1..6 coherent packet amplitudes, arbitrary-input
unitarity/work cleanup, width64 compilation, signed in-place arithmetic,
mixed colour states, paid label-projection inverse, source/reference binding,
approximation/query caps, destructive ownership and certificate tampering.
Run `python -m pytest -q tests/test_lattice_sine_window_source.py` and
`node research/certificates/lattice_sine_window_source_crosscheck.js`.

Next experiments: lower-gap q-ary sweeps with matched classical attacks;
constant-noise versus inverse-logN source budgets; norm/outer-guess costs;
and a genuinely efficient unknown-copy receiver. No private phase tables,
coherent lattice-Gaussian oracle, free normalization or source trial flag
may enter those experiments. No speedup candidate or active negative is created.
