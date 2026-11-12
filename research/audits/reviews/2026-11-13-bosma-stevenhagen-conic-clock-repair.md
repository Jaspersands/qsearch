# Represented quadratic 2-Sylow generators: conic clock repair

2026-11-13. Focused repair of the Lagarias ternary-reduction clock in
Bosma--Stevenhagen. This is not an audit of Simon's full algorithm.

**Result.** The already-audited correctness of Bosma--Stevenhagen, together
with the admitted Cremona--Rusin backend, yields a bounded-clock randomized
polynomial BIT algorithm, with integer-factorization oracle, returning
primitive binary forms representing a complete basis of the STRICT
2-Sylow class group of any nonsquare quadratic-order discriminant D.
Both signs and nonfundamental discriminants are covered. All factoring
requests have polynomial-bit inputs; there are polynomially many requests.
Accepted outputs are exact; randomized exhaustion is ABORT. No fundamental
unit, Pell identity test, ideal-principality oracle, or integral ternary
reduction clock is used.

Source inputs read:

- `audits/api_inputs/2026-11-13-selmer-two-primary/bosma-stevenhagen-primary.md`;
- the adjacent `bosma-stevenhagen-page-transcription.md`, especially printed
  pp.292--297 and308--309;
- `audits/reviews/2026-11-13-quadratic-conic-backend.md`.

The original Bosma--Stevenhagen source is
https://jtnb.centre-mersenne.org/item/10.5802/jtnb.170.pdf. The parent had
already checked its genus-theory, real-case stopping, and halving
correctness; this note supplies the replacement clock. No network, API,
Git, class-group sweep, or new numerical example was used.

## 1. An elementary small representative and class-number bound

For a primitive form Q=(a,b,c) with b^2-4ac=D nonsquare, a and c are
nonzero. Apply an integral shear to make |b|<=|a|. If a^2>|D|, swap
variables by an SL2(Z) matrix, obtaining (c,-b,a). Then

    |c| = |b^2-D|/(4|a|) < |a|/2.

Repeat. There are O(bitlength(initial |a|)) swaps. At termination, shear
once more, so

    0<|a|<=sqrt(|D|),  |b|<=|a|,  |c|<=|D|/2.

For D<0 the positive leading coefficient stays positive. Every operation
is an explicit proper equivalence. The quotient in each shear and the
new coefficients have polynomial bit length in the input. The usual
large real reduced-form cycle is never traversed: this only seeks ONE
small representative, not a canonical representative or equivalence test.

Let M=floor(sqrt(|D|)). There are at most 2M(M+2)<=6|D| possible pairs
(a,b) in this set, and c is forced by D. Every strict ideal class has at
least one such form. Therefore

    h^+(D) <= 6|D|,  log_2 h^+(D)=O(log|D|).

This deliberately weak bound works for nonmaximal orders too and requires
no analytic class-number formula or regulator bound.

After EVERY composition and every halving, apply this reduction. The
stored form coefficients then always have O(log|D|) bits. Standard
noncoprime Gauss composition (source section2) uses fixed-size integer
gcd/formula operations; equivalently multiply the two rank2 invertible
ideal lattices and use HNF with the orientation retained. From two such
small forms this produces polynomial-bit coefficients before reduction.
Neither concordant-prime search nor a class equality test is required.

## 2. Explicit polynomial-height ternary completion

For now D is even, hence divisible by4. Write Q=(a,2b,c) and

    delta = ac-b^2 = -D/4 != 0.

The source Lemma6.1, using its COMPLETE genus characters, constructs
residues u,v modulo |delta| satisfying

    u^2 = c,  v^2 = a,  uv = -b  (mod |delta|).

At each prime power dividing delta, at least one of a,c is a unit by
primitivity. If a is a unit, take v=sqrt(a) and u=-b/v; the case c a
unit is symmetric. The source's genus criterion supplies existence of
the needed roots, including its dyadic conditions. Prime powers are
known from the factorization of D. CRT gives 0<=u,v<|delta|. For
|delta|=1 take u=v=0.

Here are independently derived matrices, not a reconstruction of missing
OCR displays. Put

    B = [ (u^2-c)/delta  (uv+b)/delta  u ]
        [ (uv+b)/delta  (v^2-a)/delta v ]
        [ u             v             delta ],
    A = -adj(B).

