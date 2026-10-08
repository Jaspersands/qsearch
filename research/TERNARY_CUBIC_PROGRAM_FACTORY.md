# Unmatched Native Cubic Program Factory

LOCAL DERIVATION / REVIEW PENDING. A constructive fixed-root subsystem,
not an accepted new quantum algorithm or growing-depth speedup.

## Input And Physical Map

Start with disjoint, supplied original even-level4 native inputs (modulus9).
Use the existing fixed curvature-only windows of size(n+1)^2 to acquire
K=d+n odd-level3 inputs per program. The Gaussian packet retains at least d
joint coordinates. Keep its first d free coordinates and measure the rest,
accepting EVERY pointer, outer syndrome and complement. These frame choices
depend only on odd low rows. Original acquisition, active ancestors, unused
originals and measured branch masses are charged. Unique IDs rule out known
reuse but do not certify physical independence or upstream sample supply.

The retained state has component functions Q_j,l(z) of ordinary degree<=3
over F3. The canonical polynomial has individual exponents<=2, since z_i^3
is linear as a function. Compute mixed cubic terms from actual native low
rows and the physical kernel frame. Obtain lower terms with2d+binomial(d,2)
public residual evaluations, not a secret phase oracle or an exponential
phase table. The standardizing frame is explicitly a subset of free
coordinates: no unimplemented arbitrary chart is required.

The cubic vector space has

    R=n*(binomial(d+2,3)-d)

coordinates. R+1 programs guarantee a nonzero F3 relation c_j among their
cubic vectors. Gaussian elimination chooses this relation using ONLY cubic
low data. No top tensors need match. All acquired programs are charged,
including c_j=0 programs. Unselected states remain available but are not
claimed to be unconditioned fresh IID samples.

Prepare a KNOWN maximally entangled data/reference pair. For each c_j!=0,
apply SUM coefficient-c_j from data z into that single supplied program u.
Measure the program wires, obtaining m_j. The Kraus operator is

    K_(j,m)=3^(-d/2) diag_z omega^(<s,Q_j(m+c_j*z)>).

Consequently EVERY outcome has probability3^-d for arbitrary input,
including reference-entangled input. One unknown program is consumed once.
Coefficient2 means a domain sign, not two copies, conjugation, or an unknown
inverse. The output is a Choi state for

    G_l(z)=sum_selected Q_j,l(m_j+c_j*z).

Translation leaves each cubic top unchanged; domain scaling multiplies it
by c_j^3=c_j. Thus every cubic component cancels for EVERY transcript, not
only zero measurement outcomes. Drop the now-global constant, recompute
the resulting quadratic matrices M_l and linear offsets beta_l, and uncopy
the reference with inverse SUM if a flat program is needed. The implemented
quadratic receiver can then use a common isotropic line. Its direction must
read matrices ONLY, not beta. At d>=(n+1)^3-n the existing common-orthogonal
construction guarantees a nonzero such direction by known diagonal SDE.
Small bounded controls can lack a common direction; that is recorded as a
receiver failure, not filtered out of the population.

