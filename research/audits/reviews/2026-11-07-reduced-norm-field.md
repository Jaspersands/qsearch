# Prescribed splitting field: core and polynomial-bit review

2026-11-07. Scope: Sections 1--3 of `REDUCED_NORM_PRESCRIBED_FIELD.md`.
Read STATE/TRAPS and the actual Goldstein--Schacher source, especially
Lemma 1 and Theorem 2. No network/API, Git, implementation or finite sweep.
The split-algebra quantum primitive and compact regular-module endpoint
are outside this review.

**Verdict:** the field constructor closes in polynomial BIT cost, with the
explicit precision/CRT construction below. The ramification-support and
real-signature claims are correct. Distinguish the Q-regular trace used for
the integral discriminant from the K-regular trace used for real signatures.
The finite-field counting proof is valid, and the Newton criterion needs
no tameness assumption. This proves a field-construction lemma, not the
complete reduced-norm algorithm whose remaining endpoint is reviewed
separately.

## 1. Regular-trace support without a maximal algebra order

Put R=[K:Q] n^2. In a rational basis `1,b_2,...,b_R`, let M clear every
multiplication denominator. Then
`Lambda=Z*1 + sum_{i>1} Z*(M b_i)` is closed under multiplication:
the constant coefficient of `(M b_i)(M b_j)` is integral after multiplication
by M^2, and its other coefficients in the scaled basis are multiplied by M.
All coordinate sizes are polynomial in the supplied structure constants.
The ordinary Q-regular trace pairing is nondegenerate because A is a
semisimple Q-algebra in characteristic zero. Its Gram determinant delta is
a nonzero integer of polynomial bit length.

Here is a complete proof that every finite ramification prime lies over a
rational prime dividing delta. If `p` does not divide delta, let
`B=Lambda tensor Z_p` and `Bbar=B/pB`. For an element r of the Jacobson
radical of Bbar and any y, ry belongs to that radical and is nilpotent.
Left multiplication by ry is nilpotent, so its ordinary trace is zero.
Nondegeneracy of the reduced regular trace pairing forces the radical to
vanish. By the finite-dimensional semisimple structure theorem and the
finite-division-ring theorem,

    Bbar = product_t M_(s_t)(F_(p^f_t)).

For clarity, this semisimple reduction really implies the required generic
splitting; it is not merely a heuristic good-reduction test. Lift its
orthogonal idempotents in the p-adically complete ring B. Cross Peirce
modules between distinct blocks reduce to zero and hence vanish by
Nakayama, so the block idempotents are central. Within a block, lift the
diagonal matrix idempotents. Lift opposite off-diagonal matrix units and
correct their products by units in the corners to obtain equivalences of
these idempotents. This yields an exact matrix-ring presentation `M_s(C)`
over one corner C.

The corner C is a finite free Z_p-module with reduction F_(p^f), so its
rank is f. Choose a finite-field primitive element, and any monic lift F
of its degree-f irreducible polynomial. A lift of the primitive element
has F' invertible. Newton iteration in the commutative subalgebra generated
by that lift converges to a root of F in C. It gives a homomorphism
`Z_p[T]/F -> C`, which is an isomorphism by reduction, Nakayama and the
equal ranks. Thus C is the unramified degree-f field order. Consequently

    A tensor_Q Q_p = product_t M_(s_t)(Q_(p^f_t)^unram).

Comparing centers with `K tensor_Q Q_p` proves that A is split at every
K-place above p. No maximal A-order, explicit lifted matrix units or local
splitting computation is needed by the algorithm: this lifting is a proof
of the support bound. The trace discriminant may include unnecessary
primes, including primes dividing matrix sizes; that is harmless.
Factoring delta is the charged bounded-error quantum factoring call from
the main contract. Given its verified factors, decomposition in the
supplied maximal order of K and the remaining construction are classical
polynomial-bit procedures with the stated finite-field randomness. This
review does not assert unconditional classical polynomial-time integer
factoring.

## 2. Real ramification and its bit cost

Use `q_A(x)=Tr_K(L_(x^2))`, where L is left multiplication on the
n^2-dimensional K-vector space A. Its scalar factor relative to the
reduced trace is positive at every real embedding. On M_n(R), diagonal
entries give n positive directions and each off-diagonal pair contributes
one positive and one negative direction. The signature difference is +n.
On M_r(H), n=2r, each diagonal quaternion contributes (1,3) and each
off-diagonal quaternion pair contributes (4,4). The difference is -2r=-n.
This detects precisely the split and nonsplit real completions.