All entries of B are integral. Its Schur complement in the last entry
is delta^{-1}*[[-c,b],[b,-a]], so det B=1. Consequently A is integral,
det A=-1, and its upper-left block is [[a,b],[b,c]]. Thus the ternary
form F(x)=x^T A x restricts to Q(x,y) at z=0.

With a small representative Q, entries of B and A are bounded by fixed
powers of |D|. Their bit length is O(log|D|). Because Q is not negative
definite and det A=-1, F has signature(2,1). Source Lemma5.8 guarantees
its isotropy/integral equivalence class; only that correctness statement
is used, not the Lagarias algorithm or its complexity assertion.

## 3. From the admitted conic solver to a small primitive isotropic vector

Diagonalize A by exact rational congruence in dimension3. If a candidate
diagonal pivot is zero, an off-diagonal nonzero entry gives a pivot after
replacing a coordinate vector by a sum of two vectors. Nonsingularity
ensures progress. Only a fixed number of rational operations is required,
and the change of basis and diagonal coefficients have O(log|D|) bits.
Clear their denominators, obtaining nonzero integers A0,B0,C0 in

    A0 U^2 + B0 V^2 + C0 W^2 = 0.

Set x=A0 U, d=-A0 B0, t=-A0 C0. This gives x^2-dV^2=tW^2. Factor d,t
with the PAID oracle, remove their square factors, and apply the admitted
signed-squarefree Cremona--Rusin interface. The split d_squarefree=1
case has the direct rational parametrization already recorded in that
review. Undo square-factor rescaling and the rational diagonalization,
clear three denominators, and divide by the coordinate gcd.

This returns a nonzero primitive integral v with F(v)=0 and polynomial
bit length. The fixed-dimensional transformations preserve polynomial
bit size. The conic is known solvable, so a NO result would indicate a
failed exact check; ABORT remains the controlled randomized outcome.
Verify v^T A v=0 and gcd(v_i)=1 exactly before the next step.

## 4. A primitive isotropic vector gives the REQUIRED integral isometry

This addresses the interface gap: a rational point alone is not the
SL3(Z) transformation needed by source Theorem6.7.

Write <x,y>=x^T A y. As A is unimodular and v primitive, the entries of
Av have gcd1. Extended gcd finds w with <v,w>=1. The saturated lattice
L0=ker(<v,->) has rank2. Compute a basis by integer HNF/SNF, write v in
that basis, and extend v to a basis (v,z) of L0 by a two-coordinate
extended gcd. This is possible because v is primitive in L0. Then
(v,z,w) is a unimodular basis of Z^3.

In this basis the Gram determinant is -F(z). Since det A=-1, F(z)=1.
Replace w by w-<w,z>z. Now <w,z>=0, <v,w>=1, F(v)=0, and F(z)=1.
Put k=F(w). If k is odd, simultaneously replace, using OLD v,z,w,

    z <- z+v,     w <- w-z-v.

This unimodular change preserves all the displayed pairings and changes
k to k-1. Thus k is even. Replace w by w-(k/2)v. Now w is isotropic.
The basis (v,z,-w) has Gram matrix

    [0  0 -1]
    [0  1  0],
    [-1 0  0]

which is Phi=y^2-2xz. Its determinant as a change-of-basis matrix is
plus or minus1; multiplying the entire matrix by -1 fixes the sign if
necessary, without changing the Gram matrix. We have therefore explicitly
constructed M in SL3(Z) with M^T A M=Phi.

All HNF/SNF tasks have dimension at most3. Their inputs, Bezout
coefficients, and the fixed number of subsequent products have polynomial
bit length. This is a polynomial BIT conversion from a primitive conic
point to an INTEGRAL isometry, with no Pell equation or lattice-orbit
search hidden inside it.

## 5. Halving, real signs, and the total number of calls

Apply the source's exact Theorem6.7 to the last row (p,q,r) of M:

    P=(p,2q,2r) if p is odd;
    P=(r,-2q,2p) if p is even.

It gives a primitive discriminant-D form with 2[P]=[Q]. Reduce P
immediately by section1. For D<0, p and r have the same nonzero sign
because 4(q^2-2pr)=D<0. If necessary right-multiply M by
diag(-1,1,-1), an SL3(Z) isometry of Phi, so p,r are positive BEFORE
applying the formula. Thus the output satisfies the positive-form
convention as well. This adjustment has constant bit cost.

