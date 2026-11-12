# Sparse native constants: finite places and the support gate

2026-11-13. The full completed advisory report
`audits/openai_runs/2026-11-13-sparse-vertical/response.md` was parent-read.
The support lemma, falsifiers, pencil reduction and torsion step below
were checked directly. The complete378line independent clock review was parent-read and checked:
`audits/reviews/2026-11-13-sparse-known-prime-clock.md`. The supplied-prime
CONSTANT-RESTRICTION compiler is now reviewed written correct-or-ABORT. No full growing-degree classical
relation algorithm is established.

## Native support, with discovery unpaid

Use the unchanged native model and formal bounds of
GENERAL_SPARSE_CONSTANTS_ATTACK.md: M(u_i)=A_i/D^delta,
H_i=det A_i, ||D||_1,||H_i||_1<=2^B for computable polynomial B.
The proof-only set of relevant rational primes is contained in

 Supp(cont(D) product_i cont(H_i)).

At a prime outside cont(D), all monic f coefficients and original atoms
are integral for the p-Gauss valuation, so every extended valuation of
u_i is nonnegative. If cont(H_i) is also prime to p, the norm valuation
is zero. Its positive weighted sum of the extended valuations then
forces every one to vanish. Restricting to algebraic constants covers
all their finite places. There are only polynomially many possible
primes and at most delta rows per prime; this is an OUTPUT-SIZE bound.

The missing operation is to find explicit nonzero integers C_i, of
polynomial BIT length, with cont(H_i)|C_i. Their factorizations, together
with cont(D), cover all needed primes, and extra primes are harmless.
Any nonzero coefficient would work, but extracting one is not paid by
modular PIT. The least representative of H_i(t) modulo m need not be
divisible by cont(H_i). Factoring is a separately charged oracle here;
prime-labelled support itself factors arbitrary integers on inputs u=N.
A successful support compiler would therefore at most establish a
classical FACTORING-ORACLE counterpart via this route.

## Supplied-prime constant valuations: reviewed written polynomial clock

Input includes a prime p and a CORRECT integer basis of Alg. No constant
field, order, local factors or aligned places are supplied. Every accepted
regular specialization gives all required constant valuation rows; only
completion needs randomness. The explicit precision schedule and proof are
in the378line independent review, Sections3--7.

Let B0=2+ceil(log2 max(H,V)), Delta=delta e0, eps=eta/8. Work in an
unramified degree-r p-adic coefficient ring with residue size q=p^r>
max(16(delta+1)^2,(k+2)(Delta+1)/eps). Protect ONLY D,det J,det A_i.
Schwartz--Zippel after proof-only p-content removal ensures all valuation
caps pass with high probability, without extracting contents. Set
 Ccap=(delta^2+1)(B0+1), P0=2 Ccap+20,
 Kraw=2 Ccap+2B0+24, Qfin=Ccap+4.
These are BASE-p digits. Binary sparse powering pays original exponent
bits; no huge-height rational point is constructed. Check visible denominator,
discriminant and original-atom norm valuations. Scale X=p^B0 Y and
z_i=p^(delta B0)u_i to integrality.

Normalize the order A using I=rad(pA) and its multiplier ring (I:I).
In an adapted I basis, multiplication has coefficients
p^(eps_j-eps_l)c_ij^l with eps_j in{0,1}. Its reduction requires TWO
old-table digits. Kernel of aI subset pI modulo pA gives J and
(I:I)=p^-1 J. Each strict enlargement loses at most TWO table digits;
coordinate recoding has integral inverse and loses none. Each decreases
discriminant valuation by at least2, so at most floor(Ccap/2) steps leave
more than Qfin digits. A nonzero integral socle representative in O/A
satisfies xI subset A intersect rad(pO)=I, proving strict progress whenever
A is nonmaximal. This repairs the advisory report's unproved precision cap.

Factor the reduced residue algebra, lift its component idempotents via
e->3e^2-2e^3 for ceil(log2(delta Qfin)) steps (paying the initial nilradical),
and use the SAME projectors for every atom. Component norm valuations nu_ji
are visible below Ccap; divide by component degree d_j and subtract delta B0.
Repeat each row d_j times. Finite-field construction, factorization,
primitive-element search and uniform sampling have explicit finite clocks.
Total BIT cost is polynomial in native size, log p, basis bits and log(1/eta).

