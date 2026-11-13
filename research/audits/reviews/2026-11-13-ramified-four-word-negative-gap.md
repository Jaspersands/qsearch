# Prescribed negative-gap four-word attack: scoped negative result

2026-11-13. STATE/TRAPS and the retained exact Q2(sqrt2) data were read.
Only the two requested valuation patterns were tested, in the requested
order. No network, API, Git, archives, paid calls, or shared-status edits.

**Result.** No >4 or disconnected isometric target was found. The maximal
shortest paths were 2 for R=(0,-2,0), and 3 for R=(0,-2,1). This is a finite,
scoped negative search result, not an all-field four-word completeness proof.
No other field or valuation pattern was added.

## 1. Exact search universe and independent isometry criterion

Use F=Q2(pi), pi^2=2, with e=2,f=1, r=1+pi, s=1+2pi, delta=5.
The squareclass generators (pi,r,s,delta) and unit classes are the same as
in the already verified three-word counterexample. The exact Hilbert-bit
matrix, recomputed by Sage/PARI, is

    [1 1 0 1]
    [1 1 1 0]
    [0 1 0 0]
    [1 0 0 0].

It has rank four. The unit classes 1,r,s,rs,delta,r*delta,s*delta,rs*delta
have defects infinity,1,3,1,4,1,3,1, respectively; [-1]=[s*delta].
Defects were checked using exact algebraic integers modulo pi^5, not
floating p-adic approximations. These eight unit classes are complete.

Normalize the first initial coefficient to 1 by a common unit scaling.
For each ell in {0,1}, use valuation pattern (0,-2,ell), so u=-2,v=ell+2.
Enumerate initial norm classes (1,pi^-2*b,pi^ell*c), with b,c ranging over
the eight unit classes. Test the actual good-BONG conditions

    u+d(C)>=0,  v+d(D)>=0,  C=-a1*a2, D=-a2*a3.

Together with u,v>=-2e and R1<=R3, these are Beli LF85–97's existence
conditions. Exactly 32 initial class tuples survive each pattern.
For each start enumerate all unit endpoint ratios x,z; determinant-square
matching fixes the middle ratio as x*z. Check the target's good-BONG
conditions separately. The target is NOT declared isometric from reachability.

Instead apply actual Beli Theorem3.1, LF680–686 of
sources/2026-11-13-expanded-norm/beli_classification.txt:
matching R and alpha; d(x)>=alpha1, d(z)>=alpha2; matching rational Hasse
invariants; and its extra binary representation condition when required.
The implemented formulas are

    h=min(e+u/2,u+d(C)),  k=min(e+v/2,v+d(D)),
    alpha=(min(h,u+k), min(k,v+h)),
    Hasse difference=<C,x>+<D,z>+<x,z>.

All surviving cases here have alpha=(1,3). Thus alpha1+alpha2=2e and the
STRICT extra condition(iv) is inactive. The control nevertheless includes
that condition as <C,x>=0 whenever alpha1+alpha2>2e. All inequalities are
computed with doubled integer thresholds, avoiding half-integer rounding.

## 2. Actual binary graph, not a guessed normal-form test

At every vertex, recompute the current C,D. A move on the pair of valuation
difference w may use precisely the unit classes eta satisfying

    d(eta)>=min(e+w/2,w+d(current product class)),
    (current product class,eta)=+1.

This is Beli Lemma5.1/LF980–997 and the already proved order-unit coordinate
operation. Both adjacent pairs are allowed. A breadth-first search computes
shortest lengths; it checks that each reached vertex remains a valid good
BONG. It also verifies that the full reachable set equals the independently
computed isometric endpoint set for every start. Identity moves and free
unit-square changes do not inflate the reported minimum lengths.

The exact output is:

| R | Valid normalized starts | Isometric ordered pairs | Distance counts | Maximum |
|---|---:|---:|---|---:|
| (0,-2,0) | 32 | 640 | 0:32, 1:224, 2:384 | 2 |
| (0,-2,1) | 32 | 512 | 0:32, 1:192, 2:224, 3:64 | 3 |

The second pattern ran only after the first found no >4/disconnected target.
The control would stop immediately at the first such target, but none occurred.
These counts are not estimates, and no probabilistic local equality test is used.

## 3. These are actual lattice patterns, despite the negative BONG entry

For the chosen representatives, validity forces b in {1,s,5,5s}; hence
1+b is divisible by pi^2. The binary reconstruction takes c0=1/pi:

    L12=O*e1+O*(pi^-1*e1+e2),
    q(e1)=1, q(e2)=b/pi^2, B(e1,e2)=0.

Its Gram matrix is [[1,pi^-1],[pi^-1,(1+b)/pi^2]]. Adjoin the third
orthogonal line of norm pi^ell*c. Multiplying the whole form by pi gives
the explicit INTEGRAL native Gram matrix

    [[pi, 1, 0], [1, (1+b)/pi, 0], [0, 0, pi^(ell+1)*c]].

Its good-BONG valuations are the common shift (1,-1,ell+1). A common scalar
scaling leaves every binary group and word-length question unchanged.
For a valid endpoint (x,z), use instead

    [[pi*x, x, 0], [x, x*(1+b*z)/pi, 0],
     [0, 0, pi^(ell+1)*c*z]].

Here z lies in U3, so this is integral too. Thus the scan does not mistakenly
treat the fractional orthogonal BONG as an integral orthogonal lattice.
No counterexample was found for which further coordinate realization is needed.

## 4. Artifact and disposition

The isolated script/result are
`audits/controls/ramified_four_word_negative_gap/verify.py` and `result.json`.
They were run by /opt/anaconda3/envs/qsearch-cas/bin/python through the
prescribed /opt/anaconda3/bin/python driver. The previous stable control was
not imported/executed or rewritten; only its exact setup was copied.
Result field PASS records this scoped negative test, not theorem acceptance.

The existing explicit THREE-word falsifier remains valid. This experiment
adds no >4 obstruction and supplies no universal upper bound. The remaining
four-word question over growing ramification requires its independent
all-input argument or a different explicitly authorized falsifier.
