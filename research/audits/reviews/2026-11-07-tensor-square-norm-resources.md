# Tensor-square support for rational norm equations: source/resource audit

2026-11-07. Independent actual-source/resource review. STATE/TRAPS and the
retained odd-Galois class-generator note were read. Interpreter:
`/opt/anaconda3/bin/python`. No Git, network or API action. This review does
NOT prove the new tensor-square S-support theorem; it is conditional on the
independent core proof of that theorem.

## Verdict

The proposed resource composition is polynomial BIT and supports COMPACT
solution output, conditional on the support theorem and GRH. One source repair
is required: the inspected local primary explicitly supports constant48, not
the proposed constant12. Either provide the actual Bach statement establishing
12 under the intended hypotheses, or use48. No standalone Bach primary was
found in the local source inventory. Using48 changes no asymptotic claim.

Do not claim polynomial height of an expanded solution. A compact power
product is the necessary output model. Handle a=0 separately by returning0;
the S-unit computation concerns a nonzero rational target.

## Actual primary locators

Primary PDF: `research/literature_cache/arxiv_2510_02280v2.pdf`, corrected
24 November2025 version. Parent's exact extraction:
`/tmp/qsearch-sunit-v2.txt`.

- Lines103--107, Theorem1: S-unit computation in compact representation is
  polynomial in n, log absolute maximal-order discriminant, |S| and the
  largest logarithmic prime-ideal norm. It does not require S to generate the
  class group; that generation condition enters the later applications.
- Lines880--949, Proposition2/Algorithm3: deterministic full lattice-basis
  extraction from sufficiently accurate GENERATING vectors, rather than
  accepting merely independent vectors as a basis.
- Lines1576--1594, Theorem5: failure probability mu is explicit, with
  K=O(log d+log(1/mu)+m log a) oracle calls. Item3 guarantees that the good
  underlying vectors generate the ENTIRE dual lattice. Adequate precision,
  basis extraction and compact recovery preserve this complete-generation
  event. Its failure budget is logarithmic in1/mu. Proposition2's unrelated
  use of the symbol mu denotes a shortest-vector lower bound.
- Lines1654--1669, Definition8: choose the constant compact base l=2. Every
  atom is an exact polynomial-size field element, with polynomially many
  levels. Lines1671--1687 explain the rational correction for negative
  valuations. Such correction exponents stay binary, not expanded.
- Lines1769--1781, Proposition7: exact compact recovery in polynomial time.
- Lines1799--1805, Section8.2: under GRH, prime-ideal classes of norm at most
  **48(log|Delta|)^2** generate the ordinary ideal class group. This is the
  inspected source-backed cutoff. Introductory references to norm equations
  do not themselves prove the candidate's new support theorem.

## Tensor discriminants and polynomial support enumeration

The tensor-order estimate is correct. For an integral basis of O_L with trace
Gram matrix G, the tensor basis has Gram matrix G tensor G. Its determinant
is det(G)^(2n). Thus the order A=O_L tensor_Z O_L has absolute discriminant
D_L^(2n), rank n^2, and lies in the maximal product order
B=product_j O_(E_j). The index/discriminant identity gives

    D_L^(2n) = [B:A]^2 * product_j |D_(E_j)|.

Consequently each logarithmic field discriminant is at most2n log D_L. This
argument requires no construction of E_j or B. A prime ideal of norm at most
the chosen cutoff lies above a rational prime no larger than that cutoff.

For an exact integer cutoff, use for example

    B0 = 48 * max(1, 2n*bit_length(D_L))^2.

This safely dominates the natural-log source bound. Degree-one tensor
factors have trivial class group. L=Q can be handled directly. Enumeration
of all rational primes p<=B0 is polynomial NUMERICALLY in n and log D_L,
not just a polynomial-bit description of an exponentially long loop.