The source section3 algorithm uses only the explicit genus-character
matrix to identify the principal genus and decide when enough generators
have been found. It never asks whether a real form represents the
identity class. Keep the redundant initial ambiguous generator in the
real case. One may also keep it in the imaginary case, avoiding the
special imaginary relation entirely: the source's general redundant-
generator argument and stopping proof remain valid.

Let C be the strict 2-Sylow, |C|=2^m, with r generators and exponent2^N.
The source's displayed count(3.6) is m-r in its imaginary-basis version
and m-r-1+N when one redundant initial generator is retained. The latter
also follows by counting j-1 halvings for each final order2^j generator
and at most N-1 halvings of the extra column. In all cases, including
the immediate-stop trivial group,

    number of halvings <= 2m <= 2 log_2(6|D|),
    number of stages <= log_2(6|D|).

There are O(log|D|) stored forms/characters, and only polynomially many
binary linear-algebra operations and compositions. This proves the
clock independently of any unknown real fundamental unit size.

## 6. Odd and nonfundamental discriminants

For odd D, run the construction at E=4D. The source explicitly states
the natural isomorphism C(4D)->C(D) on 2-Sylow subgroups. This also
covers nonfundamental odd D. More explicitly, increasing the order
conductor by2 has class-group extension kernel a quotient of the local
unit quotient at2, of order 2-chi_d(2), which is1 or3; restricting to
totally positive units for strict classes still gives a quotient of that
odd group. The extension map is surjective, so its restriction to the
2-Sylow is an isomorphism. Here d is the FUNDAMENTAL field discriminant.

The represented projection is explicit. For a primitive form (a,b,c)
of discriminant4D, b is even and at least one of a,c is odd. Swap if
needed to make a odd. Choose odd b0 congruent to b/2 modulo a, with
|b0|<=|a|. Then

    (a, b0, (b0^2-D)/(4a))

is a primitive form of discriminant D representing the extended ideal
with its orientation retained. Indeed extending
(a,-b/2+sqrt(D)) from Z[sqrt(D)] to the order of discriminant D gives
(a,(-b0+sqrt(D))/2), since2 is invertible modulo odd a. This projection
is polynomial bit cost. Reduce once more at discriminant D.

For an even nonfundamental discriminant D=f^2 d, run the algorithm on D
ITSELF. Do not replace its genus data by that of d. The source section3
explicitly includes the odd primes dividing f, the full prime powers
p^k||D in its ambiguous forms, and the extra dyadic characters/forms
(notably its v_2(D)>=5 case). These are essential. The completion in
section2 uses all prime powers of delta and remains valid without
squarefreeness. Thus no conductor factor, dyadic contribution, or strict
sign class has been discarded. D=f^2d and its factorizations can be
computed directly from the supplied factorization of D.

## 7. Final resource statement and remaining boundaries

Put E=D for even D and E=4D otherwise, and L=2+bitlength(|E|).
Every stored reduced form has O(L)-bit coefficients. Each halving has
O(L)-bit completion matrices and polynomial-bit conic/isometry outputs;
immediate reduction prevents successive-height growth. There are O(L)
halvings and polynomially many total fixed-dimensional arithmetic and
binary linear-algebra operations. Every additional factoring request is
on an O(L)-bit integer obtained during fixed-dimensional diagonalization
and square-factor removal. There are O(L) such factorizations, up to a
fixed number per halving.

Use the conic review's capped modular-nonresidue searches, also for the
prime-power roots in the completion. Allocate error eta divided by an
explicit polynomial bound on the number of calls. Odd-prime Hensel
lifting and dyadic lifting have polynomial bit clocks. Exact checks of
roots, matrices, and forms prevent an accepted incorrect answer; the
union bound makes ABORT probability at most eta. Hence the total BIT
cost is polynomial in L and log(1/eta), with the integer-factorization
oracle charged explicitly. Output consists of O(L) primitive forms of
O(L)-bit coefficients and their 2-power orders, generating the COMPLETE
strict 2-Sylow. Their associated oriented ideal representatives also
have polynomial-bit bases and norms.

This closes the specific represented-generator source-clock prerequisite.
It does not by itself verify how Simon2006 calls or uses this primitive,
its other dimensions/steps, or Kutas's composition. Those audits remain
separate. No ordinary-class substitution, regulator computation, generic
classical polynomial factoring, novelty, or speedup is claimed. The
parent owns the shared handoff/state update and any admission into Simon's
backend contract.
