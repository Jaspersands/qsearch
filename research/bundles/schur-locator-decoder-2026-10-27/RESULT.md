# The Native AG Family Already Has A Matrix-Only Classical Decoder

## Decision

This removes the claim that the current AG family needs genuinely quantum
decoding. A sparse-error classical decoder can be built from the SAME public
generator B alone, without a curve, divisor, hidden partition or private
representation. Its coherent use gives the ordinary decoding-based quantum
sampling baseline for the original By=s/all-nonzero problem.

This is NOT a classical full-support search algorithm and NOT a dequantization
of the sampling task. It is a decisive prior-mechanism comparison: the special
signed-pair quantum decoder is unnecessary for this parameter family. The
construction is an elementary error-correcting-pair specialization, not a
claimed new coding theorem. The completed independent review in
../usd-novelty-review-2026-10-27/REVIEW.md checks the locator and the same-input
truncated-source DQI argument and supports this demotion. It does not
independently certify the parent implementation or establish a separation.

## 1. Matrix-Only Locator Lemma

Let V be the k-dimensional row space of the explicit matrix B over F_p and
W=span(V*V). Suppose proved distance bounds satisfy

    k>t, d(W)>t, and 2*d(V)>m.

Given r=c+e with c in V and wt(e)<=t, solve the LINEAR equations

    a in V, a*r in W

for any nonzero a. There is such an a: the at-most-t constraints a_i=0 at
error positions leave a nonzero vector because k>t. For ANY nonzero solution,
a*c is in W; thus a*e=a*r-a*c is in W and has weight at most t. The distance
condition forces a*e=0. Therefore r_i=c_i wherever a_i is nonzero.

The zero set of a has size at most m-d(V)<d(V). Two codewords cannot agree
off that set. Solve for the unique c in V matching r on support(a), then
verify that its distance from r is at most t. The output is the message in
the ORIGINAL row basis, not only a codeword in a changed basis.

Implementation computes W and W-perp using exact modular elimination. The
locator equations are W-perp * diag(r) * B-transpose times the unknown message
of a. All information comes from B. Source geometry is needed for a theorem
about the distance promises, not as an uncharged runtime oracle.