Compute the symmetric K-matrix of q_A and diagonalize it with exact
fraction-free field linear algebra. If a diagonal pivot vanishes but an
off-diagonal entry does not, a two-vector basis change produces a nonzero
pivot. Determinant bounds keep all resulting coordinates polynomial size.
Certified real-root isolation and sign evaluation of these nonzero
algebraic numbers have polynomial bit cost in the growing field degree
and expanded heights. The same applies to signs of a. Thus the HMS NO
test has a paid exact clock, rather than an assumed numerical gap.

One can make the magnitude bounds used later entirely explicit. Choose a
positive integer d_a with b=d_a a integral. Let U_a>=1 be an integer bound
on the absolute values of all conjugates of b, for example the maximum
row-sum norm (rounded up to at least one) of its integral multiplication
matrix. Since its nonzero absolute norm is an integer,

    |sigma(a)| >= alpha := 1/(d_a U_a^([K:Q]-1))

for every embedding. The positive rational alpha has polynomial bit size
and is at most one. It supplies a concrete lower bound without needing
to compute the minimum positive real embedding numerically.

## 3. Prescribed-constant finite-field density

The counting argument in the note is correct. For a prime ell dividing g,
the restriction of `N_(q^g/q)` to F_(q^(g/ell))* is
`N_(q^(g/ell)/q)^ell`. The equation that this equals a prescribed nonzero
target admits at most ell values of the smaller-field norm, each with
`(q^(g/ell)-1)/(q-1)` preimages. Union over these maximal proper subfields
catches every element of degree less than g.

For prime g, the resulting bad fraction is at most `g/(2^g-1)<=2/3`.
For composite g>=6, the sum of its distinct prime divisors is at most g,
and each denominator is at least `q^(g/2)+1`. The real function
`x/(2^(x/2)+1)` decreases for x>=6 and is 2/3 at 6. The remaining g=4
case has bad fraction at most `2/(q^2+1)<=2/5`. Thus at least one third
of each prescribed norm fibre consists of full-degree elements. Dividing
by g and by the q^(g-1) possible coefficient tuples proves irreducibility
probability at least `1/(3g)`. The g=1 case is immediate.

Uniform coefficient sampling and Frobenius/gcd irreducibility tests are
classical finite-field operations. Across Q selected places, cap trials
at `O(g log(Q/eta))` for each; failure is at most the allocated budget.
No finite-field norm-preimage oracle or quantum discrete logarithm is used.

## 4. Local polynomial and explicit stability precision

Let c=(-1)^n a, v=v_q(c), k=floor(v/n), v0=v-kn, g=gcd(n,v0),
e=n/g and h=v0/g, with g=n when v0=0. A basis element of q outside q^2
is a valid uniformizer pi. Such an element exists because a Z-basis of q
cannot lie wholly in its proper subideal q^2. It is not a generator of q.
Computing these ideals and membership tests uses the supplied maximal
order and polynomial-size HNF arithmetic.

There is also an elementary proof requiring no imported Newton theorem.
All coefficients lie on or above the line of height `v(n-i)/n`, with
strict inequality away from the indices divisible by e. For any root
alpha of the constructed or sufficiently perturbed polynomial, valuation
smaller than v/n would make the leading term the unique least-valuation
term; larger valuation would make the constant the unique such term.
Neither can cancel. Hence `v_q(alpha)=v/n=k+h/e`. Its reduced denominator
forces the ramification index of K_q(alpha) to be a multiple of e.
The unit `beta=alpha^e/pi^(h+ke)` reduces to a root of the chosen degree-g
irreducible residual polynomial, forcing residue degree at least g. Thus
`[K_q(alpha):K_q]>=eg=n`, which proves irreducibility. This includes e=1
and v0=0. It remains valid when p divides e: no tame-root or derivative-unit
premise is used. Scaling gives the exact constant c as stated.

Write b_(q,i) for the free coefficient of X^i, 1<=i<n, in P_q. Its
Newton line is of height `v(n-i)/n`. It suffices to require

    v_q(t_i-b_(q,i)) >= ell_q := 1+|v_q(c)|.

This is strictly above that line for every i. The Newton polygon and
every residual coefficient are then unchanged. The exponent ell_q is
polynomial NUMERICALLY in input size: valuations of the expanded c are
bounded by the bit lengths of an integral numerator's norm and its
rational denominator. The same bounds pay direct ideal-membership
valuation calculations. Every power of pi used in P_q has polynomial
numerical exponent, so the expanded local coefficients have polynomial
bit size. Residue representatives come from the explicit finite algebra.

