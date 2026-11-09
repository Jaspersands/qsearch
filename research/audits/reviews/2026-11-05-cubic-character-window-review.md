# Cubic character central-window attack

Date: 2026-11-05. Focused mathematical derivation and exact finite falsifier.
This is a classical full-table attack, not a quantum result or a classical
poly(log p) algorithm. No novelty or hardness claim is made.

## Contract and conclusion

Let p >= 23 be prime, h=(p-1)/2, and let
Q=X^3+bX^2+cX+d be monic irreducible over F_p. The input is the native
oracle g(a)=chi(Q(a)), a in F_p; the attacker receives no values of Q
itself, derivatives, extension-field queries, or secret coefficients.
Exactly p oracle queries suffice for deterministic reconstruction by
interpolation and a linear system with three unknowns. Its arithmetic
cost is O(M(p) log p + p), where M(p) is polynomial multiplication cost
over F_p, when standard product-tree interpolation is used. This is
quasilinear in p, hence exponential in the input bit length log p.
The finite control uses Sage Lagrange interpolation and does not measure
or claim the fast-interpolation runtime.

The uniform full-rank proof below is independent of the finite control.
The control falsifies a stronger p>=13 claim: 48 of the 728 irreducible
cubics at p=13 have rank two. Every irreducible at p=17 and p=19 has rank
three in the exact exhaustive control. Small-prime recovery cannot be
silently supplied by enumeration: at p=5 there are 40 irreducible cubics
and only 32 possible sign tables, so some inputs are not identifiable.

## Native interpolation and equations

Put F=Q^h. Euler's criterion gives F(a)=g(a), including the interpretation
of +/-1 inside F_p. Let P be the unique interpolant of these p oracle
answers with degree less than p. Since deg F=3h and X^p=X as functions
on F_p, every monomial of F of degree at least p wraps to degree at most
3h-(p-1)=h. Consequently

    [X^j]P = [X^j]F = A_j   for h<j<=p-1.

The exact identity QF'-hQ'F=0, at coefficient X^n, gives

    (n-2-3h)A_(n-2)
      + b(n-1-2h)A_(n-1)
      + c(n-h)A_n + d(n+1)A_(n+1) = 0.

Use n=h+3,...,p-2=2h-1. Every coefficient in these equations lies in
the unaliased window. They give a consistent linear system in b,c,d.
The attack constructs P and this system from the oracle table alone.

## Uniform rank-three proof for p>=23

Suppose a nonzero null perturbation H=uX^2+vX+w exists. Then the
coefficients of HF'-hH'F vanish for n=h+3,...,2h-1. Since h is nonzero
in F_p, the same holds for

    D=Q^(h-1) W,       W=HQ'-H'Q.

If k=deg H<=2, the leading coefficient of W is (3-k) times that of H,
so W is nonzero and deg W=k+2<=4 (p>3). Factor W=X^r V with V(0)!=0,
and write v=deg V, so r+v<=4. Since Q is irreducible, Q(0)!=0. Put

    E=Q^(h-1)V,       N=deg E=3h-3+v=p+e,
    e=h-4+v <= h.

The coefficient gap for E is

    [X^j]E=0 for L=h+3-r <= j <= U=2h-1-r.

Its length is h-3. Moreover E satisfies the exact first-order equation

    A E' = B E,
    A=QV,       B=(h-1)Q'V+QV'.

Let a=deg A=3+v<=7. Here A(0)!=0 and the leading coefficient of B
equals N times the leading coefficient of A. For p>=23 we have h>=11,
and thus the initial gap has length h-3>=8>=a.

Writing E=sum_j e_j X^j, the coefficient of X^(j-1) in the equation
expresses A(0) j e_j in terms of e_(j-1),...,e_(j-a). Starting with
the gap, this propagates zero coefficients upward through j=p-1,
because none of these j vanish modulo p. In the reverse direction, the
coefficient of X^(k+a-1) expresses

    A_a (k-N) e_k

in terms of e_(k+1),...,e_(k+a). Now N=p+e, and
L-e=7-(r+v)>=3. For k=L-1 down through e+1, k-N is nonzero modulo p.
Thus the zeros propagate downward through e+1. We conclude

    E=U_0 + X^p Z,       deg U_0, deg Z <= e <= h < p.

Since Q^(h-1) divides E, Q^(h-2) divides E'. Therefore it also divides

    E' Z - E Z' = U_0' Z - U_0 Z'.

The right side has degree at most 2e-1<=2h-1, whereas
deg Q^(h-2)=3h-6>2h-1. It must vanish. Also Z is nonzero because
deg E=p+e. After removing gcd(U_0,Z), vanishing of this Wronskian
forces both remaining polynomials to have zero derivative: each divides
its own derivative, and a nonzero derivative has smaller degree.
Their degrees are less than p, so they are constants. Hence U_0=cZ
for c in F_p, including c=0, and

    E=Z(X^p+c)=Z(X+c)^p.

Irreducibility of Q implies gcd(Q,X+c)=1. Consequently Q^(h-1)
divides Z, impossible because deg Z<=h<3h-3. This contradiction proves
there was no nonzero H, so the native linear system has rank three.

The proof uses the cubic promise, full p-query interpolation and the
large central coefficient gap. It gives no analogous derivative oracle
from a few character samples, and no poly(log p) reconstruction.

## Exact falsifier

Run from the repository root:

    /opt/anaconda3/envs/qsearch-cas/bin/python research/classical_baselines/cubic_character_window_control.py

Artifact: `research/classical_baselines/cubic_character_window_control.json`.
All arithmetic is exact in Sage. The attack function receives only p and
the character table. The harness separately checks the promised
irreducibility, unaliased coefficients, true-solution consistency, and
exact reconstruction whenever rank is three.

| p | All monic irreducible cubics | Rank 2 | Rank 3 |
|---|---:|---:|---:|
| 13 | 728 | 48 | 680 |
| 17 | 1632 | 0 | 1632 |
| 19 | 2280 | 0 | 2280 |

At p=13, Q=X^3+X^2+X+5 is irreducible and the nullspace contains
H=X^2+4X+9. This refutes uniform rank three at that prime, not
identifiability from its full sign table or every other classical attack.

## Comparator and remaining obligations

The locally supplied Kaluđerović--Kleinjung--Kostić 2020 published source,
Section 4D2, describes a full-p-query cubic time-memory collision attack
with O(p^(3/2)) Legendre-symbol work. The present derivation supplies a
stronger full-table arithmetic upper bound under the stated native
irreducible-cubic promise; historical and modern literature priority is
not established by this review. The source is
`research/audits/sources/legendre_prf/kkk_2020_published.txt`.

Before promoting the rank theorem into repository state, independently
review the gap propagation and Wronskian argument. Any future quantum
comparison must charge the full input oracle model and compare against
this p-query, quasilinear-in-p classical construction, while leaving
the classical poly(log p) question open. The exact scans do not establish
the asymptotic theorem, a speedup, or classical hardness.
