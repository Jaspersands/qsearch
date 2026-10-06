# Native DCP Path Codes Are Deferred Pair Fusion

LOCAL DERIVATION / REVIEW PENDING. No accepted candidate, new sieve, polynomial
decoder, generic DCP no-go or full classical state simulator. This pass closes
the concrete retained-register target from `DCP_PROJECTIVE_CODE_ADMISSION.md`.
It does not claim to have disproved all coherent extensions of phase fusion.

## Decision

Do not pursue fixed path-code signal benchmarks as a new algorithmic direction.
The six-to-two transformation is an explicit, linear-cost Clifford instrument:
ordinary native pair fusion, with a common parity bit retained coherently,
followed by Fourier-basis parity checks. Every syndrome has a closed formula.
Measuring the common parity gives an exact known-pair-fusion comparator.

The prior sign counterexample remains true, but its interpretation is weaker:
sign information survives in the measured comparator too. Extra parity
coherence can increase that statistic, yet no full-secret decoder, composable
known-label sieve rule or improved asymptotic resource bound follows.

## Source And Literature

Consume 2m independent native qubits
`|phi_(k_i,s)>=(|0>+exp(2*pi*i*k_i*s/N)|1>)/sqrt(2)` with public IID uniform
labels, N=2^n>=8. Registers are independent; labels may repeat. Gates below are
public and independent of secret AND labels. No chosen labels, cloned states,
unknown preparation inverse or reusable conditional phase oracle is supplied.
If generated through the standard full-DHSP-oracle bridge, charge 2m oracle
queries as well as its Fourier/label preparation overhead.

