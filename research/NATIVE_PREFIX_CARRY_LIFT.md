# Native Prefix Rows And A Compact Mod9 Carry System

Local derivation / external review pending. This implements an actual public
low-prefix parametrization and the FIRST nontrivial carry constraints. It is
not a polynomial cubic solver, higher-root row compiler or new speedup.

## A Stronger Row Baseline Than The Unrestricted Relaxation

For actual native label pairs a_j,c_j, the word map modulo3 is

```
sigma(t) = sum a_j + sum (a_j+c_j)*t_j, t_j in F3.
```

When its slope matrix has full row rank, direct F3 affine parametrization
prepares all native words with the chosen low target digit. There are
3^(M-n) words per cohort, not q^(2M-n) arbitrary coefficient vectors.
The recipe/inverse are public, and only n pivot word coordinates depend
densely on the remaining k=M-n free trits. Free word coordinates are the
identity. All preparation, target controls and pointers still need physical
compilation/precision; no unknown input inverse is granted.

Filtering to an entire rootq target accepts eta_sigma/[B*3^(M-n)] if every
cohort has full prefix rank. For a fixed label family, averaging over all
higher target digits with the same low target gives exactly3^[-n(r-1)].
This mean is not a selected-target guarantee. For prescribed targets fixed
conditional on low labels before seeing higher labels,
conditioning on low labels and independent IID uniform higher original
label digits gives the same ensemble mean: every valid word contains a
unit original coefficient. The population law is an explicit promise,
not inferred from finite controls. Ordinary amplification of this fixed
prefix/filter preparation still pays the acceptance cost. Other structured
carry solvers are not excluded.
The basis choice and cohort weights in that population comparison depend
only on the low labels. Choosing an easy target or reweighting the input
using higher-label information is outside this stated mean bound.

## Actual First Carry, Not A Linear Approximation

Write every pivot trit as t_j=T_j mod3, where T_j=c_j+sum b_jl*u_l is an
integer affine form in free trits u_l. For ALL integers T,

```
T mod3 == T^3-3T(T-1) (mod9).
```

Together with the actual selector coefficients, this gives the exact local
frequency at modulus9

```
a_j + (c_label_j-2*a_j)*T_j^3 + 3*a_j*T_j*(T_j-1).
```

The constant c_j of the affine trit form is NOT the original label c_label_j.
The code uses distinct field names for them. This formula is verified against
the actual frequency evaluator, including roots larger than9. In those
cases it proves only the first two digits, not the entire higher-root target.

Reduce each pure free-trit cube by u_l^3==u_l+3u_l(u_l-1) modulo9.
The low-prefix equations force every remaining constant and linear
coefficient to be divisible by3. Higher-degree coefficients already contain
3. Dividing the canonical coefficient residues0,3,6 by3 produces a genuine
F3 polynomial system of total degree at most3 for the next target digit.
This is INTEGER coefficient division after verification, not inversion of3
in Z9.

## Compact Cubics, Not A Huge Expanded Tensor

For a pivot form c+L_b, define the divided cube

```
D_b(u) = [(sum b_l*u_l)^3 - sum b_l^3*u_l^3]/3 (mod3).
```

Its numerator is always divisible by3. It has mixed monomials u_l^2*u_m
and u_l*u_m*u_h, and no pure cubic monomials. It is NOT an ordinary rank-one
cubic over characteristic3. Calling its cube tensor rank1 would be false.

For output coordinate i, set w_j=c_label_ji-2*a_ji. After constant/linear
coefficient reduction, each pivot contributes

```
(w_j*c_j+a_ji)*L_b(u)^2 + w_j*sum b_l*u_l^2 + w_j*D_b(u).
```

Every free site contributes only (w_j+a_ji)*u_l^2. Thus a compact circuit
needs at most n dense divided-cube forms, n dense squares, and a diagonal
quadratic for each of n equations. It does not materialize k^3 entries.
The module also offers a capped expanded canonical polynomial for independent
small ANF checks. No small-degree assertion is inferred merely from a fit.
The vector coefficients w_j modulo3 on pivot divided cubes equal the
invertible prefix slope minor S, because c_label_j-2*a_j==c_label_j+a_j
mod3. Applying S^(-1) to the output equations therefore isolates one
divided-cube form in each output equation and preserves the zero set.
Quadratic terms and shared free variables remain coupled. This is an
output-basis identity, not independent scalar solving or diagonal SDE.

## Why This Is A Useful Search Target

The missing row primitive can now be attacked as structured public carry
equations rather than a black-box short-preimage oracle. There are only n
next-digit constraints and about n^2 free variables in the current regime,
but that alone does not give a polynomial solver or ensure every target is
solvable. A useful algorithm must sample the CORRECT uniform/coherent row,
not just find one solution, and must handle later digits without erasing
cohort phases or silently discarding failure. Any classical target-word
solver triggers the original-data classical reconstruction audit.

Likely failure: solving the cubics reduces to the original hard word problem,
an apparently useful affine restriction eliminates too much row mass, or
complexity/degree grows rapidly on later carries. A mod9 result must not be
extrapolated to arbitrary r. Study existing underdetermined polynomial-system
methods before introducing a solver. Higher-root equations, coherent cleanup,
complete sampling law and original-data baselines remain open obligations.

Falsifiers: treating canonical trits as unrestricted Z9 variables; ignoring
the cube reduction; dividing nondivisible coefficients; calling divided
cubes rank-one F3 cubics; inferring chosen-target success from a mean; or
promoting a mod9 match to a higher-root match.

Run `python theorems/native_prefix_carry_lift.py --write` and its tests.