This is the error-correcting pair (V,W-perp) for the target V: V*(W-perp)
is contained in V-perp, dim(V)>t, d((W-perp)-perp)>t, and d(V)+d(V)>m.
The established framework is described in
[Couvreur-Marquez-Corbella-Pellikaan, Section4.1](https://arxiv.org/html/1401.6025v3#S4.SS1).
We do not rely on blindly transferring their separate McEliece attack's
degree interval or dual-code orientation to this family.

Computing W takes polynomial field operations, e.g. O(k^2*w*m) by streaming
products and reducing against a basis. Each decode uses linear systems of
dimension at most m, hence O(m^3) field operations by naive elimination.
The executable backend currently supports primes below2^63 via python-flint.
The mathematical procedure uses ordinary finite-field arithmetic and can be
compiled reversibly with polynomial history space. A reversible netlist is
not implemented here.

Outside the distance/error promises the executable may return FAILURE. Any
returned word is still a checked codeword within the requested radius; it
does not claim unique recovery without the distance promise. Failure is
never infeasibility or evidence of classical hardness.

## 2. Application To The Actual Parameter Family

For the complete native AG code, p=1019 and

    g=5e+1, deg(G)=10e+3, k=5e+3, m=22e.

Standard evaluation-code distance bounds give

    d(V)>=m-deg(G)=12e-3,
    d(W)>=m-2deg(G)=2e-6.

The second follows already from W contained in the evaluation of L(2G);
surjectivity onto that space is not needed for this lower bound. Hence

    t=2e-7

is a valid decoding radius for every e>=8. This applies to both special11I-E
and generic prime-divisor inputs meeting the same complete AG promises.
Neither a full Schur cube nor disappearance of short kernel words blocks it.
Column permutations, nonzero column scalings and invertible row changes
preserve the argument; controls exercise these without exposing the changes
to the decoder.

On the actual43-by-176 matrix, the bounds are d(V)>=93, d(W)>=10 and t=9.
The new decoder correctly recovers deterministic test codewords with0,1,8,9
errors on the original matrix and a transformed matrix. These are checks of
the algorithm; the all-error-pattern guarantee follows from Section1, not
finite experiments. No higher-e input was generated.

## 3. Ordinary DQI Comparator, Including The Output Law

For full support, the inverse-Fourier single-symbol source has amplitudes
sqrt((p-1)/p) at zero and -1/sqrt(p*(p-1)) at each nonzero symbol. Its error
weight is Binomial(m,1/p). Let f_t be this product amplitude vector truncated
to weight<=t and normalized, and let tau be the retained squared norm.

The truncated state is efficiently preparable without an alphabet-sized
table. Compute conditional binomial tails by polynomial-size dynamic
programming, prepare successive error indicators conditioned on the running
weight, prepare uniform nonzero symbols where required, and attach the sign
(-1)^weight. Clear the indicator/count work using the data before translation.
All probabilities have polynomial bit descriptions; rotations need charged
precision. This is a constructive resource argument, not an emitted circuit.

The native distance exceeds2t. Translates X^c f_t for different c in V have
disjoint support, so the classical decoder erases the retained c EXACTLY on
the ideal truncated source. The usual character-weighted superposition and
final Fourier transform are therefore available at polynomial bit cost.

For every full-support y, the Fourier amplitude of f_t is the SAME value
sqrt(tau)/(p-1)^(m/2). To see this, each sum of nontrivial additive characters
over a nonzero symbol is -1; that cancels the source's minus sign, leaving
the binomial tail normalization. The retained character then restricts
support to the original B y=s fiber. Consequently

    raw verified success = lambda_s * tau,
    ideal verified output = EXACT uniform distribution on that fiber.

This is stronger than an inference from a generic worst-case decoder-error
bound: it uses an exactly truncated source and its explicit amplitudes.
The ideal conditional uniform law does not imply that a finite-precision or
noisy physical implementation is exactly uniform. Whole raw-channel errors
and their conditioning factor must still be charged.

The elementary union bound gives

    1-tau <= binom(m,t+1)/p^(t+1).

Combined with the existing full-support normalization bound
alpha=(p^k-1)/(p-1)^(m-deg(G)), this yields success at least
(1-alpha)*(1-tail). At e8, tail<=5.017959261267054e-15 and
alpha<=4.2751027594776105e-151. The fixed-p large-e tail decreases
exponentially: binom(m,t+1)<=[exp(1)*m/(t+1)]^(t+1), and m/(t+1)->11
while p=1019. Higher rows are analytic, not generated matrices.

This is an instantiation of the existing decoding-to-constrained-sampling
framework, not evidence that the project has invented a new quantum
algorithm. In particular, a classical sparse-error decoder used coherently
does NOT make the whole quantum sampler a classical algorithm.

## 4. Consequences And Remaining Question

Deprioritize the native family as evidence that quantum-only decoding crosses
a classical decoding barrier. The claimed need for that ingredient is false
even in the strict B-only model. Retain the signed-pair circuit as a scoped
reusable construction, not as the reason to expand the AG source backend.

The original classical full-support search and uniform-sampling questions
remain separate. Fiber repair solves the special finite search control; affine
rejection samples the uniform fiber with its actual rejection cost. The new
decoder by itself solves neither task classically. No claim that every AG
code or every possible Schur decoder regime is covered follows.

Further work needs either a useful consequence of this already classically
decodable quantum framework, a new matched classical full-support sampler,
or a different explicit family where the proposed quantum receiver handles
noise beyond ALL available classical decoding radii. Do not manufacture that
gap merely by suppressing public structure or labeling an absent decoder hard.
