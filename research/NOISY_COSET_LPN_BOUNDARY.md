# Noisy Coset Copies: An Exact Learning Boundary

2026-10-22. Access-model reduction and protocol-specific cost analysis.
Not a new LPN algorithm, hardness proof, universal purification lower bound,
or refutation of the noiseless Rees theorem. The binary noisy-Simon/LPN
connection is established prior art. This note makes the copy-only interface
and the tempting purification shortcut explicit for this repository.

## 1. Why This Matters

The proposed Rees receiver takes fresh IID **clean mixed coset states**.
REES_NOISY_STATE_SOURCE.md instead purifies a state with a NONDEGENERATE
principal eigenvector before constructing coset states. Those contracts
cannot be interchanged. A contaminated coset state's principal eigenspace
usually has exponentially large multiplicity.

The substantive target for a claimed generic noise-tolerant receiver is
already present in the abelian special case: decoding noisy linear samples.
Do not launch more nonabelian noisy fixtures until a mechanism addresses
this case without supplying the unknown secret, error flags, clean samples,
a coherent example oracle, or an inverse unknown-state preparation.

[May, Schlieper and Schwinger, Section 5](https://arxiv.org/pdf/1910.00802)
establish polynomial equivalence of their binary noisy-Simon distribution
and LPN. Our direct construction below uses one extra coordinate and a
promised nonzero pivot. It also states the density-operator interface, so
the conclusion applies before any measurement, not just to one chosen
classical postprocessor. No novelty is claimed for the binary connection.

## 2. Exact Reduction, Including the Noise Law

Fix a prime p, a secret s in F_p^m, and visibility 0<v<=1. An ordinary
classical sample consists of

    a uniform in F_p^m,
    e distributed as v*delta_0 + (1-v)*Uniform(F_p), independently,
    b = <a,s> + e.

The algorithm sees (a,b), NOT s or e. Put G=F_p^(m+1), N=p^(m+1),
u=(s,-1), and H=span(u). Thus |H|=p. With the usual right-regular action,

    rho_H = (1/N) sum_(h in H) R_h,
    sigma_H,v = v*rho_H + (1-v)*I/N.

The public Fourier transform diagonalizes every rho_H in the SAME basis:

    F rho_H F^dagger = (p/N) sum_(y in H^perp) |y><y|,
    P_v(y) = v*p^(-m)*1_(y in H^perp) + (1-v)*p^(-(m+1)).

For y=(a,b), y.u=<a,s>-b=-e. The specified error law is invariant under
negation. Consequently P_v is EXACTLY the ordinary noisy sample law.

**Sample to copy.** Given just the observed y=(a,b), prepare F^dagger|y>.
Forget the sample in the receiver's interface. Averaging over samples gives
sigma_H,v exactly. This takes one sample per copy and public product Fourier
operations; it does not coherently query the sampling process. The preparer
may hold y as a classical record, but the simulated receiver gets only the
promised state. Fresh samples give the promised product state even when the
receiver requests them adaptively.

**Copy to sample.** Apply F and measure. This recovers exactly (a,b)'s law.
These channels work for every s and use no secret-dependent operation.
For p=2 they are exact Hadamard circuits. General prime-modulus Fourier
circuits have charged polynomial approximation cost; allocate error across
the entire requested sample stream, not normalized rare outcomes.

**Answer conversion.** Any nonzero recovered generator w of H has w_last!=0.
Return s_j=-w_j/w_last. The pivot promise loses no instance of the specified
noisy-learning problem. We do not silently assume the correct scale of w.

For p=2 the bit-flip probability is tau=(1-v)/2, giving standard search
LPN for every 0<tau<1/2. For odd p it is a SPECIFIED q-ary contamination law:

    Pr[e=0] = v+(1-v)/p,
    Pr[e=t] = (1-v)/p for every nonzero t,
    Pr[e!=0] = (1-v)*(1-1/p).

This is NOT Gaussian LWE, a worst-case lattice reduction, or a transfer of
binary LPN hardness to arbitrary growing primes. The exact-Lie Rees core
uses odd p; a robust odd-prime extension would solve this q-ary problem.
A robust all-prime extension, including its abelian branch, would solve LPN.

## 3. What Commutativity Does and Does Not Prove

All these states commute. For T copies, every measurement's output law is
a classical stochastic function of the T Fourier labels: its kernel is the
diagonal matrix element of the POVM in the known product Fourier basis.
Equivalently, sample the labels, prepare their public Fourier basis states,
and run the original quantum receiver. Thus the state inputs offer no extra
information over the classical samples, even for joint adaptive processing.

This is NOT efficient classical simulation of arbitrary quantum processing.
Computing that stochastic kernel classically may itself be difficult. A
polynomial quantum decoder for classical LPN samples would be an important
result and would also solve these noisy coset instances. None is provided
here, and no unconditional quantum runtime lower bound is asserted.

[Cross, Smith and Smolin](https://arxiv.org/pdf/1407.5088) study noisy
COHERENT quantum examples, a different input. The finite countercontrol
here mixes the coherent states sum_a |a,<a,s>+e>/sqrt(2^m) over a common
label error e. Their computational diagonals equal the classical sample
distribution, but Fourier readout conditioned on the last bit being one
reveals s. Dephasing first destroys that property. This control uses a
global label-flip model, not a simulation of their local-noise theorem.
Equal classical marginals are not an access-preserving quantum reduction.

## 4. Why Recursive Symmetric Purification Does Not Repair This Cheaply

Let r=N/|H|=p^m. Write e0=(1-v)*(1-1/p). The eigenvalues of sigma are

    a=(1-e0)/r, multiplicity r,
    b=e0/(N-r), multiplicity N-r.

Its trace distance from rho_H is exactly e0. This top space is degenerate
for m>=1, so the nondegenerate principal-state promise in the known
[streaming purification analysis](https://arxiv.org/abs/2503.22644) is absent.
Even if the goal is the flat projector rho_H rather than a pure vector,
the symmetric two-copy recursion has a severe rank dependence.

For two independent inputs, keep one subsystem after the symmetric outcome:

    probability = (1+Tr(rho^2))/2,
    rho_next = (rho+rho^2)/(1+Tr(rho^2)).

The two-flat-block form and the top multiplicity r are preserved. At every
level a<=1/r. If O=e/(1-e) denotes outside-to-inside probability odds,

    O_next/O = (1+b)/(1+a) >= 1/(1+1/r).

Therefore achieving target delta<e0 requires

    K >= log((e0/(1-e0))/(delta/(1-delta))) / log(1+1/r).

For a completely rational certificate, put R=(e0/(1-e0))/(delta/(1-delta)):

    K >= ceil(r*(1-1/R)).

This uses log(1+1/r)<=1/r and log R>=1-1/R. It is a necessary lower bound,
NOT a sufficient schedule. A balanced K-level recursive protocol consumes
at least 2^K fresh raw copies even if EVERY herald succeeds; rejects only
increase cost. For any fixed nontrivial improvement, K=Omega(r), so the
minimum raw-copy count of THIS protocol is 2^Omega(p^m). This is stronger
than just observing that its pure-state theorem has an unmet hypothesis.
It does not exclude unequal-depth protocols, collective decoders, or other
noise-handling algorithms.

At p=2, v=3/4, e0=1/8 and delta=1/16, the bound is ceil(8r/15). For m=64
this exceeds 9.8e18 levels. The report records log2(copy count), not an
impossible allocation or a floating-point extrapolation.

## 5. Charging the Apparently Fast Power Filter

Normalized virtual squaring, rho^2/Tr(rho^2), improves error much faster.
It is not the preceding physical SWAP output. Here a concrete way to
realize the power filter is available because the eigenbasis is public:
measure k IID Fourier labels, accept only when all k are equal, and prepare
the retained label's Fourier state. Its exact success probability is

    P_k = r*a^k + (N-r)*b^k = Tr(rho^k),
    e_out = (N-r)*b^k/P_k,
    expected raw copies = k/P_k.

For the binary v=3/4 case and k=2, e_out=1/50, but P_2=25/(32r) and
expected raw copies=64r/25. This is exponential in m. It is a separate,
much cheaper protocol than the balanced SWAP tree, yet still not a
polynomial repair. A generic density-matrix power calculation that omits
normalization/access cost is not a decoder. This bound does not exclude
more sophisticated learning from the same samples.

## 6. Falsifiers, Evidence, and Decision

- Disprove the reduction by exhibiting a density entry or Fourier label
  probability that differs from the classical sample preparation. Controls
  construct regular translations independently of the proposed Fourier law.
- Disprove the resource bound by finding a level of the specified IID
  balanced symmetric recursion violating the odds inequality, or a legal
  output with a lineage containing fewer than 2^K raw inputs. A different
  protocol does not refute this scoped bound.
- A receiver supplied with an error flag, coherent noisy-example oracle,
  retained preparation environment, or fresh clean source is out of scope.
- The noise model is IID global depolarization of each already-mixed coset
  state. Local hardware noise, faults during clean-source generation, and
  adversarially correlated noise are different contracts.
- Noisy-sample quantum computation remains a constructive avenue. Any
  candidate must give a real decoder on the binary pivot family before
  claiming a generic robust extension. Passing finite maximum-likelihood
  recovery, enumerating secrets, or renaming a Gaussian-noise solver fails.

Keep the clean Rees theorem and its principal-state source construction
separate and unchanged. Do not prioritize generic coset denoising as
mechanical follow-up: it has a substantial learning problem inside it.
No new registry candidate or negative-result admission is made.

The clean theorem's allowance for small complete-channel implementation
error is also unchanged. It budgets error inversely in the whole circuit's
instrument count; it is not a promise of constant corruption in every raw
input. Fault-tolerant execution of a clean preparation is different from
being handed already contaminated copies with no preparation access.

The infinite nilpotent-group extension was also screened this pass, but not
pursued: finite-index period reductions would add another oracle corollary,
whereas deficient-rank inputs have no automatic finite-quotient source.
[Kuperberg's infinite-group HSP paper](https://arxiv.org/html/2507.18499v1)
already handles arbitrary-rank abelian inputs and explicitly distinguishes
binary-coordinate query cost from pseudopolynomial cost. No nonabelian
extension or lattice application was established here.

Replay: `python -m theorems.noisy_coset_lpn_boundary --write`.
Tests: `python -m pytest tests/test_noisy_coset_lpn_boundary.py -q`.
