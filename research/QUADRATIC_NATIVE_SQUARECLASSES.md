# Complete quadratic squareclasses by rational conics

2026-11-13. REVIEWED WRITTEN classical polynomial-bit algorithm with the
native rational bad-prime factorization supplied. No full unit group,
class group, integral Pell solution or extra factorization is used.

## Exact contract and result

Let K=Q(sqrt(d)), with nonzero squarefree d!=1. Let S_Q contain 2 and
every prime dividing disc(K), and let S contain ALL primes above S_Q.
Given d and the factorizations of d and S_Q, output an explicit basis of
K(S,2), together with evaluable native elements, in polynomial bit time.
Accepted answers are exact; bounded random nonresidue searches may ABORT
with total probability at most eta. The clock is polynomial in the input
length and log(1/eta). Native quadratic defining polynomials reduce to
this presentation after factoring their discriminants.

Put U=Q(S_Q,2)=span(-1, primes in S_Q), and let V be its subspace of
global norms from K. The exact sequence is

    0 -> U/<d> -> K(S,2) --Norm--> V -> 0.

Thus dim K(S,2)=|S_Q|+dim V. Compute V by the rational Hilbert-symbol
matrix (a,d)_v, v in S_Q union infinity. Hasse--Minkowski supplies the
local-global criterion; all other places have trivial symbols.

For each basis vector represented by a signed squarefree integer a,
solve X^2-dY^2=aZ^2 and divide the integer triple by its gcd. Use
beta=X+Y sqrt(d), NOT beta/Z, as the squareclass representative.
No factoring of Z or Norm(beta) is needed. Adjoin the images of a
rational basis of U/<d>.

## Why this is complete

The rational restriction kernel is <d>. If Norm(alpha)=c^2 and alpha
is not the rational element -c, then

    (alpha+c)^2=(Tr(alpha)+2c) alpha.

The rational factor has even valuation outside S_Q, since those primes
are unramified; hence the norm kernel is the image of U/<d>.

For surjectivity, choose the primitive conic solution above. If p is
outside S_Q then p does not divide 2ad. At an inert prime, divisibility
of beta implies p divides both X,Y, hence Z, a contradiction. At a split
prime, the two primes above p cannot both divide beta for the same reason.
Their valuation sum is 2v_p(Z), so each valuation is even. Therefore beta
belongs to K(S,2), with norm squareclass a. Independent norm images and
the rational kernel prove that the returned generators form a basis.

The full independent proof is
audits/reviews/2026-11-13-quadratic-norm-squareclasses.md (240 lines).
The separate paid OpenAI quadratic-classical report independently found
the same primitive-numerator route; its conic complexity citation is
superseded by the checked backend below.

## Paid conic backend and source repairs

Cremona--Rusin, Efficient Solution of Rational Conics, actual pp.3--4,
10,15--17: https://johncremona.github.io/papers/conics.pdf.
The full 271-line proof/source audit is
audits/reviews/2026-11-13-quadratic-conic-backend.md; parent read in full.

With h=gcd(|d|,|a|), reduce to pairwise coprime squarefree coefficients
h,-d/h,-a/h. All factors are inherited. Certificates are modular square
roots, paid with finite Tonelli--Shanks nonresidue searches and CRT.
Use the exact certificate congruence lattice and its index-two quadratic
parity kernel. Weighted integer-Gram LLL in rank three plus thirteen
vectors finds a shortest vector. The Gauss equality case must be removed:
when the two positive coefficients are both 1, use Gaussian gcd; for all
other inputs the shortest norm is STRICTLY below twice |abc| and its
indefinite quadratic value is zero. The audit proves strictness by an
integer sublattice-index contradiction, without assuming an unqualified
shortest-vector theorem. The printed lattice basis has a sign mismatch;
use the corrected sign or the exact HNF congruence kernel.

Every output coordinate has O(input length) bits. A deliberately loose
schoolbook bound is O((B+1)^8(1+log(1/eta))) per conic with factorizations
supplied. No additional integer factorization occurs. This supplies the
previously missing discovery clock, not merely a certificate check.

## Consequences, controls, and boundaries

Combine with LOCAL_KUMMER_ALL_PRIMES.md: for every native odd-degree monic
squarefree f whose irreducible factors have degree at most two, exact
Selmer dimension has a polynomial classical remainder after factoring
2disc(f). Shor factoring gives an unconditional quantum composition, but
no new unit-computation advantage survives on this restricted family.
Adding the retained cubic factors uses their separate unconditional
quantum source; this note does not dequantize them.

The exact d=34 control uses (X,Y,Z)=(3,1,5), beta=3+sqrt(34), norm=-25.
Its valuations outside {2,17} are even although integral negative Pell
is insoluble. This falsifies the Pell prerequisite, not an asymptotic claim.
The hypotheses on S are essential: missing a ramified prime or including
only one prime above a selected split prime invalidates the argument.
Global units, integral norm-one generators, arbitrary base fields, and
general classical Selmer algorithms are not supplied by this result.

Next hard question: which part survives for a quadratic extension of a
nonrational base? Local norm tests alone do not pay relative conic solving,
primitive ideal coordinates, completeness, or compact localization.