The local unit `u0=c/pi^v` requires special care: a denominator in its
expanded global coordinates need not be invertible modulo q, despite u0
being a local unit. Write `u0=b/d` with b integral and a positive rational
integer d. If `t=v_q(d)`, then `v_q(b)=t`. Solve

    d*z = b mod q^(t+1),  with z in O_K,

using the generator matrix for `d O_K + q^(t+1)` and HNF with preimages.
This ideal is q^t, so the solution exists. Dividing the congruence by d
shows that z is the required residue of u0 modulo q. This is the already
proved division interface in `COMPACT_RESIDUE_CONDUCTOR_DECISION.md`,
not an invalid inverse of d modulo q. Here t, all ideal sizes and all
HNF coordinates are polynomially bounded because u0 is EXPANDED with
polynomial-size coordinates. Arbitrary succinct local input with a huge
binary valuation would not justify the same numerical-exponent bound.

## 5. Explicit CRT plus simultaneous real smallness

The following fills the note's quantitative weak-approximation obligation.
Choose a positive rational integer D clearing every denominator of every
b_(q,i), so D b_(q,i) is globally integral. Put

    E_q=v_q(D)+ell_q,   I=product_q q^E_q.

All exponents and log Norm(I) are polynomial. For each free coefficient,
ideal CRT computes an integral N_i satisfying

    N_i = D b_(q,i) mod q^E_q   for every selected q.

Reduce N_i in an HNF fundamental domain of I. Its expanded coefficients,
and hence the integer row-sum bound U on every conjugate of all N_i, have
polynomial bit length. Take a positive rational integer M with
`M O_K subset I`; for example use the product over underlying rational p
of `p^(max_{q|p} E_q)`. Its bit size is polynomial, and this choice is
valid even at ramified primes because v_q(p)>=1.

Set delta0=alpha/(4n), using the explicit alpha from Section 2. Choose an
integer s of polynomial numerical size with `2^s>=max(1,U/delta0)` and put

    T=1+M*2^s,   t_i=N_i/(D*T).

T is positive and congruent to one modulo I; in particular it is a local
unit at all selected q. Since D b_(q,i) is integral,

    N_i-D*T*b_(q,i)
      =(N_i-D*b_(q,i))+(1-T)*D*b_(q,i) belongs to q^E_q.

Consequently `v_q(t_i-b_(q,i))>=ell_q`, as required. At every real
embedding, `|sigma(t_i)|<=U/(D*T)<=delta0`. Both D and T may be large
numerically, but their binary lengths and every output coordinate length
are polynomial. There is no enumeration up to T and no qualitative
approximation oracle. Indeed archimedean numerical evaluations are
unnecessary for this final size bound.

The global polynomial `P=X^n+sum_{i=1}^{n-1}t_i X^i+c` therefore has
all required local irreducibilities and its constant is untouched. At a
nonsplit real place n is even and a>0. For |x|<=1 the absolute free-term
sum is at most `(n-1)delta0<a/4`; for |x|>=1 it is at most
`(n-1)delta0 |x|^n<|x|^n/4`. Hence P(x)>0 there.

Including rational prime 2 ensures a selected finite place and therefore
global irreducibility. F=K[X]/P has degree n. At every potentially ramified
finite place its single completion has degree n, a multiple of the local
index. At nonsplit real places its completions are complex, of degree two.
All other places have index one. The actual source's Lemma 1 then proves
F splits A, and the constant gives `N_(F/K)(theta)=a` exactly. The field's
expanded arithmetic table has polynomial size; its maximal-order payment
belongs to the separately reviewed downstream primitive.

## Remaining scope

No fatal counterexample was found in Sections 1--3. The critical guards are
the two different regular traces, all primes dividing the actual order
discriminant, normalized prime-ideal valuations, strict precision above
the Newton line, and T congruent to one at the DENOMINATOR-ADJUSTED modulus.
Dividing CRT representatives by an arbitrary large T would fail this last
test. Fixed constant c and its real signs cannot be altered during
approximation. The construction permits nonintegral coefficients and
produces a field, not an integral norm witness; it does not contradict
integral outliers. No normal closure, local division presentation, maximal
A-order or supplied field generator is assumed. The full reduced-norm
witness theorem still needs the separate split-map, compact zero-test and
regular-module reconstruction review.

The later advisory report
`audits/claude_runs/2026-11-07-reduced-norm-local/response.md` supplies the
same elementary root-valuation/degree proof, checked above. Its assertion
that the algorithm is only Las Vegas in expected time is not the chosen
contract: the verified success probability gives the capped trials and
ABORT/error budget already specified here. Its finite examples were not
used as evidence for the quantified lemma.
