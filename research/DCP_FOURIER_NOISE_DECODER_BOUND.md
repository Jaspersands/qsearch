# A Strong Converse For The Measured Fourier-Noise Shortcut

LOCAL DERIVATION / REVIEW PENDING. This is an information obstruction for a
specific classical-observation source, not a general quantum algorithm no-go.
No novelty or independent review is claimed.

## Exact Source

Normalize f=c0*delta0+c1*delta1 modulo q>=3. Its unitary Fourier distribution is

    P(e)=|c0+c1*exp(-2*pi*i*e/q)|^2/q.

First suppose a proposed quantum-to-classical bridge asks a decoder to recover a
uniform secret s in Z_q^n from b=A^T*s+e modulo q, where the coordinate errors
are independent with these distributions. A is public, independent of s;
it may be ANY fixed matrix, not only random. The decoder sees classical (A,b),
not the noise purification or residual quantum source.

Fourier orthogonality for q>=3 gives

    kappa=q*sum_e P(e)^2=1+2*|c0*c1|^2 <= 3/2.

An order-two two-point gap is an exception to this orthogonality calculation;
the native Boolean witness envelope has unit gap and is not that source.
Complex, unbalanced or coordinate-dependent normalized coefficients do not
evade the bound. Uniform noise gives kappa=1; balanced noise attains3/2.

## Decoder-Independent Proof

More generally let independent noise distributions P_i have collision
multipliers kappa_i=q*sum_e P_i(e)^2. Let G=q^n. An optimal decoder of the
classical input can be deterministic: each observation chooses a likelihood
maximizer. Randomization or quantum computation on that classical input
cannot improve its optimal average success.

Partition observations into disjoint decoder regions D_s. With
Q_s(b)=product_i P_i(b_i-(A^T*s)_i), Cauchy--Schwarz gives

    P(correct) = (1/G) sum_s sum_(b in D_s) Q_s(b)
      <= (1/G) sqrt( [sum_s |D_s|] [sum_s sum_(b in D_s) Q_s(b)^2] )
      <= (1/G) sqrt( q^m * G * product_i sum_e P_i(e)^2 )
       = sqrt(product_i kappa_i / G).

Heralded rejection is just an incomplete partition and only decreases the
unconditional success. No runtime assumption, chosen decoder, Gaussian
heuristic or random-matrix property appears in the proof.

For the product Boolean-envelope Fourier source,

    P(correct) <= min(1,sqrt((3/2)^m / q^n)).

At q=2^L and m=nL+Delta, Delta=O(log(nL)), this is exponentially small in nL.
Using the EXACT inequality (3/2)^5<2^3 gives the conservative dyadic bound

    P(correct) <= 2^-max(0,floor((5*n*L-3*m)/10)).

At L=4n+1, Delta=16, n=8,16,32 the exponents are48,203,820. More decoding
time cannot fix an information-deficient classical observation source.
The same bound on the mean uniform-secret success prevents a pointwise
high-success guarantee for every fixed secret. It does not say every
individual fixed secret is hard for a specially chosen constant-output decoder.

For this bound to become vacuous needs m>=nL/log2(3/2). That is only a necessary
threshold for avoiding THIS bound, not sufficient for any efficient decoder.
Shannon's stricter asymptotic capacity constraints may require more samples.
The module records finite entropy estimates, not a second unproved theorem.

## What This Does And Does Not Kill

Killed: treating the broad measured Fourier errors as binary, or proposing
an unlimited-time classical decoder of that product-noise source at native
near-entropy width. The new binary-error Hensel decoder receives a DIFFERENT
input distribution and cannot be substituted without a reduction.

Not killed: collective quantum use of the m physical phase registers; a
correlated-noise conversion; coherent processing of purification; another
phase envelope; additional legitimately charged samples; a different density
and readout architecture; or explicit-input Boolean subset-sum solvers.

In particular this is NOT a classical hardness lower bound for the public
arithmetic task A*x=t, and it does NOT classically simulate DCP. The latent
uniform secret/noise source is essential. General quantum arithmetic solvers
remain legitimate potential inputs to the preferred direct witness filter.

The ternary literature operates at a different alphabet/density. Its binary
Fourier noise and quadratic sample regime are compatible with these bounds;
this audit does not refute it.

## Self-Critique: Entangled Envelopes Also Fail

The initial recommendation to simply correlate the Boolean envelope's
amplitudes was too weak. The same collision converse holds for ANY normalized
complex envelope f supported on the physical Boolean cube, including entangled
amplitudes depending arbitrarily on public A. Coordinate-noise independence
is unnecessary for this extension.

