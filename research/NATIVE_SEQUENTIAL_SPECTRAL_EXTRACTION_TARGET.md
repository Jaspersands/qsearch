# Next Positive Target: Sequential Spectral Moment Extraction

IMPLEMENTED CONDITIONAL EXTRACTOR / LOCAL DERIVATION REVIEW PENDING. The
implementation and audited proof are in
`theorems/ternary_sequential_spectral_extraction.py` and
`research/TERNARY_SEQUENTIAL_SPECTRAL_EXTRACTION.md`. Balanced cyclic averaging
improves the draft constant below to h_q=(q^2-1)/(4q). Exact independent
trajectory/reference replay and norm/metric/representation falsifiers are
implemented. The native access audit in `research/TERNARY_NATIVE_SPECTRAL_ACCESS.md`
is the follow-on; source construction and an efficient decoder remain absent.

The retained text below is the earlier proof draft, NOT an implemented native
decoder or an outstanding request to recreate the extractor. It avoids replacing a whole almost-
commuting operator family by nearby commuting matrices. No novelty claim.

## Why Change The Target

The exact flat character extractor is implemented. Global approximate
operator rounding is now a poor default: the retained Weyl falsifier has
nonzero winding, and the conservative many-generator repair loses precision
rapidly. Neither fact rules out approximating only the NATIVE MOMENTS in a
given state. That weaker, useful target has a direct positive construction.