Soundness does NOT require these evaluated rows to equal the original Gauss
rows off Alg. At ANY accepted point t, formal substitution T=t+X and simple
roots give ALL delta embeddings of F into Frac(Cp[[X]]). Algebraic constants
map to constants in Cp, and each constant-field embedding occurs exactly
delta/[C:Q] times. Every original atom is regular and nonzero. Therefore for
EVERY e in true Alg, each evaluated row dotted with e is precisely the
valuation of the corresponding conjugate of u^e. Restricting rows to Alg
thus gives all finite-p unit conditions, always sound. ABORT probability
is <=eta. An upstream erroneous Alg basis retains its own failure budget.

A separate stronger off-Alg Gauss-row interface protects every coefficient
of det(D^delta Z0 I+sum Zi A_i). Weighted Gauss valuations determine joint
upper-orthant counts and hence alignment. That interface is bounded-error,
NOT correct-or-ABORT: local certificates do not certify a good sample.
The intended constant-restriction interface avoids this exponential
proof-only union entirely. Neither variant finds the complete prime list.

## Exact native falsifier with nonzero Alg

Take P(Z)=Z^3+3Z+3, d>=1, binary M>=2,
 f(T,Y)=P(Y^d-T^M), A(T)=T^M(T^(2M)-1),
 u_1=A(T)(Y^d-T^M-1), u_2=A(T).
The degree is3d and the expanded Y coefficients have only polynomially
many supplied sparse terms. P is Eisenstein at3. Over K=Q(alpha),
alpha a root of P, T^M+alpha is squarefree, so Y^d-(T^M+alpha)
is Eisenstein at any of its prime-polynomial factors. As
alpha=Y^d-T^M, f is irreducible over Q(T), with the required degree.

Here c=alpha-1=u_1/u_2, Alg=Z(1,-1), and Norm_K/Q(c)=-7. Thus
 Norm_F(u_1)=(-7)^d A^(3d), Norm_F(u_2)=A^(3d).
Input coefficient contents only have the nontrivial prime3, but the
required vertical support includes7. Modulo7,
P=(Z-1)(Z^2+Z+4), with coprime factors. At the degree-one prime c has
valuation1, and at the other prime valuation0. A is primitive, so a
required row is(1,0), excluding(1,-1) from the unit kernel. The kernel
inside Alg is zero. This defeats input-content-only support.

For M=2^n+1,n>=2, T=2 modulo5 gives A=1. Norm residues are nonzero
integers in{1,2,3,4}; their gcds/factors do not supply7. For any rational
t with both atoms nonzero, t is not0,1,-1 and h(A(t))>=M h(t)>=M log2.
Expanded rational specialization therefore has exponential output height
in log M. The family itself is easy from the displayed expressions;
these are scoped falsifiers, not hardness or general evaluation no-go.

## Irreducibility does not supply a content witness

Given sparse g,h in Z[T][Y], g monic, deg_Y h<deg_Y g, gcd(g,h)=1,
introduce X and set f=g+Xh,u=h. Primitivity and linearity in X imply
irreducibility over Q(T)[X,Y]; monicity in Y gives the native field
promise over Q(T,X). Its norm is exactly Res_Y(g,h), independent of X.
Thus prime-labelled native norm support includes finding all primes at
which arbitrary such sparse pairs acquire a modular common factor.
This is a reduction for the SUPPORT OPERATION. Alg may be zero in
these pencil examples; it is not a hardness reduction for fullRel or
for every unit-kernel method. The preceding nonzero-Alg family does
not turn this separate reduction into an impossibility result.

## Final torsion can be removed without general discrete logarithms

Conditional on a correctly computed torsion-exponent lattice B_tor,
choose p>W=2delta^2 and a good full finite-algebra specialization of
the original atoms. The retained native coefficient/degree bounds pay
prime generation and good-point probability with polynomial BIT cost.
Evaluate the compact products by binary powering and enumerate the
subgroup they generate: it has at most W elements.

Reduction is injective on this subgroup. If a nonidentity root of unity
zeta of order n<=W reduced to1, the exact geometric-sum identity would
give n=0 in the nonzero algebra of characteristic p>W, impossible.
Enumerate a generator and the at-most-W discrete powers, then take the
exact integer congruence kernel and lift through B_tor. This returns
the FULL nonsaturated identity lattice in polynomial time. No expanded
algebraic products, general finite-field DLog or phase oracle is needed.
Finding B_tor and the finite-unit lattice are separate unpaid inputs.