[Kuperberg, section 3, pages 2-3](https://arxiv.org/pdf/quant-ph/0302112)
explicitly uses a pair CNOT and parity measurement to obtain sum/difference
phase labels. [Regev, section 2.2](https://arxiv.org/pdf/quant-ph/0406151)
gives the native source and parity-fusion interpretation. These primary
mechanisms, not a literature-priority search, were inspected. The new path-code
identity and sign-loss calculations below are local derivations, not claims
that those papers state these particular formulas. All-paper proofs and every
possible coherent-fusion variant were not reviewed.

## Full Path-Code Instrument

For j=0,...,m-2, row j of M has ones on both qubits of pairs j and j+1.
The code consists of duplicate-coordinate vectors `(b_0,b_0,...,b_(m-1),b_(m-1))`
with even parity of b. It has rank m-1, MM^T=0, and doubly-even words.
Measure every commuting Z^(row j) and X^(row j), leaving exactly two qubits.
Write the respective syndrome bits as z_j and x_j.

Let d_0=q_0=0, d_(j+1)=d_j XOR z_j, q_(j+1)=q_j XOR x_j.
Let theta_i=2*pi*k_i*s/N, beta=sum_i theta_i/2, and

`alpha_(j,p)=(theta_(2j)+(-1)^(p XOR d_j)*theta_(2j+1))/2`.

In the public logical basis (p,t), where p is the common pair-parity reference
and t is a Fourier-basis logical bit, the UNNORMALIZED amplitude is

`A_(z,x;p,t)=2^(-m/2)*exp(i*beta)*product_j f_(t XOR q_j)(alpha_(j,p))`,

`f_0(alpha)=cos(alpha), f_1(alpha)=-i*sin(alpha)`.

The probability of a branch is sum_(p,t)|A|^2. All 4^(m-1) branches are retained.
Z syndromes alone are exactly uniform for each fixed secret and label packet;
complete syndrome probabilities need not be uniform on that packet. With IID
uniform labels and NONZERO secret, mean complete-syndrome probability is
4^(-(m-1)). A specified syndrome plus measured p has mean 2^(-(2m-1)).
There is no per-instance lower bound and no replacement of E[1/P] by 1/E[P].
The mean follows by averaging the source to the maximally mixed input, since
the nonzero cyclic character has zero mean. It fails at s=0 and can fail after
label-dependent packet selection. The producer retains all failed/zero branches.

### Proof And Public Compiler

For original pair bits, put r_j=bit_(2j), p_j=bit_(2j) XOR bit_(2j+1).
The Z checks enforce p_j=p XOR d_j without measuring p. X checks translate
adjacent r bits; their character condition is q_j XOR q_(j+1)=x_j.
Fourier transformation of the retained `a=XOR_j r_j` gives bit t. The amplitude
is the 2^(-m/2)-normalized character sum over all r, with original phase
`sum_j(theta_(2j)*r_j+theta_(2j+1)*(p_j XOR r_j))`. Factoring each two-term
sum gives the displayed cos/sin products, including their complex phases.

An explicit circuit, in little-endian original qubit numbering, is:

1. For each pair j, CNOT 2j -> 2j+1, producing r_j,p_j.
2. For j=m-2 down to 0, CNOT 2j+1 -> 2j+3, producing z_j on qubit 2j+3.
3. For j=1,...,m-1, CNOT 2j -> 0, producing a on qubit 0.
4. Hadamard every qubit 2j for j>=1 and qubit 0.
5. Measure qubits 2j,2j+1 for j>=1. Their Fourier bits are q_j; compute x_j
   by adjacent XOR. Retain qubit 1 as p and qubit 0 as t.

Exact cost: 3m-2 CNOTs, m Hadamards, 2m-2 measured qubits and two retained
qubits, with no ancilla, adaptive gate or postselection. This describes a
specified algebraic measurement, NOT restored circuit search. The local
compiler exports the actual gate list. The general Kraus identity follows
from the invertible binary coordinate map and its character transform. Tests
also check every computational-basis input for m=3, all syndromes of the
previous purified Pauli instrument for m=2,3,4, and full native controls up to m=5.

### Measured-Fusion Comparator

If p_j are individually measured immediately after step 1, each of their
2^m patterns has probability 2^-m. The remaining qubit r_j is the ordinary
phase state with known label `k_(2j)+(-1)^p_j*k_(2j+1)` and branch global phase
`exp(i*theta_(2j+1)*p_j)`. Keep those global phases when comparing Kraus vectors;
they become relative phases if the parity register is retained coherently.

Apply the same r parity compression and Fourier checks. The resulting
unnormalized logical t state for each full measured parity pattern equals
`A_(z,x;p,.)` exactly. Thus measuring p in the coherent output is the same
instrument as measured pair fusion followed by these checks, up to a public
relabeling of the classical record. Discarding measured p gives its dephased
version. This is NOT equality of the original coherent and dephased channels.
It is NOT a classical simulator of native quantum samples.

## Sign Retention And Its Scaling Falsifier

For native input, changing s to -s is global X on all physical qubits, up to
an overall phase. When m is even, the all-ones word belongs to the path code:
the complete quantum instrument erases this sign distinction in every source.
When m is odd, global X becomes logical Z_t, up to a syndrome-only phase.
Sign is a two-hypothesis diagnostic, NOT reconstruction of the unknown shift.

For any unnormalized branch vector u, its sign partner is Z_t u. Coherent
branch trace distance is `2*||u_(t=0)||*||u_(t=1)||`. Measuring p changes it to
`2*sum_p |u_(p,0)*u_(p,1)|`; hence it cannot improve sign distinguishability.
The coherent statistic can be strictly larger, without exceeding input
distinguishability. All branches use physical probabilities, not an average
of normalized conditional-state distances.

For odd m, summing the MEASURED comparator over all x,z,p gives exactly

`D_measured(k,s)=product_j (|sin(theta_(2j)+theta_(2j+1))|
                          +|sin(theta_(2j)-theta_(2j+1))|)/2`.

Both complementary t products use one sine and one cosine per pair. Their
absolute product is independent of x; summing all z,p enumerates every
measured pair-parity pattern. This proves the formula without dropping labels.
For odd secret and IID uniform labels, each sum/difference phase is uniform
on Z_N, so

`E_k D_measured=((2/N)*cot(pi/N))^m < (2/pi)^m`.

For nonzero even secret, replace N by character order N/gcd(N,s); the formula
applies when that order>=4. It is zero for order 2 and for even m. The mean
is the trace distance of the FULL public-label cq ensembles, not a hidden-label
average. It is a scoped loss of this particular measured instrument; the
coherent parity extension, adaptive selection and arbitrary DCP decoders are
NOT excluded. No generic sample/runtime lower bound is inferred.

For the same eight unfiltered six-qubit draws as the prior pass, measured
distances are approximately .670,.157,.240,.074,.221,.160,0,.286. Coherent
distances are approximately .897,.368,.351,.359,.415,.570,0,.532. Seven signals
survive without parity coherence, and the degenerate eighth source is kept.

## Nonlinear Phase Is Not Known-Label Closure

For odd m, x=z=0 and measured p, transform t back to a. The amplitudes have
equal modulus, since their cosine and sine products are in quadrature:
`A_a proportional C+(-1)^a*(-i)^m*S`. The phase ratio is nonlinear, determined
by `product_j tan(alpha_j)`. This is a legitimate conditioned flat phase qubit;
it is not automatically `|phi_(L,s)>` for a publicly known modular label L.

As a function of continuous phase parameter, the zero-branch phase has first
nonconstant term of order m when all pair sums are nonzero. For m>1 this is not
a nonconstant linear phase law. Discrete modular coincidences or special
label families are not ruled out by that observation. A separate N=32
calibration with labels [1,2,3,5,7,11] checks all nonzero odd-secret branches:
every L in Z_32 fails, with minimum worst-secret complex ratio error about1.774.
This packet is a COUNTERCONTROL, not filtered IID-source advantage evidence.

Consequently, ordinary sieve metadata cannot simply attach one sum/difference
label to this output or use its two-adic valuation. A decoder using nonlinear
phase functions remains possible in principle, but must provide an actual
uniform operation and complexity argument. A proposed-secret amplitude can
be evaluated in O(m) arithmetic here; that does not prepare an unknown state,
invert its preparation or search an exponential secret space efficiently.

## Attempts To Kill The Diagnosis

- **Only the zero branch was checked:** false; full complex amplitudes and
  charged probabilities for every syndrome are replayed independently.
- **The retained coherence is unnecessary in every protocol:** not proved;
  dephasing can strictly decrease distinguishability. No Blackwell dominance,
  decoder equivalence or coherent-protocol impossibility is claimed.
- **The sign signal establishes a new primitive:** false; it survives the
  explicitly derived measured pair-fusion comparator too.
- **Nonlinearity means a new algorithm:** not without a usable target, native
  preparation law, all-branch strategy and polynomial or improved sieve cost.
- **Select a large good branch for free:** mean specified-branch yield is
  exponentially small; label-conditioned selection needs a new proof and cost.
- **The measured exponential sign loss proves generic DCP hardness:** false;
  it applies only to this full measured path instrument, not general receivers.
- **A decomposition into familiar gates disproves all novelty:** false;
  useful new algorithms can use familiar gates. The present evidence removes
  the primitive-only rationale, not a future end-to-end algorithmic theorem.

## Artifacts And Next Decision

Module/tests: `dcp_path_code_fusion`; live report under `phase_workbench`;
independent JS checker under `certificates`; matching hypothesis/source audit.
Full-state and all-syndrome enumerations are bounded calibrations. Symbolic
compiler resources, mean yield, path kernel and scoped sign decay scale.
The exact fixed-code kernel is
`K=1/2+((3/2)^m+(1/2)^m)/4`, by summing even-weight duplicate words and their
shortenings. It remains only a classical collision metric, not full inference.

Independent checker:14 native controls,3,104 complex logical amplitudes,
776 full quantum branches,1,552 measured-fusion blocks and8 exact ledgers.
Verification:22 new focused tests and118 related tests pass in10.91s.
Python/JS syntax, strict JSON and scoped whitespace checks pass.
No full production/CLI validation or independent human theorem review claimed.

Gemini: integrate this as a scoped equivalence/falsifier, preserve all syndromes,
compiler costs, measured-vs-coherent distinctions and zero branches. Do NOT
accept a candidate on sign retention or nonlinear angle alone. Full registry
and CLI wiring/validation remain delegated.

GPT next: stop collecting fixed-code statistics. Prefer a literature-grounded
hidden-ELEMENT state-isomorphism transfer audit, or an actual source-legal
decoder/reduction that uses coherent phase functions. Returning to this family
needs a concrete blocker-removing operation, not a new small-block plot.
