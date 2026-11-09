# Exact oscillator pairing and independent mechanism triage

2026-11-06. A scoped algebraic falsifier and direction-selection record.
No new quantum algorithm, novelty, separation, or general nonlinear no-go.

## Question chosen by external value

After closing the sparse characteristic-zero relation pass, compare paid
operations for native reconstruction/optimization instead of automatically
extending its growing-degree arithmetic residue. Start from STATE/TRAPS;
the corpus queries below preceded literature checks and construction.

The strongest unresolved target in this comparison is polynomial-time
recovery of a growing-degree monic squarefree Q over F_p from its padded
quadratic-character BIT oracle. This is the published query/time gap, not
a new oracle problem. The current uniform circuit composition costs
exp(O(d log d))*poly(log p). Removing its factorial source penalty would
materially change that upper bound. This pass did NOT find such an operation.

## Candidate contracts and admission decisions

| Route | Native input/output and mechanism | Target resources and classical comparator | Obligation and cheapest falsifier | Decision |
|---|---|---|---|---|
| Nonlinear oscillator relabeling | Public reversible pi on m bits; use the Section6.3 Fourier/Dicke construction to optimize the represented position score | Desired poly(m) preparation/readout and an optimization gain; Gaussian elimination and explicit position-shell sampling apply under the exact pairing premise | A map sigma must satisfy sigma(y).z=y.pi(z) for ALL y,z; test this identity before constructing a Hamiltonian | The identity forces linearity; invertible case is classically solved, as proved below |
| Complete-list DQI beyond unique decoding | Explicit OPI tables/evaluation map; complete syndrome lists, fixed padded index and coherent uniform-index projection | Polynomial complete-list decoder, source preparation and inverse herald probability; Prange restarts, information-set/line search and existing full-table attacks | Charge success Z/(L Z0), never replace a list by one witness or vary padding with its size | Already Jo Sections4-6 and SCALAR_OPI_RANDOM_TABLE_LIST_SAMPLER.md; no new operation |
| Rank-metric oscillator/DQI | Explicit matrix-space code and target; rank shells, dual decoding, Fourier readout for low residual rank | Polynomial shell preparation/decoding would be needed; rank-metric decoding and elementary interpolation/completion are legal baselines | Compare the actual attainable rank with classical code geometry, not a proxy alone | Corpus already records2606.04843; its concrete construction is prior art and no different decoder was supplied |
| Growing-degree character reconstruction | Binary prime p, unknown monic squarefree degree-d Q, coherent padded BIT queries; output and statistically verify all coefficients | Desired poly(d,log p); charge every source, inverse, factorization, Fourier transform and flag. Existing full-table poly(p), exhaustive empirical decoding and chosen-Fourier-feature classical match remain | A nonsplit-factor or collective operation must obtain its phase from the ORIGINAL oracle. Split permutation erasure is already polynomial; support density is the bottleneck | No paid new operation found. Claude returned no report; general problem remains open |

Independent helper comparison also considered explicit binary self-dual-code
permutation equivalence and two-curve supersingular isogeny reconstruction.
Both have external motivation, but supplied no new paid decoder. Code-state
overlap is exactly classically computable by intersection dimension, which
does NOT simulate a coherent permutation-controlled algorithm. Endpoint
amplification gives a square-root improvement over the same path sampler,
not by itself polynomial time; coherent history erasure remains unprovided.
No broad hardness/no-go or status change follows from that bounded comparison.

The hidden-spired-graph source2605.11228 was also checked at Sections8 and
10-11: its instance uses an obfuscating oracle over exponentially large
graphs, with numerical quantum-efficiency and classical-hardness conjectures.
No native compiler/application was supplied, so it was not selected. This
does not adjudicate those conjectures. Metacyclic source2608.05321 was already
scoped in REES_WHOLE_PROOF_SCOPE_AUDIT.md; no new reduction arose here.

## Exact pairing theorem and complete classical counterpart

Let pi:F_2^m -> F_2^n and sigma:F_2^n -> F_2^m be arbitrary maps such that

    sigma(y) . z = y . pi(z)     for EVERY y,z.                 (1)

Define the public n-by-m matrix M by M[:,j]=pi(e_j). Set z=e_j in (1):
sigma(y)_j=y.pi(e_j), hence sigma(y)=M^T y for every y. Substituting back,
every y has y.pi(z)=y.Mz. Nondegeneracy of the dot product gives
pi(z)=Mz for every z. This proves both linearity statements without any
sampling or asymptotic assumption. Conversely, this matrix pair satisfies (1).

