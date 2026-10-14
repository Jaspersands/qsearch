# Original-Data Modulus Descent And Lost Information

Local constructive derivation; external review pending. This is an actual
classical-record transformation, NOT an operation on unknown quantum phases.
It establishes neither a polynomial LWE solver nor a general quantum no-go.

## Actual Source Transformation

For q=3^r, r>=2, take disjoint blocks of n+1 ORIGINAL paired records
(a,y_a),(c,y_c). Compute a nonzero F3 kernel vector v for the n by n+1
matrix of slopes (a+c) mod3, using slopes only. For z=1,2, a site's native
selector difference from selector0 has coefficients (-2,1) or (-1,-1),
depending on v*z mod3; zero direction sites contribute nothing.
Let Delta A_z, Delta Y_z be the actual signed original sums. The kernel
condition makes Delta A_z divisible by3 modulo q. Set

```
U_z = (Delta A_z modq)/3 in Z_(q/3)^n
W_z = nearest_integer(Delta Y_z/3) mod(q/3).
```

Nearest third is exactly floor((x+1)/3), including negative integers; there
are no ties. Adding q to an original response shifts its rounded signed
combination by an integer multiple of q/3. Thus the transformation is
well-defined on actual circular observations. If y=a.s+e modq,

```
W_z = U_z.s + nearest_integer(Delta e_z/3) mod(q/3).
```

No secret, source error, known mask or fresh error oracle enters the code.
One output pair uses n+1 input pairs, including inactive sites in its paid
block. Every original ancestor is retained in the verification lineage;
reusing ancestors as independent blocks is rejected. Tails are explicitly
unused. Derived pairs keep their correlated-noise type through recursion.

## Conditional Label Distribution

Condition on ALL LOW SLOPES, not all low original labels. Original full a
is then uniform, and higher digits of c are independently uniform. Fix all
but one active site. There U1+U2 equals minus the sum of active ORIGINAL a
modq/3. Vary that site's full a over Z_q and c's higher digits over Z_(q/3).
The sum is uniform; independently a unit coefficient of c's higher digits
makes U1 uniform. Each output pair has exactly3 preimages per coordinate.
The reversed selector orientation has the same property. Independent
coordinates and disjoint source blocks give IID uniform output label pairs.

Conditioning on all low original labels instead fixes the pair's sum mod3,
and joint uniformity FAILS. Exact finite populations verify both statements.
This distinction repairs the nonunit determinant3 of the two difference
coefficient rows; it must not be erased by pretending arbitrary ring
choices were the source. Output labels are uniform even conditional on
the original errors, if those errors are independent of labels/secret.

## Correlated Noise And Recursion

With independent symmetric original scalar errors of second moment<=V,
an active m-site branch has second moment<=5mV before rounding. The two
branches have covariance mV before rounding (for identical true variance V).
If only independent scalar variance uppers<=V are promised, the covariance
can be as large as2mV; the API charges this heteroscedastic upper, not mV.
They are NOT independent. Nearest-third noise is jointly sign symmetric;
E rounded_error^2 <= (2/9) E Delta_error^2 +1/2.
Thus the first-level marginal bound is 10mV/9+1/2.

At subsequent levels only independent PAIRS and conditional joint sign
symmetry may be used. The conservative within-pair covariance bound gives
E Delta_error^2<=9mV and rounded bound<=2mV+1/2. Never reuse the independent
scalar5mV rule for derived pairs. Public local slope selection preserves
these conditional promises for this source; arbitrary adaptive reuse does
not. Increasing upper noise budgets are NOT lower bounds or general no-gos.
Moments alone do not upper-bound maximum noise atoms. Exact pushforwards
are available only for a separately DECLARED finite original error law.

The SAME-BANK fixed block policy supplies floor(M/(n+1)^d) pairs after d
levels. One modulus3 pair at depth r-1 therefore requires (n+1)^(r-1)
original pairs. All four cubic-bank, r=n scaling controls have zero terminal
pairs. This is exact accounting for this disjoint-block policy, not a lower
bound on alternative sieves, overlapping correlated reuse or coherent
receivers. Fresh copies prepared from old classical records are not fresh
original errors or new independent source pairs.

## Exact Information Erasure

Hold original labels and errors fixed. Replacing s by s+(q/3)h changes
each original response by a.(q/3)h. Each selected Delta A is divisible by3,
so the change in Delta Y is a multiple of q. Its descended response is
identical modulo q/3. After d levels the final observation depends only
on s mod(q/3^d). For a uniform original secret, even a noiseless optimal
decoder using ONLY final observations has full-secret success<=3^(-nd).
This is an exact quotient ambiguity, not an experimental hardness signal.

