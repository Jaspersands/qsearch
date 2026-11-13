# Fresh native operation selection: two arithmetic mechanisms

13 November 2026. Independent local-only selection. STATE/TRAPS and the
current topic notes were read; no network, API, Git, tests, or status edits.
**No new paid batch is recommended.** One useful proof-only height lemma
survives. Neither mechanism below supplies a new complete native algorithm.
The second has an immediate resource falsifier, so its proposed phase-power
compiler should not be dispatched.

## 1. Single-place p-adic replacement for sparse constant relations

**Native task and external output.** Given monic irreducible
f in Q(T_1,...,T_s)[Y], charged Y-degree delta, and nonzero atoms u_i in
the Y-power basis of degree below delta, return the full unsaturated lattice
Rel={e in Z^k: product u_i^e_i=1}. Coefficients are sparse rational
polynomials with binary T-exponents; s,delta,k grow. The established quantum
clock is polynomial in this native bit input. General classical Alg recovery
is written, and fullRel is classically written for every fixed delta.
GENERAL_SPARSE_CONSTANTS_ATTACK.md and SPARSE_CHARZERO_FUNCTION_FIELD_RELATIONS.md
give the exact contract; explicit finite-Q-algebra Lenstra--Silverberg is the
strongest applicable endpoint once its actual algebraic inputs are supplied.

**Distinct proposed operation.** Evaluate the original atoms at one good
p-adic specialization, use additive p-adic logarithms to recover the torsion
relation lattice inside Alg, and remove the finite torsion afterwards. An
injective embedding of a number field in a finite extension E/Q_p has
ker(v_E,log_E)=mu(E) on its multiplicative group. Thus complete finite-prime
support is not logically necessary. This exact injectivity statement is not
a finite-precision integer-relation algorithm.

Native evaluation itself has a plausible paid interface: select a prime and
a specialization avoiding coefficient denominators, atom norms, and the
discriminant; factor the degree-delta residue polynomial and Hensel lift one
factor. Original sparse powers are evaluated modulo p^M by binary powering,
with bit cost polynomial in the input and M log p. No expanded integer
T^exponent is constructed. The localized algebra maps to the resulting local
field, and its algebraic-over-Q subalgebra is a field, so its restriction is
injective. In particular all constant products under consideration retain
their identities. This paragraph does not supply a uniform relation guard M.

### Checked proof-only height lemma for the original atoms

This sharpens the old proof-only integer-specialization height bound; it
does not compute a place, an initial edge, a leading coefficient, or a field.
Clear scalar denominators and let D be the product of coefficient polynomial
denominators. Choose H>=2 with all resulting coefficient numerators and D
of coefficient l1-norm at most H; log H is polynomial in native bits.
For multiplication by Y write C=A/D. Its entries have l1-norm at most H.
Since each u_i has Y-degree below delta,

    M(u_i)=A_i/D^delta,
    ||(A_i)_{ab}||_1 <= B=(delta+1)^(delta+1) H^(delta+1).

Indeed expand the at most delta powers C^j, accounting for the at most
delta^(j-1) matrix-index paths. Consequently the nonzero polynomial

    P_i(T,Z)=det(D^delta Z I-A_i)

annihilates u_i, has Z-degree delta, and satisfies

    ||P_i||_1 <= C_0=delta! (2B)^delta,
    log C_0=O(delta^2 (log H+log(delta+1))).

These are formal norm bounds, not a demand to expand the determinant.
All numerical T-degrees have polynomial binary length. Choose proof-only
Kronecker weights which are injective on monomials up to a simultaneous
degree bound for the P_i, denominators, atom norms, and discriminant.
Substitution T_j=t^(weight_j) preserves their nonvanishing and cannot
increase coefficient l1-norm. The specialized monic polynomial is separable;
choose any irreducible component L/Q(t), of degree m<=delta. Every atom is
nonzero in it. The localized algebra containing the original u_i and their
inverses maps to L. Its algebraic constants form a field (the inverse of a
nonzero algebraic element is a polynomial in it), so this map is injective
on every constant product relevant to Alg. It need not embed the original
whole multivariable function field.

At one place of L over t=0, let e be its ramification index and K_0 its
residue field, of degree f over Q. Then ef<=m. In equal characteristic zero
the completed field has a coefficient field K_0 and parameter pi. Write
t=c pi^e(1+h), with c in K_0^* and h of positive valuation, and replace pi
by pi(1+h)^(1/e). Choose a^e=c^-1. The resulting compatible Puiseux embedding
has pi=a t^(1/e), and all leading coefficients lie in

    E=K_0(a),   [E:Q]<=ef<=delta.

This normalization is essential: arbitrary rescaling of a uniformizer
would not give the asserted height bound. Let alpha_i be the first nonzero
coefficient of u_i in this fixed t^(1/e) convention. Among the terms of
P_i(t,u_i), the lowest valuation occurs at least twice. Their leading
coefficients give a nonzero edge polynomial Q_i(Z) in Z[Z], with
deg Q_i<=delta and ||Q_i||_1<=C_0, satisfying Q_i(alpha_i)=0.
Removing an irrelevant power of Z is harmless. The minimal polynomial
factor and Mahler-measure bound yield

    h(alpha_i)<=log C_0+log(delta+1).

