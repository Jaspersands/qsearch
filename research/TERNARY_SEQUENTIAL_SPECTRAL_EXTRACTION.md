# Sequential Spectral Extraction: Conditional Moment Rounding

IMPLEMENTED / LOCAL DERIVATION REVIEW PENDING. This is a supplied-matrix
classical extraction method, NOT a native decoder, novel quantum measurement,
proof of hardness or accepted quantum algorithm. Calibration matrices encode
KNOWN secret support; they were not learned from noisy native records.

## Premises That Are Actually Checked

For q=3^r, provide n exact R-dimensional operators U_i, a positive Hermitian
metric G and a normalized vector psi over Q(zeta_q). Require U_i^* G U_i=G
and U_i^q=I. Exact LDL certificates verify G>0 and

    delta_ij^2 G - [U_i,U_j]^* G [U_i,U_j] >= 0.

This is an operator-norm upper bound in G, not an entrywise tolerance. All
original first, second AND difference harmonics are retained. For a native
unit-difference basis D and balanced b=f D^-1 mod q, require

    |m_f - <psi, product_(i in committed order) U_i^b_i psi>_G| <= sigma_f.

The code independently checks this inequality, |m_f|<=1, identical-frequency
consistency and the zero-frequency moment. A different product order requires
revalidation, not reuse of a convenient old representation bound. Positive
metric, original-block and q-order failures cannot pass through sampling.

U_i^q=I is q-PERIODICITY, not a proof of primitive order q. For each spectral
family let g_i=gcd(q, all its nonzero-projector labels). Its exact period is
q/g_i, and extracted secrets satisfy (D*s)_i in g_i Z_q. The report charges
the resulting possible-secret coverage bound product_i(q/g_i)/q^n.
Qutrit order-three generators at a larger root may define a perfectly valid
distribution but cover at most3^n secrets, not all q^n. This is another reason
a certified conditional score cannot be promoted to full-secret recovery.
Actual nonzero projector vocabularies give the stronger bound
product_i(number of spectral labels of U_i). For EXACTLY commuting matrices,
joint spectral sectors are orthogonal, so there are at most R possible secrets.
The report retains the minimum of these bounds. In particular our known-support
commuting R3 calibrations cover at most THREE secrets, regardless of growing n.
An input-dependent learned model could select useful support, but that is the
missing inference algorithm; sparse fabricated support is not a shortcut.

## A Direct Distribution, Not Nearby Commuting Operators

The finite-order projector is P_i,t=(1/q) sum_k zeta_q^(-tk) U_i^k.
Measure these projectors sequentially in the committed order. The distribution

    p(t)=||P_last,t_last ... P_first,t_first psi||_G^2

is positive and normalized even for noncommuting operators. Every tuple t
gives a genuine shared secret s=D^-1 t. This does NOT assert a nearby commuting
matrix family or order-independent distributions.

Let E_i(X)=sum_t P_i,t X P_i,t and Phi_i,b(X)=U_i^b E_i(X).
These maps are operator-norm contractions in G. The moment of p equals the
expectation of nested Phi maps, with the first measured operator OUTERMOST.
Compare this nested expression to the ordered product. At each step the
remaining product is disturbed by E_i, while preceding errors are contracted.
Using balanced powers in the cyclic average gives the improved constant

    h_q=(1/q) sum_(k=-(q-1)/2..(q-1)/2) |k|=(q^2-1)/(4q),
    ||E_i(X)-X|| <= h_q ||[U_i,X]||.

The product commutator identity, including negative powers, then gives

    |E_p zeta_q^(f.s) - m_f|
      <= sigma_f + h_q sum_(a<c) |b_order[c]| delta_order[a],order[c].

Both complex moments have modulus at most1, so this error may be capped at2.
For a uniform delta, the coefficient is at most
h_q*(q-1)*n*(n-1)/4. Thus sufficient precision is inverse polynomial in n,q,
not the exponential many-generator GLOBAL rounding recurrence. Large q may
itself be exponential in input length. The known Weyl winding example remains
consistent: delta=O(1/q) makes this sufficient disturbance bound vacuous.

This is a direct local proof, not an application of an unstated approximate
flat-extension theorem. Sequential quantum measurements are standard; no
novelty of the measurement or the bound is claimed without literature review.

## One-Branch Sampling And Honest Abort Semantics

The classical sampler constructs q projectors per generator, then follows
one outcome path. It does NOT enumerate q^n secrets. It keeps unnormalized
vectors, so no square roots or normalized-state divisions leave the field.
Conditional probabilities are selected with dyadic random prefixes and exact
rational/algebraic sign certificates. A cap or unresolved sign aborts the
WHOLE run; it is never silently discarded and replaced with another draw.

Let the supplied harmonic score be mu and the sum of the original moment
error bounds be B. The actual character score is in [-3m,3m], and its mean
is at least mu-B. For epsilon>0, an ideal independent draw exceeds its mean
minus epsilon with probability at least epsilon/(6m+epsilon). Therefore

    K=ceil(kappa*(6m+epsilon)/epsilon)

independent draws give some score >=mu-B-epsilon except probability at most
exp(-kappa)<=2^-kappa. The implementation additionally checks the returned
score exactly. Seeded controls demonstrate a deterministic posthoc fact,
NOT an IID probabilistic failure guarantee.

With bounded-prefix aborts the coupling proves a bound on the joint event
"bad score AND a result returned". It does NOT prove the same failure bound
conditioned on completing, unbiased accepted draws, or a completion guarantee.
Choosing the best score needs exact comparisons; unknown comparisons abort.
The score is not the complete log likelihood, and a high score is not
held-out prediction or true-secret recovery.

Classical costs include supplied matrix bytes, field degree 2q/3, q^2*n
matrix terms to build projectors, R-dimensional arithmetic, coefficient
heights, probability precision and K draws. The arithmetic-count procedure
is polynomial in n,q,R,K; a full intermediate bit-complexity theorem is NOT
certified by these finite controls. Quantum-only access instead requires
fresh state preparations and controlled generators for every draw. Sample
supply does not grant those preparations, inverses or classical coordinates.

## Controls, Falsifiers And Research Decision

The live report keeps actual native-label controls at roots9/27 and growing
dimensions8/12, plus two noncommuting exact-order root9 controls in opposite
measurement orders. Only bounded n2 controls enumerate reference outcomes;
all81 balanced words are compared against the independently evaluated
Heisenberg law and the disturbance bound. Nonrational probabilities are
included. The supplied support is KNOWN and disclosed in every input model.

Falsifiers include indefinite metrics, false operator-norm bounds, missing
original difference moments, original representation mismatch, wrong order,
noncanonical/float bounds, insufficient complete caps, insufficient sample
budget and ambiguous random prefixes. None may be converted into acceptance.

The central unresolved premise is CONSTRUCTION of a useful polynomial-size
model from real native inputs with small delta and sigma. Merely fabricating
a commuting representation of known secrets does not discharge this premise.
An efficient classical construction would be a dequantization route, not a
quantum separation. Do not stack more abstract model validators next: audit
actual source operations and seek a costed native receiver or learner.

Gemini/Antigravity owns routine qsearch/registry/UI wiring and production
validation. GPT owns this proof audit and focused mathematical falsifiers.
