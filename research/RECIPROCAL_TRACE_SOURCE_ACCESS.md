# Reciprocal Trace: The Fourier Source Is Classically Accessible

2026-10-22. Known elliptic-curve mechanism, explicit source-access audit.
No new point-counting algorithm, full dequantization, or quantum speedup.

## Research Decision

Do not attribute difficulty to evaluating or sampling the Fourier source
in BALANCED_CODEWORD_FILTER.md. Both have polynomial-time classical
algorithms by known binary elliptic-curve point counting. This is stronger
than an exponentially enumerated Walsh table. The remaining candidate
advantage is the COHERENT composition of code addition, decoder erasure
and inverse Fourier readout, not the source's classical probability law.

The repository supplies a counted, capped rejection-sampling reduction and
small independent point-count controls. A scalable characteristic-two
point-counting backend is not implemented here. Importing that known
backend is an implementation dependency, not an open complexity conjecture.

## 1. Exact Signed Coefficients From Curve Orders

Let f(x)=Tr(inv0(x)), q=2^n, and define

    W(u)=sum_x (-1)^Tr(inv0(x)+u*x).

W(0)=0 because inversion is a permutation and trace is balanced. For u!=0,
consider the nonsingular ordinary elliptic curve

    E_u: v^2+z*v=z^3+u.

The known identity is

    W(u) = #E_u(F_q)-q.

See [Ahmadi-Granger, Lemma2.1 and introductory point-counting discussion](https://arxiv.org/pdf/1104.3882).
The correspondence and polynomial-time coefficient access are prior art.
Their separate task of FINDING a Kloosterman zero is not needed here;
evaluating a supplied coefficient is not the same search problem.

Direct derivation to fix conventions: the point at infinity and the unique
point with z=0 contribute two. For z!=0, set t=v/z. Then
t^2+t=z+u/z^2, so the number of t is 1+(-1)^Tr(z+u/z^2).
Since Tr(u/z^2)=Tr(sqrt(u)/z), the total is

    q+1+sum_(z!=0) (-1)^Tr(z+sqrt(u)/z).

The nonzero Kloosterman sum is invariant under Frobenius in its parameter.
It therefore equals W(u)-1, giving q+W(u). The zero-extended convention
matters: replacing #E-q by #E-q-1 loses the source's actual coefficients.
The singular u=0 curve is NOT passed to a point-counting backend.

For the normalized uniform root state of target b, the additive Fourier
amplitudes are

    a_b(0)=1/sqrt(2),
    a_b(u)=(-1)^b*W(u)/(sqrt(2)*q),  u!=0.

Thus signs as well as probabilities are classically evaluable. Exact
integer numerators require only polynomially many bits. Approximating the
common square-root normalization to any specified precision is separate
elementary arithmetic.

Point counting in characteristic two is an established algorithmic
capability. See also [Schoof's account](https://jtnb.centre-mersenne.org/item/JTNB_1995__7_1_219_0.pdf)
and the [characteristic-two implementation description](https://magma.maths.usyd.edu.au/magma/handbook/text/1557).
Do not substitute short-Weierstrass formulas requiring odd characteristic,
or claim a floating/heuristic curve-order estimate is an exact backend.
The field polynomial/basis is the same public input used by the native task.

## 2. Exact Classical Sampling With A Paid Clock

Parseval and W(0)=0 give sum_u W(u)^2=q^2. Hasse gives
|W(u)|<=1+2*sqrt(q), hence W(u)^2<=8q for q>=4. Conditional on a nonzero
Fourier symbol, the distribution is

    p_nonzero(u)=W(u)^2/q^2.

One rejection trial draws u uniformly from F_q and an independent integer
r uniformly from {0,...,8q-1}. Accept exactly when r<W(u)^2. This uses
n and n+3 random bits, respectively; no floating acceptance test or
enumeration of all frequencies occurs. The unconditional probability of
accepting u in one trial is W(u)^2/(8q^2), so:

- One-trial acceptance is EXACTLY1/8.
- An accepted sample has exactly p_nonzero, including after a fixed cap.
- Unbounded expected trial count is8; a B-trial cap aborts with probability
  (7/8)^B. At most B point counts are charged (u=0 needs none).

To sample the full source law, flip a fair coin: half the time output0,
otherwise use the nonzero sampler. Without a cap this is an exact
expected-polynomial-time sampler. With a cap, keep ABORT as an outcome.
Its probability is (1/2)*(7/8)^B. The non-aborted full mixture is NOT exactly
the original distribution after renormalization: zero has been favored by
the nonzero-branch abort. At the product-source level, use a union bound
over coordinates, or the exact independent abort probability. Never drop
those failures and label the normalized data exact source samples.

The sampler is exact conditional on a CORRECT point counter and independent
uniform random bits. The deterministic pseudorandom seeds in unit tests
are reproducibility controls, not proofs of randomness. Hasse and order
divisibility checks reject some malformed counters but cannot certify every
plausible incorrect order. The backend's correctness remains its contract.

## 3. Why This Does Not Yet Dequantize The Algorithm

Classical samples are not the signed superposition. Sampling a Fourier
error and a public codeword produces the diagonal law before coherent
erasure; it does not sum amplitudes before squaring after inverse QFT.
Even efficient amplitude queries plus squared-amplitude samples do not by
themselves supply a general efficient Fourier-output sampler.

In particular, the final target constraints b affect signs away from zero,
but not the local Fourier probabilities. A procedure using only these
probabilities discards information used by the coherent readout. It cannot
be advertised as a simulation without reconstructing the final law and
verifying BOTH native parity and inverse-trace constraints.

This observation neither proves such a simulation impossible nor closes
the classical-hardness question. It identifies a stronger baseline and
narrows the quantum resource claim to the unresolved coherent composition.
The previous affine-flat native witnesses are still valid counterevidence
against finite-size advantage claims.

## Controls And Next Work

The reference directly counts all affine pairs on E_u and the point at
infinity for n=2,3,4,5:56 nonsingular curves altogether. Tests compare the
result with direct inverse-trace Fourier sums, including negative values,
zero coefficients, both target signs, exact rejection mass and clock aborts.
This reference is EXPONENTIAL in n and is guarded at n<=5. The report says
explicitly that no scalable point-counting backend has run.

No new registry or UI feature is justified. If a concrete classical
coherent-readout attack needs this sampler, mechanical follow-up can attach
a trusted characteristic-two counter while preserving the exact input
field and all abort/sign accounting. Do not implement a new point-counting
algorithm just to reproduce known theory. The substantive next question is
whether source sample/query access plus the public RS decoder actually
permits native witness sampling; no such reduction is established here.

Replay: `python -m theorems.reciprocal_trace_source_access --write`.
Artifact: `research/classical_baselines/reciprocal_trace_source_access.json`.
