# Approximate Translations: A Falsifier And A Finite-Order Repair

KNOWN OPERATOR-THEORETIC MECHANISM; LOCAL ADAPTATIONS / REVIEW PENDING. These
are translation-certificate tests, not oracle problems or algorithm candidates.
They neither give a native noisy decoder nor rule out source-specific quantum
or approximate moment methods.

## Kill The Naive Operator-Norm Rounding Claim

At FULL q=3^r define clock Z|j>=chi_q(j)|j> and shift X|j>=|j+1 modq>.
Both have qth powerI, but ZX=chi_q(1)*XZ. Their group commutator is
ZXZ^*X^*=chi_q(1)*I. The ordinary commutator operator norm is

    |1-chi_q(1)| in [4/q, 44/(7q)].

The upper bound uses pi<22/7; cap it at2. Thus errors tend to0 as q grows.
Nevertheless NO commuting unitary pair can be within1/4 of both matrices
in operator norm. Exact finite order and a small commutator alone are not
a uniform certificate of proximity to a true character representation.

The winding/Bott obstruction is established work, not a new result. Primary
sources include [Exel--Loring](https://doi.org/10.1016/0022-1236(91)90034-3) and
[Loring's quantitative study](https://sigma-journal.com/2014/077/).

For this pair the principal logarithm winding is exactly

    (1/(2*pi*i))*Tr log(ZXZ^*X^*)=q*(2*pi/q)/(2*pi)=1.

For commuting matrices it is0. Every unitary commutator has determinant1, so
the principal-log expression is an integer and is constant along any path
whose commutator spectrum avoids-1. If a commuting pair were within epsilon
of Z,X, their short unitary logarithm paths remain within epsilon. Telescoping
the four commutator factors gives distance<=4*epsilon from chi_q(1)*I.
That scalar is distance2*cos(pi/q)>=1 from-1 for every q>=3. At epsilon<1/4
the path therefore avoids-1, contradicting the change from winding1 to0.

The implementation stores the exact symbolic full-root schema, rational norm
bounds, index and homotopy margin, without allocating q-by-q matrices. Large
q still means operator dimensionq; this is not a free small-rank representation.
At root59049 its commutator passes a1/1000 threshold while the1/4 obstruction
remains. Root3^20 also passes. Neither is a supplied native flat completion.

This is an OPERATOR-NORM obstruction. Do not extend it to normalized
Hilbert--Schmidt distance, selected moments, held-out secret prediction or
all approximate flat source ensembles. Extra native consistency constraints
could exclude the obstructed pairs. Numeric tiny eigenvalues/commutators
alone do not establish that exclusion.

## Positive Finite-Order Pair Law

The negative example does not make approximation hopeless. Let U,V be EXACT
unitaries with U^q=V^q=I and ||UV-VU||<=delta. Pinch V into U's eigenspaces:

    A=(1/q)*sum_(k=0)^(q-1) U^k*V*U^(-k).

This commutes with U. Telescoping bounds ||A-V||<=eta=(q-1)*delta/2.
If eta<1, A is invertible. Its polar unitary W commutes with U, and its
singular values lie in [1-eta,1+eta], so ||W-V||<=2*eta.

V has only qth-root eigenvalues. Normal-resolvent perturbation puts every
eigenvalue of W within2*eta of some V eigenvalue. Round W's eigenvalues to
the nearest qth roots, preserving its commutation with U. The resulting
unitary V' satisfies (V')^q=I and

    ||V'-V||<=4*eta=2*(q-1)*delta.

This is dimension-independent but q-DEPENDENT, and requires a certified
operator-norm bound plus exact input orders/unitarity. An entrywise residual
is not that bound, and floats do not establish those premises. It is fully
compatible with the Weyl falsifier: its commutator lower bound4/q already
violates eta<1 for every q>=3.

Numerical controls use rational planar conjugations of known commuting
q-order diagonal matrices. Their analytic commutator bound is8*t from
||H-I||<=2*t; it does NOT come from observed floating residuals. Replay uses
SciPy polar and Schur decompositions at roots9/27. Numerical output metrics
are calibration only, not exact certificates or unknown-secret recovery.

## More Generators: Do Not Hide Precision Growth

For commuting already-rounded generators, their pinching maps commute and
can be applied successively using O(n*q) terms, not q^n group enumeration.
But their errors relative to original generators worsen the next commutators.
If each original pair commutator is<=delta and previous rounding errors are
epsilon_i, a conservative iterative guarantee is

    epsilon_j <= 2*(q-1)*[(j-1)*delta+2*sum_(i<j) epsilon_i].

The implementation retains exact coefficients e_j with epsilon_j<=e_j*delta
and reports the sufficient delta for a chosen total error. These coefficients
grow rapidly with n; this method does NOT prove polynomial precision in n.
The bound can be loose and is NOT a general impossibility theorem. Improving
it with source structure, a global consistency law or certified gaps is a
real mathematical task, not a tolerance-setting exercise.

## Revised Next Research Target

Native approximate flat extraction must control the ORIGINAL Gram block,
positive weights, metric conditioning, operator norm, q-order and all
generator relations. It must exclude nonzero winding where relevant AND
avoid the sequential precision blowup. The pair law is only one component.
No generic optimizer or rounded low-rank matrix can replace these obligations.
Observable-only decoding could avoid global operator reconstruction; test
that alternative rather than assuming the topology rules it out.

Gemini owns optional CLI/registry integration and full production validation:

```sh
python theorems/ternary_translation_stability.py --write
node research/certificates/ternary_translation_stability_crosscheck.js
python -m pytest -q tests/test_ternary_translation_stability.py
```
