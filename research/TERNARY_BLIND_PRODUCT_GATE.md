# Label-Independent Product POVM Gate

LOCAL DERIVATION / REVIEW PENDING. This strengthens the fixed-Fourier gate
to arbitrary fixed finite single-qutrit POVMs. It does NOT exclude label-aware,
outcome-adaptive or collective quantum receivers, or polynomial surplus copies.
No novelty or algorithm claim. See `TERNARY_PRODUCT_TRINE.md` for the source
and the exact likelihood/classifier convention.

## Exact Single-Copy Invariants

Let {E_y} be any positive complete qutrit POVM, fixed independently of ALL
native frequency labels and the unknown secret. Null effects can be omitted.
Use reference output mass m_y=Tr(E_y)/3, independently of uniform full native
rows a,c. Native source states have phases (1,chi(a.s),chi(c.s))/sqrt3.
Their relative likelihood has six root-character terms, with coefficients
E_ij/Tr(E_y) for i!=j. Define real scalars

    d   = sum_y sum_(i!=j) |E_y[i,j]|^2/(3*Tr(E_y)),
    eta = sum_y sum_(i!=j) E_y[i,j]^2/(3*Tr(E_y)),
    d0  = sum_y (sum_(i,j) E_y[i,j]-Tr(E_y))^2/(3*Tr(E_y)).

Hermiticity pairs conjugate entries, making eta and d0 real. PSD gives
|E_ij|^2<=E_ii*E_jj. Therefore

    sum_(i!=j)|E_ij|^2 <= (Tr E)^2-sum_i E_ii^2 <= (2/3)*(Tr E)^2.

Summing and using sum_y Tr E_y=3 yields 0<=d<=2/3. Triangle inequality gives
|eta|<=d. At the zero secret L0=p0/m<=3, so E_m L0^2<=3 and 0<=d0<=2.

Full native label orthogonality over the composite ring gives centered Gram

    s=t=0: d0,
    s=t!=0: d,
    s=-t!=0: eta,
    all other pairs: 0.

Nonparallel A2 root rows have a unit minor, forcing BOTH secrets to zero.
Parallel opposite root rows require s=t; parallel equal rows require s=-t.
Unlike fixed inverse-F3, an arbitrary basis need not cancel the opposite-secret
term. Since q is odd, every nonzero secret belongs to a distinct pair {s,-s},
including nonprimitive secrets. Dropping eta would be an invalid stronger bound.

## Different Fixed POVMs On Different Copies

For M independent originals with invariants d_i,eta_i, the nonzero centered
product Gram is a direct sum of 2x2 blocks

    [[delta,kappa],[kappa,delta]],
    delta=product_i(1+d_i)-1, kappa=product_i(1+eta_i)-1.

Its exact operator norm is delta+|kappa|. Positivity and |eta_i|<=d_i imply
|kappa|<=delta: the lower product bound also uses
product_i(1+d_i)+product_i(1-d_i)>=2, whose expansion keeps positive even-degree
terms. Thus the operator norm is at most2*((5/3)^M-1).

Apply the three-class likelihood argument from the product-trine derivation,
now using this operator norm instead of a diagonal Gram. The nonzero-secret
contribution to uniform-secret least-trit advantage is at most

    sqrt((delta+|kappa|)/(2G)) <= sqrt(((5/3)^M-1)/G), G=q^n.

The zero-secret contribution is at most TV(P0,Q0)/G. The zero input is a pure
M-qutrit state and the reference is the maximally mixed state. Measurement
contraction of trace distance gives TV<=1-3^-M. Consequently the universal bound
is

    mean advantage <= min(2/3,sqrt(((5/3)^M-1)/G)+(1-3^-M)/G).

This handles different POVMs per copy and ANY subsequent joint classical
computation. Shared public measurement randomness independent of source labels
is covered by conditioning on that randomness first; do not incorrectly claim
that the unconditional records are IID when they share coins.

At M=nr-2 the bound is exponentially small. The difference from the exact
fixed-F3 bound is a factor sqrt2 on its nonzero term, not a new asymptotic
algorithm. The result says where measurement structure must change at this
copy budget; it does not say whether another measurement is efficient.

## Exact And Physical Controls

The producer certifies Hermiticity, ALL principal minors and completeness with
symbolic exact arithmetic for computational, F3, real two-level and real dense
bases, plus a public mixture. Matrices are serialized in Q(omega). The named
control invariants are rational; unproved PSD or unresolved scalar signs fail
closed. This finite control representation is NOT the theorem's restriction
to rational measurements.

Full q9 native-label Born censuses keep all zero, primitive, nonprimitive and
opposite secrets. The real two-level basis has d=eta=1/3, demonstrating why
diagonality cannot be imported from the F3 receiver. A Y-like two-level basis
has negative eta and is separately tested, so product kappa may be negative.
The scalar gate accepts supplied lawful invariants only as assumptions unless
their actual POVM has been certified. Dense census arrays are calibration costs.

## Attempted Refutation And Next Target

- Label-conditioned POVMs make root coefficients functions of a,c; the
  orthogonality proof then fails. Even inexpensive label-dependent phases can
  lie outside this theorem. This is a real escape route, not a minor caveat.
- Adaptive basis choices depending on prior outcomes change the batch law.
  The product Gram factorization is not automatically a sequential lower bound.
- Entangling readout is not required by this result. Label-aware local readouts
  remain open, and the preceding source-valid correlation control guards against
  mistaking local gates for bounded-radius effects.
- More copies can make the gate vacuous with a constant-factor surplus in nr.
  That is still polynomial sample cost; decoding might remain computationally
  hard, but this gate cannot establish it.
- The public-label native source must actually be available. None of these
  receivers supplies a reduction to an important input problem or state source.
- An independent expert should review the operator-norm/classifier transfer,
  composite-ring orthogonality and shared-randomness conditioning. Exact finite
  checks and automated certificate replay are not a replacement for that review.

The useful constructive target is a label-sensitive measurement policy or
collective observable with an explicit efficient implementation and a source
law different from this bounded-information product pipeline. Do not create
more blind basis benchmarks as algorithm candidates.

```
python theorems/ternary_blind_product_gate.py --write
node research/certificates/ternary_blind_product_gate_crosscheck.js
python -m pytest -q tests/test_ternary_blind_product_gate.py
```
