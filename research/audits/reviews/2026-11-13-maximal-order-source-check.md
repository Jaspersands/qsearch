# Maximal-order backend: Buchmann--Lenstra primary-source check

Status: stable focused source review. The actual theorem and proof support a
deterministic polynomial-bit maximal-order algorithm GIVEN the radical (hence
also given the complete prime factorization) of the discriminant of a known
order. The polynomial is uniform in the expanded field degree. This verifies
one native arithmetic backend, not the positive total tower-algorithm claim
in the paid batched-compiler report.

## 1. Retained primary authority

J. A. Buchmann and H. W. Lenstra, Jr., *Approximatting rings of integers in
number fields*, Journal de Theorie des Nombres de Bordeaux 6(2), 1994,
pp221--260. Successful primary URL supplied by the parent:
<https://www.numdam.org/item/JTNB_1994__6_2_221_0.pdf>.

Local files, explicitly confirmed stable before this review:

- `research/audits/sources/2026-11-13-tower-native-composition/buchmann_lenstra.pdf`
- `research/audits/sources/2026-11-13-tower-native-composition/buchmann_lenstra.txt`
- `research/audits/sources/2026-11-13-tower-native-composition/buchmann_lenstra.source.json`

Only retained local material was read; no network request was made. Locators
below count physical LF newlines in this text, including form-feed page-break
lines. The claim is checked against theorem statements and their proof, not
the abstract. Missing OCR in ancillary displayed formulas is not needed to
interpret the fully legible statements and reduction below.

## 2. Exact theorem being imported

Theorem1.2, printed p225, text LF256--258, takes a number field K, an order
A in K, and a SQUAREFREE positive integer m. It produces an overorder B of
A maximal at m in polynomial time. The preceding definition at LF253--254
means

    gcd(m, [O_K:B]) = 1.

This theorem by itself is a local-maximality statement for the primes
specified by m, not a promise that any arbitrary m produces O_K.
The discussion immediately following it, LF260--263, explains that it
suffices to include every prime p for which p^2 divides the order discriminant.

The explicit maximal-order reduction is in the proof of Theorem1.3,
printed p254, text LF1770--1775: construct an order A; set m to the largest
squarefree divisor of its discriminant; apply Theorem1.2. The resulting B
is maximal at the discriminant of A and therefore is O_K. Theorem1.3 itself
is at LF266--273; the order-discriminant implication is also stated at
LF277--280. This is the relevant direction of that theorem's equivalence;
no converse hardness interpretation is needed here.

Write delta_A=abs(disc(A))>0. The required integer is

    m = rad(delta_A) = product_{p dividing delta_A} p.

Here “largest squarefree divisor” means the radical, including primes whose
valuation in delta_A is EVEN. It does NOT mean the squarefree integer in a
decomposition delta_A = square * squarefree_part. For example, rad(12)=6,
whereas that squarefree_part is3. Substituting the latter would omit the
prime2 and can miss a nonmaximality prime. Complete factorization of delta_A
immediately computes the correct m by multiplication of its distinct primes.
Its bit length is at most the bit length of delta_A.

Why this proves global maximality: for any overorder B of A,

    disc(A) = disc(B) * [B:A]^2,
    disc(B) = disc(O_K) * [O_K:B]^2.

Every prime in [O_K:B] therefore divides delta_A; being maximal at all
primes of rad(delta_A) forces [O_K:B]=1. One can alternatively use only the
primes occurring at least twice in delta_A, as the source observes. Taking
the full radical is the simpler safe interface. The trivial case delta_A=1
already has A=O_K and needs no local processing.

The discriminant to factor can be that of the GIVEN/CONSTRUCTED ORDER.
No prior knowledge of the unknown field discriminant disc(O_K) is required.
Theorem1.4, LF291--294, provides another interface using rad(disc(O_K)),
but that stronger input is unnecessary here. Supplying only the numerical
field discriminant without its radical is not the stated Theorem1.4 input.

## 3. Proof algorithm and uniform degree/bit clock

This is not a fixed-degree assertion. The following actual source steps
establish the uniform expanded-input interpretation.

1. Section5 begins at LF1134; LF1136 says its algorithms and those of
   Section6 are deterministic. Section5.7, LF1312--1328, represents an order
   by its degree n and n^3 integral multiplication constants in a Z-basis;
   ideals use integer lattices/Hermite normal form. Thus n is part of the
   input, rather than an unspecified fixed constant.
