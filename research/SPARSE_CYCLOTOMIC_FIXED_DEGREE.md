# Full sparse function-field relations: every fixed degree is classical

2026-11-13. REVIEWED WRITTEN bounded-error classical polynomial SPARSE-BIT
algorithm for every FIXED extension degree delta. Growing s variables,
k original atoms, coefficient bits and binary exponents are permitted.
Time is polynomial in native bits and log(1/eta); the polynomial degree
depends on delta. No factoring oracle, constant-field/embedding advice,
quantum operation, full implementation, novelty or separation claim.
Full250line independent proof and the139line paid report parent-read.

Native input is F=Q(T_1,...,T_s)[Y]/monic irreducible f of degree delta,
and nonzero original u_i in the Y basis with explicit sparse rational-
function coefficients. Return the COMPLETE integer relation lattice
Rel={e:product u_i^e=1}, including torsion. Existing generalAlg algorithm
computes Alg={e:product u_i^e algebraic overQ}; it is reused unchanged.

## Mechanism and resource proof

For a nonzero rational polynomial P with K distinct monomials, take a
prime q>K for which no exponent-difference vector vanishes modulo q.
Uniform a in F_q^s makes any exponent-dot-product collision with
probability1/q. Off collisions, P(zeta_q^a) is a polynomial in zeta_q
with fewer than q nonzero terms and degree<=q-1, so cannot be a nonzero
multiple of Phi_q=1+X+...+X^(q-1). Failure<=binom(K,2)/q.

For a protected list, put Pi=sum binom(K_P,2); suppose exponent
coordinates have absolute value<2^b. A chosen nonzero difference
coordinate has <(b+1)/log2X prime divisors>=X. The retained explicit prime
interval bound gives total bad-prime plus collision probability
 <2.2 Pi(b+1)/X <1/2
for X>=max(21,maxK+1,5Pi(b+1)), uniform prime q in[X,2X]. Coefficients
are characteristicZERO, not reduced modulo q; no content exclusion.

Let m>=2 bound each input polynomial's support. Clearing each f/u_i
coefficient denominator uses <=delta factors. Each Sylvester entry then
has <=m^delta terms. The NONZERO cleared norm polynomial has support
 K_delta=(2delta-1)! m^[delta(2delta-1)],
and exponent coordinates gain <=ceil(log2(2delta²)) bits. Protect the
L original denominator polynomials separately and each of k cleared
norms, using Pi<=Lm²+kK_delta². For FIXEDdelta the required NUMERICAL q
is polynomial in native bits. These support bounds are proof-only;
neither determinant support nor all norms' product is expanded.

Evaluate original sparse coefficients by reducing exponents modulo q.
All coordinates/inverses in Q(zeta_q), degreeq-1, have polynomial bit
height. Reject zero coefficient denominators. Let r=rad(f_t); successively
remove gcd(r,u_i(t)) to obtain the largest squarefree factor g on which
ALL original atoms are units. Accept iff degg>0 and form
 E=Q(zeta_q)[Y]/g.
No factorization of f_t needed. The sufficient no-normzero event has
probability>1/2; exact partial-component acceptance can only do better.
Discriminant/separable-fibre advice is unnecessary.

Let A=Q[T,Den^-1,Y]/(f)[u_i^-1]. Its algebraic-overQ subring C_A is a
FIELD, since every nonzero algebraic element's inverse is its rational
polynomial. Accepted specialization A->E restricts injectively to C_A
because E is nonzero. Thus for EVERY accepted point, exactly
 Rel_F=Alg intersect Rel_E(original u_i(t)).
The actual Lenstra--Silverberg1509.08843 Theorem1.11 applies to this
explicit finite commutative Q-algebra of dimension<=delta(q-1).
It returns all relations, including finite torsion. Integer kernel/HNF
intersection preserves the full lattice, not just its rational span.
Never expand Alg-basis powers, which can have huge heights.

Keep X independent of eta and repeat ceil(log2(4/eta)) point trials.
Since X is polynomial for fixeddelta, even enumerating primes in[X,2X]
is permitted. Cap binary rejection sampling and account for exhaustion.
Allocate eta/2 to the retained generalAlg bounded-error step and eta/2
to point/sampling failures. Whole algorithm is bounded-error, NOT LasVegas,
although point acceptance and LS are exact. No polynomial-in1/eta field
size is substituted for the claimed logarithmic-confidence clock.

## Material report corrections and falsifier

The paid report's general-case 'exact resultant criterion' is FALSE for
partial-component acceptance. With any oddprimeq,
 f=Y²-T^q, u=Y-1,
the native f is irreducible, but at EVERY T=zeta_q^a one may retain Y=-1
and u=-2. Norm(u)=1-T^q vanishes on the whole torsiongrid. Thus zero
norm means some component is killed, not every component. This does not
affect the positive proof, which only uses normnonzero as SUFFICIENT.
Also Q[(Z/q)^s] becomes a product of copies of C only after basechange.

A generic polynomial-order cyclotomic hitting theorem for arbitrary
sparse determinants would conditionally derandomize symbolic determinant
identity testing (actual Oki Remark12/Kronecker substitution). This is
not impossibility or hardness, and no general-determinant embedding into
the native norm problem is assumed. The growingdelta case remains OPEN:
K_delta is then generally exponential. No further fixeddegree extension,
finite sweep or new implementation is queued.

Evidence: audits/reviews/2026-11-13-sparse-cyclotomic-fixed-degree.md;
paid bundle audits/claude_runs/2026-11-13-sparse-cyclotomic/;
primary scope https://arxiv.org/pdf/1509.08843 and
https://drops.dagstuhl.de/opus/volltexte/2020/12496/pdf/LIPIcs-ICALP-2020-89.pdf.
Existing full quantum/generalAlg notes remain valid at their original scope.