Teleportation/state injection is a known primitive, not a novelty claim:
[Zhou, Leung and Chuang](https://arxiv.org/abs/quant-ph/0002039).

## Source-Law Derivation

Assume the ORIGINAL frequency pairs are independent uniform modulo9 across
sites and secret coordinates. Condition on ALL original curvatures
k_i=(a_i+c_i) mod3. The fixed windows select supports using only these k_i.
Condition on their pointer outcomes, which are uniform independent of the
source frequencies because all input amplitudes have equal magnitudes.

Inside each nonempty support, keep its pivot at anchor0. Conditional on
its curvature, the pivot pair is uniform on an affine coset of

    H={(a,c):c-2a=0 mod3}.

Fix the other pairs temporarily. Their pointer-rotated contributions just
translate this coset. The support curvature sum is0, so the output pair is
uniform on H, independently of the fixed curvature data. Different supports
are disjoint, so their odd output pairs are independent. For each odd pair,
the following chart is a bijection:

    a=ell+3alpha, c=2a+3delta mod9,
    ell,alpha,delta independently uniform in F3.

Now condition on odd low rows ell, Gaussian syndromes and restriction
complements. The latter two outcomes are uniform independent of all source
high digits. The physical retained frame t_i(z)=b_i+D_i*z has full column
rank d. Its true residual phase contribution decomposes as

    fixed_low_carry(z)
    +sum_i alpha_i*(t_i(z)-b_i)
    +sum_i delta_i*(1[t_i(z)=2]-1[b_i=2]) mod3.

The first term is fixed by low data; the second is PURE LINEAR and gives
uniform alpha^T D in F3^d, since D has full column rank. The third contributes
quadratic matrices independent of alpha. In field3,1[t=2]=2(t^2-t).
This is an exact algebraic decomposition, not an empirical entropy estimate.

The relation selector uses low cubic vectors only. Injection outcomes are
uniform independent of alpha/delta even on entangled data. Each selected
nonzero domain coefficient preserves the full-rank alpha linear map. At
least one selected program supplies an independent uniform beta contribution.
Thus final beta_l are independent uniform vectors conditional on low data,
delta, source measurement outcomes and injection outcomes, and hence on M.
This conditioning EXCLUDES alpha/full public high linear metadata: after
conditioning on those, the offsets are of course fixed. The claim is an
ensemble label law, not hidden randomness conditional on every public label.

A matrix-only nonzero isotropic v therefore yields uniformly distributed
equation labels beta_l*v+2a^T M_l*v across independent fresh cohorts, even if
the fixed-program gradient is rank deficient. The receiver's Bell outcomes
are also fresh uniform. n+k independent equations have rank-failure bound
(3^n-1)/(2*3^(n+k)). This source theorem is locally derived, REVIEW PENDING;
finite censuses verify charts/identities but do not replace the proof or
certify that any external input source satisfies its physical IID premise.

## Costs And Why This Is Not A Breakthrough

At guaranteed width d=Theta(n^3), R=Theta(n^10) and each program consumes
(d+n)(n+1)^2=Theta(n^5) provided original inputs. This gives a worst-case
Theta(n^15) INPUT CAP per equation, Theta(n^16) for n+constant equations.
It is not a tight gate-count estimate. The actual dense relation representation
has R*(R+1)=Theta(n^20) field entries; ordinary Gaussian elimination has
O(R^2*(R+1))=O(n^30) field-operation scale. These are symbolic worst-case
counts, not measured hardware gates or a claim of practical efficiency.
Linear algebra/tensor expansion at this fixed degree are polynomial;
bounded amplitude replay is exponential and only a calibration, not part
of the intended runtime.

Known fixed-root sieves already have polynomial cost. This construction is
not shown to outperform them, and may be far worse. It recovers only s mod3
from root9 input, not all original secret digits. It closes a matching/copy
assumption in a constructive architecture, not the main complexity barrier.
At growing native depth, top feature dimensions and recursive source
consumption can be quasipolynomial. Even-degree tops do not admit the same
signed cancellation. No growing-depth factory, full-modulus recovery,
cryptographic sample supply, qubit synthesis or aggregate-error certificate
is supplied. No candidate is accepted as a speedup by this subsystem.

## Verification And Falsifiers

The producer fixes its seeds and records nonzero measurements, complete
bounded original-root polynomial tables and all one-use injection outcomes
for reference-entangled inputs. A separate JS checker reconstructs native
frequency charts, original affine maps, cubic relations, quadratic tables,
branch ledgers and receiver equations. Virtual calibration branches do not
constitute fresh source copies. Complete large cohort transcript enumeration
is NOT claimed: the all-transcript property follows from the top-degree
identity and the inductive Kraus formula.

Reject source reuse, mismatched dimensions, higher native levels, zero or
invalid coefficients and malformed measurement words. Attack the source law
with high-dependent selection and beta-dependent directions. Reject any
claim based on zero-outcome postselection, conjugate states, free factory
inputs, full gradient rank automatically guaranteed, or full-depth recovery.

```
python theorems/ternary_cubic_program_factory.py --write
node research/certificates/ternary_cubic_program_factory_crosscheck.js
python -m pytest -q tests/test_ternary_cubic_program_factory.py
```