Successive projective measurements and their back-action are established
quantum theory; see the primary
[Johansen paper](https://arxiv.org/abs/0705.0229). The quantitative n-generator
bound below is derived here and needs review, implementation and falsifiers.

## Required Supplied Objects

Let U_1,...,U_n be R-dimensional EXACT unitaries with U_i^q=I, q=3^r,
and pair commutator operator norms at mostdelta. Let psi be normalized.
For a public native unit difference basis D, write each native harmonic
frequency f as f=sum_i b_i*d_i, with BALANCED coefficients |b_i|<q/2.
Fix the product order1 throughn. Require an independently budgeted bound

    |m_f-<psi,U_1^(b_1)...U_n^(b_n)*psi>|<=sigma_f

for every original harmonic f=a_j,c_j,a_j-c_j. Do not omit the difference
observable, change the original moment block or infer this bound merely from
small rank. Unitarity, q-order, state normalization/positive metric and
operator-norm error are prerequisites, not promises supplied by a solver.

## A Genuine Character Distribution Without Global Operator Rounding

Projectively measure U_1, then U_2, ..., U_n. If P_(i,t) is the spectral
projector for eigenvalue chi_q(t), the sequential distribution is

    p(t_1,...,t_n)=||P_(n,t_n)...P_(1,t_1)*psi||^2.

It is positive and normalized even when the operators do not commute.
Every tuple t defines an actual shared secret s=D^-1*t moduloq, hence p
is a genuine distribution over characters. It need not exactly reproduce
the original operator moments: measurement disturbance must be bounded.

Let E_i(X)=sum_t P_(i,t)*X*P_(i,t), equivalently

    E_i(X)=(1/q)*sum_(k=0)^(q-1) U_i^k*X*U_i^(-k).

The weighted map Phi_(i,b)(X)=sum_t chi_q(b*t)*P_(i,t)*X*P_(i,t)
equals U_i^b*E_i(X). It is an operator-norm contraction, since E_i is an
average of unitary conjugations and U_i^b is unitary.
The expected character at f under the sequential distribution is

    E_p[chi_q(f.s)]
      =<psi,Phi_(1,b_1)(Phi_(2,b_2)(...Phi_(n,b_n)(I)))*psi>.

Compare this with the ordered product K_i=U_i^(b_i)...U_n^(b_n).
At stagei contraction gives a telescoping error at most
||E_i(K_(i+1))-K_(i+1)||. Averaging powers bounds this by

    ((q-1)/2)*||[U_i,K_(i+1)]||
      <=((q-1)/2)*sum_(j>i) |b_j|*delta.

The second inequality uses the product commutator identity and
||[U_i,U_j^b]||<=|b|*delta, also for negative powers. Summing stages yields

    |E_p[chi_q(f.s)]-<psi,K_1*psi>| <= L_f*delta,
    L_f=((q-1)/2)*sum_(j=1)^n (j-1)*|b_j|
       <=((q-1)^2/8)*n*(n-1).

Together with the ORIGINAL moment representation error sigma_f, the total
error is<=sigma_f+L_f*delta. This is polynomial in n,q, not the exponential
sequential GLOBAL operator-rounding recurrence. It does not contradict the
Weyl example: its delta isO(1/q), making this sufficient bound vacuous at
largeq. It also does not assert nearby commuting operators or order-independent
measurement distributions.

## Sampling Instead Of Enumerating q^n Branches

Given classical matrices and psi, one sequential draw tests q spectral
projectors at each of n steps, samples one conditional outcome and retains
only its updated vector. There is no q^n outcome table. Charge projector
construction, R-dimensional linear algebra, rational/algebraic coefficient
heights and finite-precision probability errors. q-projectors can use the
existing finite-order formula; exact zeros and positive probabilities need
certified arithmetic. At q=poly(n), R=poly(n), the stated matrix procedure
has polynomial arithmetic cost, NOT polynomial cost for exponentially largeq.

For the native harmonic score, each source contributes three real unit-phase
features. If the supplied moment score ismu, then

    E_p[score(s)] >= mu-B,
    B=sum_(all3m harmonics) (sigma_f+L_f*delta).

For independent samples, score lies safely in [-3m,3m]. A random draw has
probability at least epsilon/(6m+epsilon) of scoring at least its mean minus
epsilon. Thus K>=ceil(kappa*(6m+epsilon)/epsilon) draws give a sample with
score>=mu-B-epsilon except probability<=exp(-kappa)<=2^(-kappa).
This is a CLASSICAL conditional rounding/dequantization route for the
harmonic score, not full log likelihood or held-out true-secret recovery.

With quantum-only state access, repeated draws require fresh preparations;
unknown states cannot be cloned/reset for free. Every original native source
copy and controlled generator operation must be charged. Classical moments,
matrices and psi are not free consequences of native quantum state supply.

## Try To Falsify Before Promoting It

- Check the exact Heisenberg order; changing projection order changes p.
- Use noncommuting q-order matrices and test every balanced word expectation,
  not just one generator. At small sizes, enumerate outcomes ONLY as reference.
- Retain the Weyl example: the bound must become vacuous, not certify a
  globally commuting representation or a native matrix completion.
- Include exact commuting native-label mixtures as positive controls and
  original unit-basis pair/anchor counterfeits as failed representation inputs.
- Test a legitimate psi/metric; an indefinite Gram metric cannot define
  measurement probabilities. Operator norms cannot be replaced by entry errors.
- No hidden-secret input may select starts, matrices or sampling outcomes.
- Insufficient precision, unknown positive signs, dropped original observables
  or underbudget samples must stay UNKNOWN/unaccepted.

The central risk is upstream: native noisy records may not yield any costed
small-R matrix/state representation satisfying these premises. Proving the
conditional law does not solve that construction problem. If no concrete
source construction follows, deprioritize further generic representation
machinery and return to an actual collective receiver or source-aware learner.

## Completed Conditional Implementation Pass

Implemented `theorems/ternary_sequential_spectral_extraction.py`: exact weighted
pinching identities, coefficient-sensitive moment/error ledgers, positive
sequential probabilities, a one-branch sampler, native-score sample guarantee
and independent small reference replay. Reuse full-root cyclotomic arithmetic,
native difference bases and original-block falsifiers. Do not build another
global commuting-matrix optimizer or repeat noise/identifiability work.
Gemini handles routine CLI/registry wiring. GPT's next task must supply an
actual source-valid noncommuting receiver/learner or costed fiber transform,
not more generic spectral validators. The restricted native access audit
does not lower-bound general collective measurements.
