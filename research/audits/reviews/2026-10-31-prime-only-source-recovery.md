# Recovered Prime-Only Stabilized Surface Source

2026-10-31. Independent mathematical review of the retained October 23--25
bundles. This recovers prior work; it is not a new algorithm, a geometric
implementation, a novelty certificate, or a classical-hardness result.

## Decision

The current mixed-prime shifted-norm selector is not the next necessary
blocker for the weak-isogeny surface source. The already retained
`bundles/prime-only-source-2026-10-25/PRIME_ONLY_SOURCE.md` gives a different
constructive route: dimension-16 stabilization, one globally fixed odd
squarefree multiplier, and only prime-order weak evaluations. Its algebra
survives this independent review. Prefer auditing/executing its actual
geometric source and matched classical attacks over further selector work.

This does not solve the genus-two selector itself. It changes the output
geometry, while preserving the original Sp4 action and hidden kernel.
Keep the general end-to-end claim conditional on the explicit source and
geometric model contracts below.

## The Failed Map Is Different

`WEAK_SIEGEL_CONVERSION_AUDIT.md` rules out the natural complementary map
whose pulled-back polarization is `N I - k^2 ell H^-1`. That calculation
does not refute the recovered bundle's map

    F = H8^-1 C^dagger,
    C^dagger C = C C^dagger = N H8,
    F^dagger H8 F = N I,       FC = CF = N I.

Here `H8=diag(H,...,H)` on eight copies of the original surface, and all
entries of C are commuting integral polynomials in H. Integrality of
`H^-1=tI-H` is essential. The recovered construction does not repair the
failed complementary map; it supplies a different map with the required
polarization identity.

## Checked Arithmetic And Quantifiers

For every group query `M in Sp4(F_ell)`, evenizing each quaternion-basis
coefficient preserves its reduction modulo odd ell and makes the bounded
elementary lift `sigma0` congruent to I modulo 2. Appending
`tau=[[1,ell],[0,1]]` preserves M modulo ell and yields

    sigma = sigma0 tau,
    S = sigma^dagger sigma = I + ell T0,
    S mod 2 = [[1,1],[1,0]].

Thus its integral diagonal trace t is odd. Positivity and Moore determinant
one give `t>=3` and `S^2-tS+I=0`; rational conjugation gives the same
identity for `H=phi S phi^-1`. The integral polarization argument is still
the prior surface-source argument, not a consequence of a formal-ring test.

The actual compiler has at most 156 evenized quaternion factors, plus tau.
With `B0=sum_i Nrd(b_i)` for the supplied full integral order basis,

    U = 2+4(ell-1)^2 B0,
    t <= T = U^156 (2+ell^2)

holds uniformly over all M. This uses the existing compiler proof in
`bundles/kernel-output-2026-10-23/UNIFORM_SOURCE_BOUND.md`, with the enlarged
coefficient bound and final factor; it is not an observed maximum.

Choose one N as a product of distinct small odd primes avoiding p and ell,
until `N>T^2`. Because t is odd, `gcd(t+2,t-2)=1`. The explicit coin
construction gives nonnegative X,Y with

    (t+2)X+(t-2)Y=N.

Four-square expansions and the eight-square norm identity yield C above.
This works without factoring t+2 or t-2. Standard primorial growth gives
polynomial bit length of N and polynomially bounded largest prime in the
public input size. The imported unconditional expected-polynomial
four-square algorithm, rather than the finite SymPy implementation, remains
the asymptotic dependency.

For every `r|N`, `FC=NI` forces the local Smith exponents of F to lie in
`{0,1}`. Its polarized degree makes exactly 16 of the 32 exponents equal
to one. Consequently `ker(F_r)=im(C_r)` has dimension 16 and is maximal
isotropic. This remains true when `r|(t^2-4)`; no semisimplicity assumption
is needed. A common unit on the weak source basis changes generators, not
the subgroup. All weak phi queries are at odd primes. Lists of `r^16`
points and dimension-16 theta coordinates remain enormous fixed-dimension
costs, not a practical resource estimate.

## Field, Quotient And Marking Contracts

Retain `p>3`, distinct odd ell, the known evaluable full source order, one
genuine ell-polarized phi, and the ORIGINAL modeled polarized target.
The full source order AND phi must be defined over a paid common finite
field k. This promise is not inferred from mutually compatible weak tables
or added silently to a weaker input.

The proof in `bundles/source-field-audit-2026-10-23/SOURCE_FIELD_AUDIT.md`
checks: Frobenius centralizes the full quaternion order and hence is a
scalar c; naturality transfers `[c]` to B and every rational quotient.
One quadratic base extension gives scalar `[c^2]` with `c^2=1 mod 8`.
All intermediate 8-torsion and all geometric homomorphisms between these
scalar-Frobenius varieties descend over that fixed base. The latter uses
surjectivity, not separability, of `[c^2]`. Separate prime-order point
fields have degree at most `r-1`; they must retain fixed compatible
embeddings and must not be accumulated into a compositum.

The retained full paper is at
`/Users/jaspersands/Developer/qsearch-research-work/ppav-source-2026-10-23/2026-1142.pdf`.
Its A26 (printed page 14) explicitly accepts the COMPLETE maximal-isotropic
subgroup in X[N] and prescribes the smallest field stabilizing the subgroup;
A27 supplies products. Proposition 6.24 states the corresponding theta-model
operations. The prime-only route uses A26 at PRIME r. It therefore avoids
the nonfree prime-square defect of the displayed Algorithm 1 and does not
require an unverified repair of that loop. This is an imported geometric
operation contract, not a locally executed quotient or descent algorithm.

The quotient q has `ker(q)=ker(F)` and admits a polarized isomorphism
`u:Y -> (B,lambda_B H)^8` with `u q=F`. For each fixed marking prime s
coprime to N, transport is `q([N^-1 mod s] C Z)`, with one common mask
across the entire replicated tuple. It is N inverse, not N squared inverse.
Joint marked canonicalization must use ONE polarized isomorphism across
all levels. The existing rigidity theorem and its bounds remain an
independent dependency; per-level minima and coefficient-field Frobenius
orbits are invalid substitutes.

## Independent Validation And Boundaries

Using `/opt/anaconda3/bin/python`, with plugin autoload and bytecode disabled,
`pytest -q -p no:cacheprovider -W error` gave:

- `bundles/smooth-repolarization-2026-10-23/test_smooth_repolarization.py`:
  **56 passed in 0.70s**.
- `bundles/prime-only-source-2026-10-25/test_prime_source.py`:
  **26 passed in 5.21s**.

A separate Sage calculation over `ZZ[c0,...,c7]` verified BOTH generic
identities `C^T C = C C^T = (sum_i c_i^2) I8` for the bundle's octonion
matrix. No files under review were modified, and no broad suite was run.
Finite tests do not establish the quantified source theorem; the arguments
above are the mathematical checks.

The strongest required comparators remain the same-input product/mixing,
reverse-transport, and weak-evaluation attacks. This review did not run a
new geometric classical attack. Supplying target End/Hom lattices would
change and already dequantize the input. Neither an incomplete classical
attack nor this source construction supplies a lower bound.

No curve/torsion generation, geometric quotient, canonical marked label,
coherent oracle, or quantum HPGP learner was executed. Keep novelty,
classical hardness, cryptanalytic success and quantum speedup gates false.
The next decisive experiment is a genuinely modeled source instance with
the paid fields and prime-only data, comparing equal/different hidden-kernel
cosets after one joint marked canonicalization, while running the legal
classical attacks on that same input. Such finite success would validate
source behavior only, not an asymptotic advantage.