For the SQUARE PERMUTATION case n=m, M is invertible. The score encoded by
the source is |sigma(y)|=|M^T y|, up to its fixed affine position convention.
The classical maximum is m: solve M^T y=1 by Gaussian elimination. A
uniform sample at any prescribed score w is obtained by sampling a uniform
w-subset vector b and solving M^T y=b. The bijection makes this exactly
uniform on that score shell. If a PUBLIC classical circuit/evaluator for pi
is supplied, m basis evaluations recover M; neither inverse advice nor an
exponential truth table is needed. Complexity is polynomial in m and the
charged evaluator cost. This does not give classical access to an opaque
quantum-only unknown unitary. Basis queries recover M UNDER THE PROMISE;
they do not test whether an arbitrary supplied circuit satisfies (1).

A reversible nonlinear counterexample is Toffoli:

    pi(z0,z1,z2)=(z0,z1,z2+z0*z1).

It fixes all standard basis vectors, so (1) would force M=I and sigma=I.
For y=(0,0,1), z=(1,1,0), its two sides are 0 and 1. Thus arbitrary
reversible nonlinearity cannot retain this exact position identity. An
affine offset is excluded by z=0 in (1). Even if the identity is permitted
up to a y-dependent global phase, its binary exponent has the form
sigma(y).z=y.pi(z)+c(y). Substituting z=0 forces c(y)=y.b with b=pi(0);
the same proof then gives pi(z)=Mz+b and sigma(y)=M^T y. Recover b and M
with m+1 evaluations. The position-score optimization and shell sampling
are unchanged. Arbitrary modifications of the identity are not covered.

The RECTANGULAR noninjective case is explicitly outside the classical
optimization conclusion: maximizing |M^T y| remains Max-LINSAT. Actual
Section6.3/Claim44 returns to linear codes, and preparing its shell states
still needs the original decoder. Section6.4 suggests other oscillators;
it does not supply the missing nonlinear transform. We do not claim a flaw
in that paper, or a general classical simulation of DQI, coherent kernels,
nonlinear Hamiltonians, or quantum output states.

## Prior work and exact source scope

Corpus been-tried/baselines queries included:

- DQI harmonic oscillator interpolation adiabatic obfuscated oscillator;
- rank metric Gabidulin DQI Fourier shells bilinear forms association scheme;
- DQI list decoding coherent list interference beyond unique decoding radius;
- character polynomial reconstruction extension field nonsplit resultant.

Nearby corpus matches are leads, not novelty or impossibility verdicts.
Primary sources inspected:

- https://arxiv.org/html/2509.14443 (v2), Section6.3, Eq32 and Claim44:
  exact universal pairing premise and subsequent code/decoder construction;
  Section6.4: proposed physics generalizations, not an algorithm theorem.
- https://arxiv.org/html/2607.16541 (v2), Sections4-6/Theorem5.2:
  complete lists, fixed padding and exact success Z_I/(L Z_0).
  The native binary-table extension is already recorded locally, including
  its full primary-source decoder and normalization audit.
- https://arxiv.org/html/2606.04843, Sections1 and5 roadmap, plus prior local
  rank-metric admission record: the proposed rank mechanism is already known.
  No new general classical match is inferred from its abstract or proxy.
- https://arxiv.org/html/2605.11228, Sections8,10-11: paid spectral test and
  conjectural efficiency/hardness in the specified obfuscating-oracle model.
- Actual local Russell--Shparlinski0212016 Theorem6/proof and
  Kopparty2601.07137 Theorem1/Introduction under audits/sources/legendre_prf/:
  O(d)-query POVM existence is not an efficient circuit; the classical
  reconstruction algorithm has polynomial FIELD-SIZE cost. No new source
  theorem, degree/error scope or classical hardness is asserted.

## Claude and validation

One authorized Opus5.5/high constructive request asked for a new operation
removing the character factorial, with the actual Hankel and classical-
feature notes. Bundle: audits/claude_runs/2026-11-06-character-factorial-opus/.
Terminal status empty_response, stop_reason refusal, zero report bytes;
12913 input and612 output tokens, estimated charge $0.063892. It supplies
NO scientific findings, approval or counterexample. No retry/rephrase was
made. The estimate is not an invoice or remaining-credit measurement.

One exact Sage control, audits/controls/oscillator_pairing/exact_control.py,
recovered an invertible3-by-3 M from basis queries and solved the maximum
as y=(1,0,1), score3. All64 pairings matched. Toffoli was a permutation
but gave the explicit0-versus1 discrepancy. Its JSON retains the limited
scope. The general theorem above is proved algebraically, not inferred
from this finite control. No Hamiltonian or quantum circuit was executed.

Independent narrow pairing review and milestone disposition are recorded
in audits/reviews/2026-11-06-oscillator-pairing-triage.md.

## Next decision

No new subsystem, larger scan, benchmark or automatic neighboring extension
is justified by this pass. Reopen character reconstruction only with a
formula for a paid new operation and its original-oracle phase source;
the next experiment must test that formula against the retained exact native
control, before any circuit infrastructure. At a fresh pass boundary compare
independent externally valuable mechanisms again. No scientific candidate
is promoted because the selection or API request failed to find one.