For t final pairs and a true uniform conditional joint-noise max-atom upper
beta, independent across final pairs, a sharper bound is

```
Pguess(full original secret)
 <= 3^(-nd) * min(1, (q/3^d)^(2t-n) * beta^t).
```

Proof: sum the largest likelihood over the (q/3^d)^(2t) possible response
tuples under a uniform remaining secret with (q/3^d)^n possibilities.
Each likelihood is<=beta^t. Multiply by the unresolved uniform alias mass.
Without a noise-atom premise, the same observation-alphabet bound uses1 in
place of beta^t and requires no independent-pair noise assertion. In
particular zero responses give success<=q^(-n), not just the alias bound.
Large bounds retain exact base3 exponents rather than expanding thousands
of denominator digits; a missing short rational is not an unknown bound.
This is an information bound for arbitrary classical OR quantum processing
of these observations, including repeated preparation with fresh known
coins. It is not a bound on genuinely new independent samples.

CRITICAL scope: original/intermediate responses, value-dependent parent
hashes and proof receipts, noise/truth fixtures, and unknown quantum-only
input states are EXCLUDED. Verification artifacts retain parents and
therefore are not themselves compressed-only receiver inputs. Even a hash
of parent responses is a potential secret-dependent side channel. Receivers
that keep a complement or return to the original bank remain open.

## Countercontrol: The Original Bank Can Restore A Digit

The module also implements a CONDITIONAL original-bank top-digit lift.
Given the CORRECT lower vector x=s mod(q/3), form each original residual
y-a.x = (q/3)*(a mod3).h +e modq, where s=x+(q/3)h. Nearest of the three
circular centers gives an F3 equation for h whenever |e|<q/6. A row basis
chosen from original labels before response processing solves h over F3;
all remaining rounded equations are checked. Rank deficiency and inconsistent
equations are failures, not recovered secrets. Reading the original values
is explicitly charged and violates the compressed-only receiver restriction.

Under a true original moment upper V, rounding union loss is<=36mV/q^2 for
m paid original rows; IID uniform low labels add rank failure upper
(3^n-1)/(2*3^m). Both are conditional on a correct lower vector. The charged
budget uses the conservative3^[-min(64,m-n)] rank upper instead of expanding
an enormous rational denominator; the exact hyperplane expression stays symbolic.
Both budgets require the stated source law. A consistent
answer does not verify that vector or the noise promise: correlated label-
aligned errors can manufacture a wrong consistent answer. The live lift
controls supply the lower vector from truth ONLY to verify this conditional
mechanism, never to pretend the unresolved lower decoder exists.

For m about n^3 and V/q^2 about n^-6, this digit lift has a useful growing-n
conditional budget. Thus information erasure is a receiver-interface error,
not an impossibility of an original-bank recursive algorithm. The substantive
remaining problem is recovering the lower quotient after contraction without
overwhelming its information/noise budget. Keep that open rather than
turning this local quotient ambiguity into another overbroad no-go.

## Literature And Research Decision

[Brakerski et al., Classical Hardness of Learning with Errors](https://arxiv.org/html/1306.0281),
Sections3-4, supplies established modulus/dimension switching and small-secret
reductions. It does not grant arbitrary-secret coordinate rounding at fixed
dimension. This local block cancellation avoids that particular secret
rounding term by producing exact divisible labels; it pays sample contraction,
correlated noise and lost secret digits instead. No novelty priority or
replacement for the published reduction is claimed.
[Kirchner and Fouque, improved BKW](https://arxiv.org/abs/1506.02717)
is a necessary further sample/noise/runtime comparison, not yet implemented
for this paired source. The new
[sample-preserving search-to-decision paper](https://arxiv.org/abs/2610.12913)
also deserves composite-modulus applicability review. Its introduction and
Section4.1 retain a distinguisher/verification requirement and nonunit-multiple
ambiguity; they do not supply our missing lower decoder. An original-bank
completion of a recovered lower quotient needs its own amplified-noise budget.

Next high-impact task: identify and retain the complement carrying the lost
digits, then cost its classical and coherent use. Repreparing many states
from the same compressed values cannot restore them. Do not turn this
scoped failure into a general prohibition on original-bank or quantum LWE
algorithms. Mathematical review, source-specific atom bounds and a complete
end-to-end receiver remain outstanding.

```
python theorems/native_classical_modulus_descent.py --write
python -m pytest -q tests/test_native_classical_modulus_descent.py
```