Adjoin rational primes dividing D_L and the numerator/denominator of a;
Shor factorization has polynomial BIT cost, with checked outputs and capped
failure budgets. There are at most n prime ideals of L over any rational
prime. Therefore |S| is polynomial and log Norm(P)<=n log p is polynomial,
including possibly large prime divisors of a. The explicit maximal-order
input supplies the necessary multiplication table. Nilradical/reduced-algebra
factorization over F_p computes its primes without assuming a power basis is
p-maximal or enumerating all residues. The source Theorem1 parameters are paid.

## Norm coordinates without expanded units

Let epsilon_j be the returned complete free S-unit generators modulo roots
of unity. Adjoin the KNOWN element -1. This suffices for the rational norm
image of the omitted torsion: if a root of unity is not +/-1, the field has
no real embedding and its rational norm is+1. Norm(-1)=(-1)^n. There is no
need for an unprovided roots-of-unity oracle.

Two valid norm-coordinate implementations are available:

1. Use the returned original valuation coordinates to compute
   v_p Norm(epsilon_j)=sum_(P|p) f_P*v_P(epsilon_j). Compute its sign from
   the compact atoms: the sign of each atom's rational norm is exact, and
   only compact exponent parity matters. Never infer a sign from numerical
   logarithms of a huge expanded unit.
2. Independently compute each SMALL atom's rational norm by its exact
   multiplication determinant. These rational numbers have polynomial bit
   lengths by determinant bounds. Factor their numerators and denominators
   using checked/capped quantum factoring, and aggregate their prime vectors
   with the BINARY compact exponents. Cancellation of prime factors outside
   S is handled algebraically, without expanding any power product. This
   route also gives independent exact verification of positive outputs.

The aggregate exponent vectors have polynomial bit length: multiplying an
integer by2^k adds k bits, and k is polynomial. Include every rational prime
appearing among the atoms when independently verifying a purported norm;
do not discard an unexpected prime merely because it lies outside S.

Solve the valuation equations over Z, together with a MOD2 sign row. In
ordinary integer-matrix form, add one auxiliary variable z and the equation

    sum_j sign_j*e_j - 2z = sign(a).

Do NOT reduce the valuation rows modulo2. Integer HNF/SNF supplies existence
and polynomial-bit solution exponents. A redundant complete generating list
would suffice for this norm-image step; no dimension is inferred from its
length. Incomplete generators do not justify NO.

## Compact output, verification and confidence

Return x=product_j epsilon_j^(e_j), retaining its atoms and binary exponents.
If a single base2 compact encoding is desired, expand each INTEGER exponent
in binary, shift the existing compact levels, and multiply the polynomially
many small atoms assigned to each level. Negative exponents use inverses of
small field atoms, whose matrix-adjugate descriptions have polynomial height.
The number of levels and each resulting atom's bit length remain polynomial.
No exponentially large field element is expanded.

To verify Norm(x)=a, use the exact rational atom norms and their aggregated
prime-exponent/sign vectors. Factoring a polynomial-bit integer is paid;
accepted factor lists can be checked by primality tests and multiplication.
This verifies the compact rational identity, not an expanded integer of
possibly exponential bit length. A positively returned witness can therefore
be checked independently of the S-unit completeness event. A NO answer
remains bounded-error, dependent on that event and the support theorem.

Use Theorem5's adjustable complete-generation error, with all arithmetic and
factoring budgets summed over the polynomially many calls. Deterministic
sufficient-precision extraction/recovery does not require majority-voting
noncanonical bases. Clocks and malformed-output sizes must be capped. The
claimed dependence is polynomial in the explicit field input, n, target
rational bit length, log D_L and log(1/eta).

The strongest matched classical comparator is the same support/linear-algebra
norm algorithm with classical class/S-unit arithmetic and integer factoring.
No classical lower bound or novelty claim follows. The sole unresolved item
in THIS resource audit is the source attribution of constant12 if it is
retained; replacing it by48 closes that item.
