# Raw Word Spectral Filters: Ensemble Degree Price

Local derivation, external mathematical review pending. This is NOT a
lower bound on general quantum algorithms, lattice decoding, adaptive
measurements, different encodings or structured preconditioners.

## The Actual Operator And Measurement Model

On the native M-qutrit word domain, D=3^M and N=q^n. The public word map is
f_A(w). Define J|w>=|f_A(w)>/sqrt(D), K=J^*J. If frequency sigma has
m_sigma words, its uniform fibre vector r_sigma has K eigenvalue
p_sigma=m_sigma/D; the fibre-orthogonal kernel has eigenvalue0.

An exact native preparation has amplitudes exp(i*theta_w)/sqrt(D) from
ORIGINAL classical values. For arbitrary phases, including arbitrarily
correlated errors, c_sigma=|<r_sigma,psi>|^2 <= p_sigma. The ideal noiseless
codeword saturates this inequality, but saturation is NOT needed below.

Consider a LABEL-ONLY measurement effect E_A=P_A(K), where P is a real
degree-d polynomial globally bounded in [0,1] on ALL of [0,1]. Its
coefficients may depend on public labels, but not original response values.
This grants more than a compiled physical QSVT circuit: global positivity
alone does not establish QSVT realizability, precision or block access.

For an IID uniform original-value null, the mean UNMASKED word density is
I/D because distinct native selector words give distinct raw characters.
A value-adaptive known mask contributes a phase constant on each fibre,
commutes with K, and leaves this effect's acceptance invariant. We therefore
do NOT require that the adaptively masked density itself remain I/D.
General response-dependent polynomial selection does not enjoy this argument.

## Degree Bound Without Balance Or A Zero Kernel Response

Set p0=P(0), Q(x)=P(x)-p0 and C_A=sum_sigma p_sigma^2. Then

    source_acceptance = p0 + sum_sigma c_sigma Q(p_sigma),
    IID_null_acceptance = p0 + (1/D)*sum_sigma Q(p_sigma).

The classical Markov derivative inequality applied to
R(t)=2*P((t+1)/2)-1 gives |P'(x)|<=d^2 on [0,1]. Consequently

    |source_acceptance - IID_null_acceptance|
      <= d^2 * sum_sigma |c_sigma-1/D| p_sigma
      <= d^2 * (C_A + 1/D).

This includes a nonzero P(0), missing fibres, unbalanced counts and arbitrary
source phase noise. For IID full-root original labels, each two distinct
native selector words differ in at least one ORIGINAL coefficient that is
a unit modulo3^r. Their frequency collision probability is exactly1/N, so

    E_A C_A = 1/N + (1-1/N)/D,
    ensemble gap <= d^2*(1/N+2/D).

For M=nr+s, the required constant advantage thus costs acceptance degree
at least sqrt(gamma*N/(1+2/3^s)). Two-ensemble operator and preparation
errors are charged as 2*epsilon+2*delta before deriving this degree bound.
An error budget that swallows gamma yields a VACUOUS degree bound0, not an
efficient algorithm. The result is ensemble-level, NOT a typical-bank
guarantee or an inference from selected successful fixtures.

For a parity-respecting degree-t singular-value amplitude polynomial on J,
its squared acceptance is a degree-at-most-t polynomial in K's eigenvalue.
This explains the scale obstruction for that PARTICULAR filter architecture.
Do not relabel the acceptance-degree statement as an unconditional query
lower bound against arbitrary circuits that inspect the public matrix.
Generic unknown-matrix black-box bounds have different premises.

Background: [Gilyen, Su, Low and Wiebe](https://arxiv.org/abs/1806.01838)
introduce QSVT and analyze its limitations; [Tang and Tian](https://arxiv.org/abs/2302.14324)
explain why bounded polynomial approximation is an essential constraint.
The collision-weighted native-source bound above is a LOCAL derivation, not
a theorem attributed to either paper, and no novelty claim is made.

## Constructive Controls And Matched Classical Statistic

Four existing ORIGINAL-data controls are regenerated, not replaced by a
new oracle problem. Native frequency/phase rows and fibre counts are computed
exactly. Geometric, Chebyshev-endpoint, constant and nonzero-kernel-bias
filters give exact cyclotomic source probabilities and rational null traces.
Diagnostic cosine values are not used as proof certificates.

For k>=1, draw k+1 independent uniform words. The bounded random variable

    1[ALL frequencies equal] * exp(i*(theta_last-theta_first))

has expectation <psi,K^k psi>. Real parts supply a same-source classical
scalar estimator for a polynomial's moments. Coefficient l1 norms, word
evaluations and inverse precision must be paid. Chebyshev coefficients can
grow rapidly; this identity is NOT a claim of efficient universal dequantization.
It is a baseline to run before promoting finite low-degree filter signals.

Three countercontrols police scope:
- Concentrated zero labels have C_A=1 and a large degree1 gap. The small
  ensemble collision bound is not a statement about EVERY public matrix.
- P(x)=81*x fits the balanced spectrum {0,1/81} but exceeds1 elsewhere.
  It is not a globally bounded filter or an implemented normalized encoding.
- A degree0 response-dependent classical effect can distinguish a zero-secret
  noiseless calibration from an IID null. Label-only null trace reasoning
  cannot be extended to arbitrary response-dependent coefficient selection.

## Decision And Next High-Upside Target

Do not spend a search campaign fitting polynomials to the raw K spectrum
and calling normalization free. To escape THIS scope, construct and pay for
a different operator/preconditioner with a useful overlap and spectral scale,
or a noncommuting collective observable with its own source/null analysis.
Masking, constant condition number and extra word surplus alone do not do it.

    python theorems/native_word_spectral_filter_audit.py --write
    node research/certificates/native_word_spectral_filter_audit_crosscheck.js
    python -m pytest -q tests/test_native_word_spectral_filter_audit.py
