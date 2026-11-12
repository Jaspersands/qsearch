# Cyclic content projections: certificate without a general success clock

2026-11-13. Full completed Claude report
`audits/claude_runs/2026-11-13-content-cyclic/response.md` parent-read.
The general growing-degree success guarantee remains OPEN. No new
subcase sweep, Kummer subsystem or full relation claim is justified.

For a nonzero native implicit integer norm numerator P=det A_i, the
reviewed formal bound ||P||_1<=V has polynomial log V. Use Kronecker
weights(1,B,...,B^(s-1)), where B exceeds every per-variable degree of P.
The substituted P_w is nonzero and its exponent BIT lengths remain
polynomial. Reducing modulo T^q-1 only merges coefficients, so each
integer projection coefficient C has |C|<=V and cont(P)|C. ANY nonzero
C is therefore a sound polynomial-bit content-support cover.

For polynomial numerical q this projection is computable without
expanding P: evaluate the formal common-denominator/companion-power
circuits for A_i in (Z/ell)[T]/(T^q-1), take a division-free determinant,
and CRT its q coefficients using product modulus>2V. All dimensions,
ring operations and bit lengths are polynomial. This works over rings
with zero divisors. Factoring a nonzero C is separately charged.
An optional mod-p PIT filter can discard provably extraneous primes;
false zero tests only keep extra primes, not lose genuine support.

The report's alternative assertion that clearing arbitrary native
rational coefficients leaves EXPLICIT SPARSE Sylvester entries is
incorrect: different denominator products can expand exponentially.
Use the native formal numerator circuits and their already proved V
instead. This repair pays computation of a CHOSEN cyclic projection,
not the missing probability of finding a nonzero one.

For prime q, P_w mod(T^q-1)=0 iff both P_w(1)=0 and Phi_q divides P_w.
If P_w has at most K monomials and q>K, vanishing at a primitive qth
root forces a collision between two distinct support exponents modulo q.
A union bound on prime divisors of their differences gives polynomial
q in K and exponent BIT length. K can be exponential in growing delta;
fixed-delta success is already covered by SPARSE_CYCLOTOMIC_FIXED_DEGREE.
The elementary T^M-1 and products-of-binomials examples defeat undersized
windows, not every polynomial window. They are not general falsifiers.

The report's radical-field positive family is already covered by the
retained monomial-Kummer work and supplies no new general mechanism.
Its probability bound also contains an unnecessary unnormalized term
for primes dividing delta: choosing q>delta removes those primes outright.
Do not adopt its stronger necessary features for all counterexamples;
fixed algebraic coefficients need their own disjointness analysis, and
a universal single counterfamily is stronger than needed to refute any
particular proposed polynomial window. No such family was constructed.

Two stronger consequences remain CONDITIONAL, not new algorithms:
(1) a polynomial-size quotient hitting the PRODUCT of protected norms
and denominators would permit direct finite-Q-algebra specialization
and LS intersection, bypassing finite-prime support; separate projections
for separate norms do not supply that common component;
(2) a polynomial Taylor multiplicity bound at a small-order root of
unity yields a nonzero local coefficient, whose norm supplies a support
integer. The independent OpenAI Taylor task addresses its actual
growing-degree hypothesis; no low-total-degree/trinomial theorem closes it.

Disposition: nonzero-projection certificate and its bit clock accepted
with the denominator-circuit repair; general success/open-bound claim
retained; no hardness, classical match or asymptotic inference from the
proposed small-q scans. Keep complete support and fullRel gates false.

## Native Taylor multiplicity: open after independent attack

The full8226byte report in audits/openai_runs/2026-11-13-native-resultant-
multiplicity/response.md was parent-read. It gives neither a polynomial bound
nor a superpolynomial counterfamily. For monic p of Y-degree delta and
q of smaller degree, R=Res_Y(p,q)!=0, ord_(T=1) R equals the length of
C[[X]][Y]/(p(1+X,Y),q(1+X,Y)), i.e. the sum of local intersection numbers.
Monicity excludes points at Y infinity. Pure Y factors can be removed and
axis roots translated by a small integer with at most delta+1 term growth.
The remaining mixed-degree fewnomial intersection bound stays UNPROVED.

The direct support bound
K=binom(s_p+deg_Y(q)-1,deg_Y(q))*binom(s_q+delta-1,delta)
and the Vandermonde bound ord R<=K-1 can be exponential in delta.
Wronskians leave an unpaid numerator multiplicity; numerical total-degree
bounds and trinomial theorems do not close this gap. The cited Koiran--Skomra
constant is5/2, not the report's OCR rendering52; no stronger scope is adopted.
Conditional on a polynomial multiplicity cap M, truncated-ring determinant
computation pays coefficient bits using |[X^j]R(1+X)|<=H(nN)^j for j<=M.
Native factored denominators still need their own zero estimate: expanding
products can be exponential. Kronecker substitution preserves nonzero norm
and content, but need not preserve the original field irreducibility.

No further subfamily scan is selected. Both general cyclic and Taylor
success clocks remain OPEN; park this support route until a new constructive
idea pays one of them. Unknown bounds are not hardness results.
