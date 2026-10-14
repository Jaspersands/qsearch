# Actual Full-Root Small-Alphabet Classical Decoder

Constructive local derivation; external review and prior-art audit pending.
No novelty, general Gaussian LWE solver or new quantum speedup is claimed.
This supplies a stronger baseline for the repository's bounded-noise fixtures.

## Two Source Families

Input is the ACTUAL classical bank y=a.s+e modulo q=3^r. Cubic decoding
requires q>=9 and canonical circular errors in{-1,0,1}. The faster quadratic
path requires errors in{-1,1} and q>=3; it reuses the existing ternary
exclusion equations without pretending a quantum measurement occurred.
Source values are explicitly legal only on this classical-original interface.
No secret, errors, mask, multiple producer or extra oracle enters either path.

## Divide Before Reducing

For the cubic path write s=u+3v modulo9, with u canonical F3 trits.
For original a,t reduced modulo9, put x=t-a.u. Errors0,+/-1 satisfy
x^3-x=0 modulo9. Exact integer division gives

    (x^3-x)/3 + a.v = 0 modulo3.

The quotient is well-defined under representative changes by9. Reducing
first would give the vacuous field identity x^3=x. On CANONICAL trits,
u_i^3=u_i+3*(u_i^2-u_i). Expanding and dividing produces mixed cubics
plus a linear v term. The exact coefficients are implemented and replayed
independently by integer polynomial multiplication, not assumed field cubes.

Features are u_i, u_i^2, u_i*u_j, u_i^2*u_j, u_i*u_j*u_k and v_i.
Their width is D=3n+C(n,2)+n(n-1)+C(n,3)=O(n^3).
A full-rank F3 solve MUST reproduce every nonlinear feature identity.
All original rows are used, no truth assignment or secret enumeration.

Given correct s mod9, subtract it from ORIGINAL responses, round to
9-spaced centers and solve the remaining noiseless equations modulo q/9.
The quadratic path analogously uses the known order3 exclusion algebra
to recover s mod3, then3-spaced centers. Both use a label-only unit minor
and exact Newton/Hensel inverses, checking all higher-root equations.
The FINAL original circular residuals must fit the declared alphabet.

Full feature rank plus a unit higher-root minor also establishes uniqueness
within that circular alphabet on this FIXED instance: any compatible secret
has the same feature vector/low prefix; two higher parts cannot differ since
their response difference is a multiple of3 or9 while two permitted errors
differ by at most2. This does NOT identify the planted secret if the actual
source violates the alphabet. A label-aligned large-error countercontrol
must remain distinguishable from valid bounded-noise recovery.

## Cubic Rank Distribution

Write a=a0+3a1 and t=t0+3t1. Coefficient row functions contain unique a1_i
in the u_i columns. Once those dual coefficients vanish, the remaining
row function is t0*Q(a0)+R(a0), with Q a homogeneous reduced quadratic.
Its t0*a0_i^2 and t0*a0_i*a0_j terms uniquely identify the quadratic
feature coefficients. Remaining cubics and linear a0_i terms are distinct
reduced ANF monomials. Thus the full public coefficient function family
has no nonzero dual annihilator. Complete parameter grids verify n1/n2/n3;
the general argument is triangular, not inferred from those counts.

A nonzero reduced F3 polynomial of total degree<=2 has relative support
at least1/3; for degree<=3 it has support at least2/9. Induct on a variable's
leading coefficient: a nonzero univariate polynomial of degree e<=2 has
at least3-e nonroots, and its leading coefficient uses the remaining
degree. The worst degree3 product is (1/3)*(2/3)=2/9.

For independent uniform original labels and independent bounded noise with
all three residues having probabilities>=p_min, the coefficient parameters
(a0,a1,t0) dominate uniform mass by3*p_min. Row escape from every proper
hyperplane is at least2*p_min/3.

The ACTUAL older fixtures instead use ONLY +/-1. With at least two distinct
noise residues each having probability>=p_min, use a different argument:
nonzero a1 terms escape with probability2/3. Otherwise Q!=0 has support
at least1/3 and a nonconstant linear t0 function cannot vanish on BOTH
noise choices, giving escape>=p_min/3. If Q=0, the nonzero R escapes with
probability>=2/9. Do not import an all-three-residue probability floor into
the signed-only source.

The rank-failure union is at most (3^D-1)/2 times (1-escape)^m.
Large ledgers use exact integer power-block/dyadic bounds with capped
conservative confidence budgets instead of giant rational strings.
Sample generation/law/IID promises are not inferred from IDs or finite rank.
Deterministic noiseless data has its own ordinary linear baseline; it is not
a positive noise-probability floor by fiat.

## Cost And Falsifiers

The cubic matrix costs O(m*n^3) row construction, O(m*D^2) naive field
elimination, O(m*D) storage and polynomial log(q)-bit original-data lifting.
Whole-matrix caps reject BEFORE construction and do not prove no secret.
Quadratic signed-only decoding uses O(n^2) features and is the stronger
baseline on that family. No exponential helper or quantum preparation is paid.
Logical entry caps do not purport to include Python/FLINT object overhead.

Reject: a failed rank treated as no original secret; a field solution with
inconsistent nonlinear features; low9 promoted to the full root; composite
field inversion; corrupted equations silently repaired; or a bounded
alphabet substituted for unbounded Gaussian source errors without a
whole-bank tail/coupling budget. Noiseless and sign-only cases are not
evidence that the campaign's Gaussian source is easy.

[Arora and Ge's linearization work](https://eccc.weizmann.ac.il/report/2010/066/revision/1/download)
is prior-art context, not a certified applicability/novelty claim for this
integer-valued prime-power construction. The primary PDF is accessible;
a complete literature comparison remains outstanding.

    python theorems/native_small_alphabet_decoder.py --write
    node research/certificates/native_small_alphabet_decoder_crosscheck.js
    python -m pytest -q tests/test_native_small_alphabet_decoder.py
