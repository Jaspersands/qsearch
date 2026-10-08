# Known Shallow Sieve As A Nonlinear Cycle, And The Unseen-Prefix Lift Gate

LOCAL DERIVATION / REVIEW PENDING. The shallow algorithm is a coherent
reformulation of the EXISTING sieve, not a new quantum speedup. The lift gate
is scoped to retaining a lower-prefix-only triple partition, not all receivers.

## An Efficient Nonlinear Action Really Exists At One Root Step

In the original even-native integer-secret model, q=3^r, r>=2, write the
actual frequency prefix as F(x) mod3=A*x+B*x^2. Take n+1 disjoint windows
of (n+1)^2 original qutrits. The existing F3 specialization of the
[Ivanyos--Santha diagonal-equation method](https://arxiv.org/abs/1503.09016)
returns one nonempty zero-sum mask m_j in each window, using ONLY B:

    B*m_j^2=B*m_j=0.

Masks are0/1 and disjoint. The input width is M=(n+1)^3; extra original
inputs may be left unchanged. For any original word x, set

    T_j(x)=(A+2*B*diag(x))*m_j.

Choose a deterministic nonzero kernel vector c(x) of the n-by-(n+1)
matrix with columns T_j(x). The implementation chooses the first free
coordinate in exact reduced row echelon form, not a random unstable choice.
Set v(x)=sum_j c_j(x)*m_j and tau(x)=x+v(x) over F3.

The two necessary line conditions hold:

    B*v(x)^2=sum_j c_j(x)^2*B*m_j=0,
    (A+2*B*diag(x))*v(x)=sum_j c_j(x)*T_j(x)=0.

More importantly, EACH T_j is invariant along the selected line:

    T_j(x+t*v(x))-T_j(x)=2*t*c_j(x)*B*m_j=0.

Thus c and v are invariant along it, tau^3=id, and tau has NO fixed word.
The ENTIRE native prefix is preserved. This is not merely a locally found
partner or an independently recomputed direction that changes on its second
application. The policy caches only A,B and disjoint masks, so it cannot read
any high frequency lifts or the secret.

Mask preprocessing is polynomial. Each tau evaluation takes polynomial
finite-field work O(n*M+n^3); standard reversible compute/uncompute yields
a uniform polynomial clean evaluator and its controlled forms from this
explicit algorithm. The host implementation is NOT a native quantum gate
synthesis or an aggregate hardware-error certificate. The canonical three-
cycle construction supplies clean index erasure with constant evaluator
calls, an M-trit uncompressed tag and one qutrit at q/3 per batch. Acceptance
is1 for ALL low matrices, not just selected random instances. Conditional
IID high lifts give the native child-row law; independent children require
fresh independent original batches.

This is the existing even-to-odd, then tangent-kernel sieve with its pointers
kept coherent. It does NOT improve the (n+1)^3 per-step fresh source budget
or remove the full-depth recursive supply cost. Do not claim that every
efficient nonlinear cycle action is missing: what is missing is a costed
FULL-DEPTH polynomial-supply action at q=poly(n).

## Why The Polynomial Explicit-Menu Gate Does Not Exclude This Program

The direction depends on the original word's invariant tangent records,
not merely on a polynomial LIST of public-label directions. If each B_mask
has full rank n, its tangent can independently range over all F3^n as the
word varies. Set the first n tangent columns to the identity and the last
to-c. The first-free kernel rule then returns(c,1) for EVERY c in F3^n.
Consequently the policy can realize at least3^n distinct directions despite
its polynomial description. Disjoint nonempty masks make these directions
distinct. The report calibrates this implication on actual native labels;
it does not assert every guaranteed mask on a random matrix has full rank.
The affine-menu audit remains valid within its original explicit-menu scope.

## Universal Gate For Reusing Cycles At Unseen Higher Prefixes

Consider ANY complete or partial triple partition chosen ONLY from frequency
rows modulo H0=3^e. Its accepted triples have constant H0 prefix, and its
raw low-stage mass is alpha. Take H1=H0*J=3^d, e<=d<r. KEEP the same triples
and accept only those whose original frequency prefixes agree modulo H1.

For each low matrix and accepted tag, the two child rows at root q/H0 are
independent uniform n-vectors, by the pointed unit-minor/high-lift argument.
The new acceptance condition is that BOTH rows vanish modulo J. Therefore

    Pr[higher-prefix match | low matrix, accepted tag]=J^(-2*n),
    E[raw higher-prefix mass]=E[alpha]*J^(-2*n).

This is exact under the original IID high-lift law, not a fitted exponent.
It applies to the cheap shallow action irrespective of its implicit direction
count. At e=1 and d=r-1, the survival factor is3^(-2*n*(r-2)); merely testing
and postselecting the old orbits at all remaining roots loses exponential
supply. Conditional residual child rows are uniform at root q/H1, but that
correct conditional law cannot erase the success cost. Each actual accepted
batch produces ONE child, not every possible successful tag.

Scope: changing the cycle policy using the higher labels, fresh sequential
root-lowering, knowing and correcting secret digits, interference between
orbits, or a noncommuting/source-state-specific instrument are NOT excluded.
The low-only partition premise is decisive. A fixed full-label instance
need not exhibit the population success rate. In particular, zero high lifts
can make a selected control unusually good. A program allowed to read H1
must establish its new coverage/output law rather than inherit this gate.

## Checks And Next Research Decision

The producer replays all3^8 original coordinates for an n=1 native source,
covering all2,187 tags. That seed is selected to exercise a nonconstant
direction policy, not to estimate the IID population. Larger n=2,3 sources use bounded
word controls; their enormous whole cubes are NOT enumerated or called
empirical scalability evidence. Nine selected physical child branches across
the three controls are checked. Selected tags include a complete TWO-column
conditional high-lift census per coordinate, from which independent-coordinate
products are inferred explicitly. Reusing the first-digit partition at H=9
is tested as a negative control with its real success fraction.

Two requirements now replace the unhelpful generic claim that nonlinear
actions are absent: construct an action using the FULL desired prefix, and
prove polynomial original supply AND polynomial clean evaluation at full
depth. Otherwise demonstrate a costed noncommuting receiver that avoids this
partition model. A faster shallow benchmark or unchanged-cycle postselection
does not resolve the gap. External proof review and novelty checking remain
required; no classical simulation, generic quantum hardness or LWE attack.

```
python theorems/ternary_shallow_kernel_cycle.py --write
node research/certificates/ternary_shallow_kernel_cycle_crosscheck.js
python -m pytest -q tests/test_ternary_shallow_kernel_cycle.py
```
