# Joint norm valuations: exact ordered-rectangle cokernel

2026-11-13. Independent all-r proof. Fresh STATE/TRAPS and
`SIMULTANEOUS_NORM_SUPPORT.md` were read, together with the stable Sage
`controls/simultaneous_norm/rectangle_kernel.py/.json`. The r=2,3,4
receipts are finite checks only; the proof below does not extrapolate them.
No additional control, network, API, Git or live report was used.

**Disposition:** for equal single r-cycle local types, EVERY r>=2, the
ordered-rectangle transfer image has exact cokernel Z/r in the joint
valuation kernel. It fails integral generation, although its rational
span is correct. The r=2 missing direction is realized by an explicit
element with both relative norms one. This refutes this transfer-based
generation claim, not simultaneous norm solvability or all norm algorithms.

## 1. Local coordinates and norm multiplicities

At an unramified prime identify X=Y=Z/r, with Frobenius adding one to every
coordinate. The pair orbits in X times Y are
    Z_c={(x,x+c): x in Z/r}, c in Z/r,
all of length r. A valuation vector z=(z_c) records the valuation at the
corresponding L-prime, equivalently its COMMON PER-POINT orbit coefficient.

There is one A-prime and one B-prime, each with residue degree r, and each
L-prime also has residue degree r. The local norm-valuation formula
    v_P(N_(L/A) x)=sum_(Q above P) f(Q/P) v_Q(x)
therefore has coefficient f(Q/P)=r/r=1 at every column. The same holds for B.
Thus both norm rows are (1,...,1), and their saturated joint kernel is
    I={z in Z^r: sum_c z_c=0}.
Identify Z^r with R=Z[t]/(t^r-1), sending z to sum_c z_c t^c. Then I is the
augmentation ideal, and I=(t-1)R. Orbit TOTALS would multiply coordinates
by r and give a different, incorrect integral calculation.

## 2. Exact image, with signs and local transfers checked

Take an ordered quadruple (x0,x1,y0,y1) and its diagonal Frobenius orbit.
That orbit has length r. Each of its four projections onto a pair orbit
is a bijection, so the corresponding local norm has residue-degree factor
one, not r. Sum its signed rectangles
    +(x0,y0) -(x0,y1) -(x1,y0) +(x1,y1).
With c=y0-x0, a=x0-x1 and b=y1-y0, the resulting per-point column is

    t^c-t^(c+b)-t^(c+a)+t^(c+a+b)
       =t^c(1-t^a)(1-t^b).                              (1)

Every triple c,a,b occurs: choose x0=0, x1=-a, y0=c, y1=c+b.
Every column is in I^2. Conversely a=b=1 gives t^c(1-t)^2 for every c.
These generate (1-t)^2R=I^2 as an integer lattice. Hence the image is
EXACTLY I^2, not merely a sublattice with an experimentally guessed index.

The signs also preserve both global norms: for a field factor C of
A tensor A tensor B tensor B, compose each of its four C-to-L norms
with L-to-A. For fixed A-slot, the two resulting C-to-A norms agree by
transitivity and have opposite signs. They cancel. Grouping by B-slot
proves the second norm is one. Repeated embeddings cause no problem.
At the present local type, each C-prime orbit has length r, giving precisely
the multiplicities already used in (1).

## 3. The quotient, not just its rank or index

The homomorphism
    chi:I -> Z/r,  chi(sum_c z_c t^c)=sum_c c z_c mod r
is well defined and kills I^2. Indeed it is derivative evaluation at t=1
modulo r; differentiating a multiple of t^r-1 changes the value by a multiple
of r, while the derivative of a product of two augmentation-zero elements
is zero. It is onto since chi(t-1)=1.

Conversely, t^c-1 is congruent to c(t-1) modulo I^2. Thus every element of I
is congruent to chi's integer lift times t-1. The relation t^r-1=0 gives
r(t-1) in I^2, because 1+t+...+t^(r-1)-r lies in I. Surjectivity of chi
shows there is no smaller relation. Therefore
    I/I^2 is isomorphic to Z/r,
and (1,-1,0,...,0)=1-t has exact order r in this quotient. In particular
there is no free cokernel part and the image index is exactly r for all r>=2.

## 4. Arithmetic realization of the missing r=2 direction

Let A=Q(sqrt2), B=Q(sqrt3), L=Q(sqrt2,sqrt3), and K=Q(sqrt6).
The prime 5 is unramified, inert in A and B, and split in K because 6=1
modulo 5. In L its Frobenius flips both sqrt2 and sqrt3, so there are exactly
two primes, each of residue degree two: the equal-2-cycle local type above.

In O_K=Z[sqrt6], the two primes are p_+=(5,sqrt6-1) and p_-=(5,sqrt6+1).
Norm_(K/Q)(1+sqrt6)=Norm_(K/Q)(1-sqrt6)=-5. Thus
    x=(1+sqrt6)/(1-sqrt6)
has valuations +1 at p_- and -1 at p_+, and no other finite valuations.
Each p_+/- is unramified and inert in L/K, since 2 is nonsquare in F_5.
The ramification index is one, so these valuations remain (+1,-1) at the
two L-primes. Each nontrivial relative involution for L/A or L/B sends
sqrt6 to -sqrt6 and x to x^-1. Hence BOTH relative norms of x are exactly one.

This exhibits actual principal joint-kernel data outside the rectangle image
2I. It does not say that a chosen allowed support excludes 5, that the norm
equations lack a solution, or that every support construction fails. Taking
the saturation I in place of I^2 would require a separately justified global
multiplicative operation; an uncharged root is not supplied by the lattice
calculation. No norm-hardness or polynomial-algorithm impossibility follows.
