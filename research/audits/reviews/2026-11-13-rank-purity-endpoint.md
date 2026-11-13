# Rank–purity endpoint: copy access and the actual remaining theorem

2026-11-13. Independent source-contract and composition audit. No numerical
controls, network, paid reports, preparation oracle, or shared-status edits.
Physical LF locators below count `split('\n')`, not form-feed-separated lines.

**Disposition.** The proposed conditional endpoint composes. For fixed known
absolute constants c>0 and C>0, the promise

    |psi> pure and normalized, chi(psi)<=k, Pi(psi)>=c k^(-C)

gives a quantum measurement/classical-processing algorithm using
poly(n,k,log(1/eta)) time and fresh copies, returning a classical stabilizer
tableau whose squared overlap is inverse-polynomial in k, with probability
at least 1-eta. Rank is used only to supply the purity lower bound.
The new structural gate is substantial: a uniform polynomial rank–purity
bound is equivalent, up to constant exponents, to a uniform polynomial
rank–stabilizer-fidelity bound. No such new rank bound is proved here.

## 1. Exact normalization

Put N=2^n, W_(a,b)=i^(a.b) X^a Z^b, and

    r_x=<psi|W_x|psi>,  p_psi(x)=|r_x|^2/N,
    Pi(psi)=N^(-1) sum_x |r_x|^4.

For a pure normalized state, Pauli orthogonality gives sum_x |r_x|^2=N;
thus p_psi is a distribution and 0<Pi<=1. The phase converting X^a Z^b
to the Hermitian W_(a,b) does not affect Pi. There is no extra N factor.

Independently, let f(x)=sqrt(N) psi_x, with uniform expectation on F_2^n.
Then E|f|^2=1. For D_a f(x)=conj(f(x))f(x+a), normalized Fourier transform
gives |D_a f-hat(b)|=|r_(a,b)|. Consequently

    ||f||_(U^3)^8 = E_a sum_b |D_a f-hat(b)|^4 = Pi(psi).

This is exactly the quantum Gowers normalization in `structure.txt`
LF932-956, not the ordinary inverse theorem for functions bounded by one.
Here ||f||_infinity may be sqrt(N).

The characteristic and Weyl distributions are defined in that source at
LF732-747: q_psi(x)=sum_y p_psi(y)p_psi(x+y). Fact 2.10, LF947-956, says

    Pi^2 <= Q := E_(x~q_psi)|r_x|^2 <= Pi.                 (1)

Theorem 1.7, LF961-962, therefore supplies absolute constants a>0,b>1
such that

    F_S(psi):=max_stabilizer phi |<phi|psi>|^2
        >= a Q^b >= a Pi^(2b).                           (2)

The theorem is stated for arbitrary pure quantum states, so it does not
require flat amplitudes, known stabilizer support, or controlled coefficients.

## 2. Actual native algorithm and its output

Arunachalam–Dutt, *Learning stabilizer structure of quantum states*, retained
`research/audits/sources/stabilizer_rank_priority/structure.txt`, Theorem 1.3 LF180-183,
states: given copies and F_S>=tau, output a stabilizer of squared overlap
at least tau^s for an absolute s>1, in poly(n,1/tau,log(1/eta)) time/copies.
That version explicitly assumes high-doubling algorithmic PFR.

Arunachalam–Dutt–Grewal–Gupte, *Marton's conjecture in polynomial time*,
retained `research/audits/sources/stabilizer_extent/marton.txt`, Theorem 8.5 and Corollary 8.6
LF3152-3161, explicitly remove this assumption from this same copy-only
self-correction guarantee. The approximate-PFR interface is Theorem 8.2,
LF2969-2973: independent R-uniform samples, membership access, polynomial
cost in n,K,R,log(1/eta), output a subspace basis. Footnote 14, LF3190-3195,
addresses the self-correction BSG sampling distribution: its flatness loss
is polynomial in the inverse signal, so these are internally compiled
interfaces, not additional input oracles. This audit uses the stated
Corollary 8.6; it does not independently reprove the entire PFR algorithm.