Let p(w)=sum_(x in {0,1}^m) f_x product_j w_j^x_j, with w uniform over q-th
roots of unity in every coordinate, q>=3. Parseval and fourth-moment
orthogonality give

    q^m sum_e |DFT(f)(e)|^4 = E_w |p(w)|^4.

Induct on the number of variables. Write p=a+w_m*b, and let X,Y be the squared
coefficient norms of a,b. Averaging the last variable eliminates nonzero
frequencies of degree at most two, giving

    E |a+w_m*b|^4 = E(|a|^4+|b|^4+4*|a|^2*|b|^2).

Induction bounds the first terms by C*(X^2+Y^2), where C=(3/2)^(m-1).
Cauchy bounds the mixed moment by C*X*Y. Finally

    X^2+Y^2+4*X*Y <= (3/2)*(X+Y)^2,

whose nonnegative gap is (X-Y)^2/2. Since X+Y=1,

    q^m sum_e |DFT(f)(e)|^4 <= (3/2)^m.

Balanced product amplitudes attain the bound. Entanglement cannot improve
this fourth moment. This is an elementary multiaffine Fourier norm inequality,
not a novelty claim. The discrete alphabet q=2 is exceptional, as is an
order-two gap inside a larger even modulus; neither is the source being bounded.

Repeat the decoder-region Cauchy proof with the full correlated noise law
Q(e)=|DFT(f)(e)|^2: replace the product of collision probabilities by sum_e Q(e)^2.
It gives exactly the SAME sqrt((3/2)^m/G) bound, pointwise for every fixed A
and every normalized secret-independent f_A. Mixtures of these envelopes also
obey the bound by convexity of squared norm. Normalizing a heralded envelope
does not evade it; its branch success must additionally be charged.

Thus correlating amplitudes before the FULL coordinate Fourier measurement
is not the needed breakthrough. Earlier scope statements about unrestricted
correlated-noise conversions remain valid ONLY when those conversions are
outside this full-coordinate Boolean-envelope Fourier model.

## Native Subgroup Covariance Is The Remaining Escape

The Fourier-noise construction imposes covariance for independent translations
in Z_q^m. Native input phases are related by v=A^T*s: only the subgroup
A^T*Z_q^n must be respected. A public-A-adaptive collective measurement can
exploit these relations and need not have the noise law above.

Actual scope countercontrol: n=1, q=2^L, m=L and labels (1,2,...,2^(L-1)).
The physical Boolean sum is a bijection x->sum_j 2^j*x_j. Coherently relabeling
the input word by that sum yields an EXACT full-q Fourier state; inverse QFT
recovers every secret with probability1. The full-coordinate measured-noise
shortcut, on the SAME matrix, has bound (3/4)^(L/2)<1. There is no contradiction:
these are different measurements, not two decoders of the same classical input.

The module executes the coherent countercontrol at L=2,3,4. This is not a
native scalable candidate: the literal ordered label pattern occurs with
probability2^(-L^2) in the IID source, and no selector/sieve is provided.
It is a source/measurement-scope calibration, not a toy oracle search.
Other adaptive patterns and collective algorithms are not ruled out by that
literal-pattern probability.

REVISED NEXT TASK: an ACTUAL A-adaptive subgroup-covariant collective primitive,
or a noise conversion provably outside the full-coordinate Fourier model.
Derive its physical circuit and source law before invoking a classical decoder.
Do not spend the next pass merely choosing more entangled cube amplitudes.

## Falsifiers And Checks

- Recompute all Fourier collision multipliers for complex envelopes.
- Exhaustively optimize the classical decoder on small fixed full-rank AND
  rank-deficient matrices; compare average success with the collision bound.
- Check the claimed error coordinates really are independent and that s is
  uniform independent of A. Conditioning, purification or label-dependent
  distributions can invalidate applicability, not the algebraic bound.
- Never drop the success probability of a noise-shaping filter.
- Seek independent review; bounded computation is not theorem verification.

Artifacts: `theorems/dcp_fourier_noise_decoder_bound.py`, its matching tests,
`research/reductions/dcp_fourier_noise_decoder_bound.json`, and the independent
`research/certificates/binary_error_source_crosscheck.js`.

    python theorems/dcp_fourier_noise_decoder_bound.py --save
    PYTHONPATH=theorems python -m pytest -q tests/test_dcp_fourier_noise_decoder_bound.py

The live report contains15 one-coordinate envelopes,15 entangled block controls,
6 exact bounded-source optimal decoder enumerations,3 coherent subgroup
countercontrols and3 symbolic growing-modulus ledgers. These small
controls calibrate the theorem, not research candidates or toy oracle problems.