2. Section5.9, LF1353--1360, explicitly bounds the encoding length of EVERY
   overorder of A polynomially in the encoding length of A. The index bound
   and canonical fractional-ideal representation control intermediate
   numerators/denominators; a sequence of order enlargements does not silently
   acquire unbounded coordinate size.
3. Algorithm6.1, LF1370--1385, and Proposition6.2, LF1386--1414, give the
   prime-local maximal-overorder routine. Its linear algebra is in dimension
   n; each proper enlargement reduces the discriminant by at least p^2,
   so its number of iterations is polynomial in log(delta_A) and log p.
   The exact index-prime-power guarantee is part of Proposition6.2.
4. The general squarefree-input routine is Algorithm6.6, LF1566--1605,
   with Theorem6.7 at LF1607--1641. The proof explicitly invokes Section5.9
   for a polynomial bound on every order representation, bounds the auxiliary
   integers by m, and notes that its small-prime loop has at most n candidates.
   Successful calls are bounded by distinct prime factors of m; unsuccessful
   refinements are bounded by their total multiplicity, O(log m).
5. The proof of Theorem1.2 at LF1726--1727 applies Theorem6.7: every divisor
   of squarefree m is squarefree, so the resulting overorder is maximal at m.
   The proof of Theorem1.3 at LF1770--1775 then imports this routine with
   m=rad(delta_A). These are explicit polynomial-time reductions, not a
   heuristic assumption that a candidate order is probably maximal.

For complete given factorization there is an even more direct implementation:
process each distinct prime dividing delta_A with Algorithm6.1. At most
log2(delta_A) distinct primes occur; enlarging an order preserves maximality
at already processed primes. All intermediate orders remain overorders of
original A, so Section5.9 gives the same uniform encoding bound. This route
avoids requiring any factorization of a new intermediate discriminant during
this single maximal-order computation. The cost of obtaining the original
factorization remains a separately charged resource.

The “best guess” approximation of Theorem1.1, LF236--247, is NOT the
algorithmic certificate being used here. Without the supplied radical or
factorization, an unproved squarefreeness guess need not produce O_K.

## 4. Native expanded-table input and output coordinates

The source theorem assumes a field and an ORDER, not a compact black box.
For an explicitly expanded rational multiplication table, obtaining an
initial order does not require a maximal-order or class-group oracle.
Here is a direct polynomial-size conversion to its stated input model.

First choose a rational basis e1=1,e2,...,en by exact linear algebra. Let c
be a positive common denominator of ALL rational structure constants in
this basis. Then

    A = Z*1 + sum_{i=2}^n Z*(c*e_i)

is closed under multiplication: coefficients of c*e_k are c times rational
structure constants, and the coefficient of1 is c^2 times such a constant.
They are integers. This unital finite free subring is an order in K. A
product of the input denominators gives a permissible c of polynomial bit
length; no minimal denominator or integer factorization is needed for c.
The basis change and its n^3 integral structure constants have polynomial
encoding length in the expanded input.

Compute disc(A) by the trace pairing/determinant in that basis, factor its
absolute value using the explicitly charged integer-factoring resource,
form its radical, and invoke the theorem. Determinants, trace matrices and
basis transformations have polynomial bit length. The source represents the
resulting maximal order as a fractional lattice over original A; Section5.9
and the explicitly known change from A to the input field basis therefore
also pay for expanded maximal-order coordinates in the original basis.
This conversion assumes the input really is the promised number field with
its explicit identity/table; it does not recognize arbitrary invalid towers.

## 5. Disposition and limits

Accepted source interface: for EVERY expanded-degree n number field with a
known explicit order A, complete integer factorization of polynomial-bit
abs(disc(A)) suffices for deterministic polynomial-bit computation of O_K,
with expanded basis coordinates. This arithmetic step is unconditional
once that factorization is supplied; it does not consume the gluing ERH
hypothesis. It needs the radical/order-discriminant support, not a unit
basis, class group, fundamental units, field discriminant advice, or fixed n.

Still charged: construction/bit sizes of the field/table and chosen order,
the actual integer factorization, and every later arithmetic or recursive
call made by a larger tower algorithm. This source does not prove that a
particular tower composition makes only polynomially many such calls or
that all later data remain polynomial-size. It supplies neither conic
solvers nor complete supported squareclasses nor their coupled recurrence.
The positive batched-native-compiler algorithm claim remains UNVERIFIED
by this backend review. No implementation, total tower theorem, GRH-free
replacement for gluing, novelty, hardness or speedup is asserted.

This source arrived AFTER the 31-artifact two-job ledger was frozen. Its
files and this review were deliberately not added to or repinned into that
checkpoint. No tests, API call, network request or Git action was performed.