Set epsilon_0=min(1,c k^(-C)), gamma=epsilon_0^2, and
tau=a epsilon_0^(2b), decreasing a to at most one if necessary. Apply (2)
and unconditional self-correction. With probability >=1-eta the output has

    |<phi|psi>|^2 >= a^s epsilon_0^(2bs),                 (3)

and cost poly(n,epsilon_0^(-1),log(1/eta)). For fixed c,C this is polynomial
in n,k,log(1/eta). Integer exponents rounded upward and rational constants
rounded downward provide a dyadic lower threshold with O(log(k+1)) bits.
The universal source constants and the assumed c,C are fixed algorithm
constants; no input-dependent overlap advice is needed. This is an
asymptotic polynomial theorem, not a supplied practical numerical exponent.

The output really has a classical tableau description. In `structure.txt`
Algorithm 7, LF2247-2285, symplectic Gram–Schmidt constructs a Clifford U;
the candidates are explicitly enumerated small stabilizer states phi_i
and observed computational strings z. The chosen output is
U^dagger(phi_i tensor |z>). Conjugating its signed Pauli generators gives
an O(n^2)-bit tableau in polynomial time. This does not require tomography
of an opaque output state.

Source LF204-213 explicitly distinguishes sample access from U_psi or
controlled-U_psi. The abstract p_psi identity must NOT be implemented by
asking for conjugated copies: the source notes at LF740-745 that directly
Bell-sampling p_psi uses |psi*>. The actual self-correction uses its
copy-only Bell-difference/measurement routines. Neither (1) nor the proof
of (2) adds a conjugation, inverse-preparation, residual-state, or
postselection oracle to the native endpoint. Copies may be jointly
measured in the constant-copy operations permitted by the source.

## 3. Converse: the rank condition is not an easier new structural gate

For any stabilizer phi, let L be its unsigned stabilizer space and epsilon_x
its valid Pauli signs. Its projector gives

    |<phi|psi>|^2 = N^(-1) sum_(x in L) epsilon_x r_x
      <= [N^(-1) sum_(x in L) |r_x|^4]^(1/4) <= Pi^(1/4).

The first inequality is Holder on the N-point set L. Maximizing yields

    F_S(psi)^4 <= Pi(psi),
    a Pi(psi)^(2b) <= F_S(psi) <= Pi(psi)^(1/4).          (4)

Thus uniform F_S>=c' k^(-C') on all rank<=k pure states implies
Pi>=(c')^4 k^(-4C'), and the proposed purity bound implies the polynomial
fidelity bound by (2). Existence of the proposed algorithm likewise implies
existence of an inverse-polynomial-overlap stabilizer. The endpoint is a
polynomial rank-versus-fidelity question in another quantitatively
equivalent form; the source algorithms already pay the extraction step.

## 4. Existing baseline and exclusions

The correct extent file is `research/audits/sources/stabilizer_rank_priority/extent.txt`.
Sinha–Lovitz Theorem 1.1 LF132-140 gives squared extent
xi=Lambda_S^2 <= 2^(O(sqrt(k log(k+1)))) for normalized rank<=k states.
Its convention is explicit at LF437-465; the Marton/learning papers use
the unsquared coefficient norm. The overlap inequality xi F_S>=1 is
LF467-471. This supplies only the stated subexponential-in-k guarantee,
not the desired polynomial one. Corollary 1.6 LF223-227 gives the stronger
output of full tomography at that subexponential time/copy cost.

Our conditional polynomial endpoint returns one high-overlap stabilizer,
not a stabilizer decomposition, near-optimal agnostic answer, or complete
tomography. No subtraction-and-repetition argument is admitted: preparing
normalized residuals and controlling their new rank/cost would need a
separate theorem. The exact-rank, normalized-pure-state, fresh-copy promise
is retained; no mixed-state or approximate-rank extension is asserted.
