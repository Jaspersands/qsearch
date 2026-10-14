# Constant-Gap Syndrome Dilation: Overlap And Sector Price

Local constructive derivation and finite reference; external review pending.
No efficient receiver, new speedup or universal quantum no-go is claimed.
This follows an actual public operator beyond polynomial filters of the raw
Gram and asks whether its favorable spectral gap improves source access.

## A Public Hamiltonian With Exactly Known Gap

Use the actual native word frequency f_A(w), D=3^M and N=q^n. Add an
nr-trit syndrome register z in Z_q^n. The reversible public operation

    T_f |w,z> = |w,z+f_A(w)>

has M label-conditioned modular shifts per coordinate, not a preimage oracle.
Let H0=sum_j(I-|+_3><+_3|_j) tensor I_z and H=T_f^* H0 T_f.
Every term is a commuting conjugated projection. H has spectrum0..M,
positive gap EXACTLY1 and ground rank N. If normalized to operator norm1,
its gap is1/M, not1. Both its diagonalization and joint ground test are
constructive: apply T_f, inverse word F3 gates, coherently test all word
digits0, and uncompute if coherent output is required. All failures remain.
Source/gate errors and physical modular-arithmetic compilation are not free.

The finite implementation applies actual permutations and local mixers to
complete joint amplitude arrays. It allocates neither a dense (DN)^2
Hamiltonian nor a granted fibre projector. Its stated caps apply to the whole
reference state, not partial calculations quietly relabelled successful.

## Noncommuting Effective Word Effects Really Exist

Define Phi_t(w)=exp(2*pi*i*t.f_A(w)/q)/sqrt(D) and the PLUS-sign syndrome
Fourier basis chi_t(z)=exp(2*pi*i*t.z/q)/sqrt(N). T_f acts on that work sector
by multiplying the word by exp(-2*pi*i*t.f_A(w)/q). If the public syndrome
ancilla has Fourier diagonal weights p_t, compressing the JOINT ground
projector back to the original word input gives

    E_p = sum_t p_t |Phi_t><Phi_t|.

This depends only on the Fourier diagonal of an arbitrary pure or mixed
ancilla, not its off-diagonal coherences. The computational-zero ancilla has
uniform p and yields E_p=K=J^*J. A single public Fourier sector gives a
rank-one word effect that GENERALLY DOES NOT COMMUTE with K on unbalanced
fibres. For words w,v in differently sized fibres,

    [K,E_t]_(w,v) = (m_f(w)-m_f(v))/D^2 * exp(2*pi*i*t.(f(w)-f(v))/q).

A nonzero rational prefactor certifies noncommutation without trusting a
floating norm. Such witnesses are retained from real original-data controls.
Thus this is not merely a polynomial of K, or a claim that all alternatives
must commute. Noncommutation alone is nevertheless not a breakthrough.

## The Uniform-Secret Source Overlap Is Unchanged

For arbitrary FIXED original error phases independent of the secret,
psi_(s,e)(w)=Phi_s(w)*exp(i*theta_e(w)). Fix A and any label-only ancilla.
Average over the actual uniform original secret s in Z_q^n. Fourier
orthogonality gives

    E_s <psi_(s,e), E_p psi_(s,e)>
      = D^-2 * sum_(w,v:f(w)=f(v)) exp(i*(theta_e(v)-theta_e(w)))
      = <psi_(s,e), K psi_(s,e)> <= C_A=sum_sigma(m_sigma/D)^2.

The right side is independent of s and of the ancilla weights. This covers
all label-only quantum-generated syndrome ancillas, not just our three
explicit easy preparations. It needs no label randomness for the per-A
identity. Under IID full-root original labels,

    E_A C_A = 1/N + (1-1/N)/D <= (1+3^-surplus)/N.

Uniform PRIMITIVE-secret conditioning costs at most division by1-3^-n,
using nonnegative acceptance and the conditioning mass, NOT an additive TV
penalty that would swamp the rare branch. The IID uniform original-value
null accepts with probability1/D, since trace(E_p)=1.

A fixed or label-only known mask simply permutes the uniform secret sweep.
A RESPONSE-ADAPTIVE mask does not. The implemented countercontrol runs a
paid public unit-basis noiseless decoder on original records, then chooses
mask=-decoded_secret. With the public Fourier-zero work sector its ground
acceptance is1. No secret enters that decoder. This classically easy source
counterexample rules out extending our general-ancilla bound to arbitrary
response-adaptive masks. Computational-zero work is different: its effect
K commutes with all fibre-constant masks and retains that invariance.

Neither the average overlap nor the primitive bound is a per-secret upper
bound. A fortunate public sector can accept its matched noiseless secret
with probability1. Entire uniform-secret sweeps, not selected lucky sectors,
test the resource claim. Quantum preprocessing that uses responses or
entangles the initial word and work registers remains outside this cut.

## Actual Readout And Classical Comparison

For our three explicit public ancillas, measure the work Fourier sector
BEFORE the diagonalizing circuit. Its projectors commute with T_f and
word operations, so this preserves the FULL measured word/sector law.
Conditional on t, the actual original-data word state remains a product;
each local inverse F3 probability is a three-term known-phase sum. A
classical counterpart samples the public sector and these M local outputs.
All word failures are kept, not replaced by an acceptance-only estimate.
Certified finite-coin sampling is an integration obligation, not implemented
by floating reference probabilities. Arbitrary quantum-generated ancilla
distributions are NOT assumed classically sampleable. Coherent amplification
and noncommuting work-register interleaving are not classically simulated.

Ordinary initial-state/ground-flag amplification satisfies
E P_ground(t) <= (2*t+1)^2 * E P_ground(0). A constant mean ground mass
therefore still costs order sqrt(N) iterations in this family despite its
constant UNNORMALIZED Hamiltonian gap. This is a scoped overlap price,
not a general oracle lower bound for all quantum algorithms.

## A Known Rank-One Adiabatic Driver Does Not Fix It

The original-data initial state is known, so its rank-one projector is a
legal costed primitive here, unlike an inverse for an opaque supplied state.
For the SPECIFIC two-projector interpolation

    H(lambda)=(1-lambda)*(I-|initial><initial|)+lambda*(I-P_ground),

the initial vector and its ground projection span an invariant active space.
Writing p=||P_ground initial||^2, its eigenvalue separation squared is
1-4*lambda*(1-lambda)*(1-p), minimized at lambda=1/2 with value p.
Thus a constant FINAL band gap does not make this path's active gap constant.
For ground rank N>1, the other N-1 ground-band directions have eigenvalue
1-lambda. The full lowest-level separation is not the active two-level
separation and closes toward the degenerate endpoint; do not confuse the two.
This neither proves an adiabatic runtime lower bound for arbitrary schedules
nor rules out different drivers, response-sensitive coupling or work mixing.

## Research Decision

The useful escape criterion is stronger than either "good spectral gap" or
"noncommuting observable": obtain nonnegligible source overlap through paid
response-sensitive joint processing, and defeat the measured sector closure.
This construction is a baseline to reject free-ground-access proposals.
It does not show that such an escape mechanism is impossible.

    python theorems/native_syndrome_dilation.py --write
    node research/certificates/native_syndrome_dilation_crosscheck.js
    python -m pytest -q tests/test_native_syndrome_dilation.py