Thus all ORIGINAL atoms have proof-only polynomial-height leading
coefficients in ONE field of degree at most delta. The leading-coefficient
map is multiplicative and agrees with the induced embedding on constants;
for e in Alg its image is product alpha_i^e_i. Large binary exponents are
not expanded. No coefficient-height dependence on numerical T-degree enters.

The p-adically evaluated u_i(t) are generally NOT the alpha_i. To compare
them, extend the specialization's embedding of the common constant field
to E inside an algebraic closure of Q_p. For every e in Alg the products
then agree, and so do their p-adic logarithms. Such an extension may enlarge
the local field; it is only a proof device. Thus a valid small-alpha
separation theorem could apply on Alg without individual-atom equality.

### Exact remaining gate, and why this is not a selection

The missing operation is a uniform polynomial precision bound for recovering
ALL bounded integer relations from one p-adic log vector when k and delta
grow, together with the actual lattice extraction. A proof-only small-height
presentation does not itself supply either. In particular, multiplying
atoms by an Alg-basis matrix may produce huge-height constants; one must
retain the original atom coordinates rather than charge those expansions.
Standard linear-forms estimates cannot be declared polynomial without
checking their dependence on the NUMBER of logarithms and the degree.
No such source theorem is admitted here.

A proposed mod-p^2 shortcut has an explicit new arithmetic condition. For
an ordinary rational unit a, its principal-unit log vanishes modulo p^2
exactly when a^(p-1)=1 mod p^2. Already a=2 gives the base-2 Wieferich
congruence. The exponent now depends on the chosen prime: the existing
union bound for prime divisors of fixed bounded products does not apply.
This is a falsifier of that asserted proof, not a lower bound on all
single-place algorithms or a claim about the distribution of such primes.

Torsion is not the main remaining problem. If a basis for the torsion
relation lattice were supplied, every resulting root of unity has order
at most 2 delta^2. At a good prime p>2 delta^2 reduction is injective on
this torsion. Its relation lattice can be recovered in the smooth-order
group of exponent lcm(1,...,floor(2 delta^2)), with polynomial bit cost,
then pulled back. Logs alone must not be advertised as full unsaturated Rel.

**Next action changing the decision:** an actual uniform theorem or explicit
native counterfamily for this finite-precision integer-relation operation.
If desired, parent should first inspect explicit Kunrui Yu p-adic
linear-form bounds for their growing-k dependence, not dispatch another
constant-map search. The retained Lenstra--Silverberg source does not
supply this local interface. This is a new possible classical replacement,
not a new quantum speedup, and presently not a justified paid batch.

## 2. Davenport--Hasse powering of a Gauss-sum phase: reject this compiler

**Native input/output.** An explicit field F_q, a nontrivial multiplicative
character specified by a generator and exponent, and requested b-bit phase
accuracy for the normalized Gauss sum G_q(chi)/sqrt(q). Exact Jacobi-sum or
Frobenius reconstruction would require a separately charged output-separation
bound. Constant additive phase accuracy is a different endpoint.

**Tempting operation.** Under compatible trace and norm characters,

    G_(q^m)(chi o Norm)=(-1)^(m-1) G_q(chi)^m.

After normalization this gives a known sign times the m-th phase power.
Taking m=2^j appears to replace 2^j repetitions in phase estimation with
one lifted Gauss-sum circuit. However its ordinary native field register
has m log_2(q) qubits, and its explicit field coordinates have that many
bits. Thus this operation costs at least Omega(2^j log q) resources.
A tower of j quadratic extensions still has total field degree 2^j and
does not compress its arbitrary elements or uniform field register.
The exact identity therefore does NOT give poly(log q,b) phase powering.
This rejects this particular compiler, not all high-precision arithmetic
algorithms and not constant-accuracy Gauss-sum estimation.

The strongest baseline must be matched to the character/order family:
quadratic phases are already explicit classically, while fixed-dimensional
algebraic point-counting is not evidence for all growing-order characters.
No current-literature complexity claim is made. If priority is needed,
parent can check van Dam--Seroussi, "Efficient quantum algorithms for
estimating Gauss sums," and the Davenport--Hasse lifting theorem (Conrad's
retained Gauss/Jacobi-sum discussion is already referenced in
FOLDED_NORM_SOURCE.md). No source fetch is needed to establish the register
size falsifier, so no proof or implementation batch is recommended.

## Corpus and scope

The two exact been-tried/baselines queries used the phrases "single prime
p-adic logarithm valuation sparse function field full multiplicative
relations constants" and "Davenport Hasse lifting Gauss sum binary
extension phase estimation fast forwarding exact Frobenius trace".
The relevant hits were read: GENERAL_SPARSE_CONSTANTS_ATTACK.md,
SPARSE_CHARZERO_FUNCTION_FIELD_RELATIONS.md, and FOLDED_NORM_SOURCE.md.
No exact local-log compiler hit surfaced; catalog silence is not novelty.
The finite-field large-prime specialization/HSP/LLL alternative is EXACTLY
the existing fullRel quantum construction and was rejected as a duplicate.
No class-four HSP wrapper, inverse-trace/DQI, Gaudin, wavelet conductivity,
quadratic-permutation index erasure, or neighboring transform is reopened.
The surviving lemma is a proof-only resource improvement. Full growing-delta
classical Rel and a new Shor-level endpoint both remain unproved here.
