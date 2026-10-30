# Independent Review: Combined Geometric Source And Suborder Reduction

Date: 2026-10-25.

## Verdict

**No fatal algebraic counterexample was found to the composition under its explicitly augmented input and geometric-algorithm hypotheses. The material does not yet establish an unconditional algorithm from an arbitrary native evaluable full-rank suborder alone.**

In particular, the primitive-map degree envelope, the use of modulus `2m` despite unknown degree dividing `p*m`, joint projective marked separation, the unknown-depth receiver, and removal of the inseparable factor from the transported target order are mutually compatible. I do not find a need to know the hidden isogeny, its degree, a target maximal order, or its Frobenius branch in those arguments.

The findings below concern the exact theorem boundary and omitted interface constructions. They are not evidence that the conditional source is impossible. Several are acknowledged explicitly in the input notes. Absence of a geometric implementation is an execution gap, not by itself a mathematical refutation of a construction using published algorithms.

This was one independent adversarial review, not a formal verification, a proof of novelty, or an executed native EndRing solver. No additional reviewer or agent was launched. Only the assigned report was written. The migrating Desktop source, staging copies, and the user's new polarization-completion bundle were not read or edited.

## Severity-Ranked Findings

### 1. P1 Scope Blocker: The Native Suborder-Only Theorem Still Needs Preprocessing

References: [SUBORDER_TRANSCRIPT.md:20](/Users/jaspersands/Developer/qsearch-research-work/suborder-transcript-2026-10-25/SUBORDER_TRANSCRIPT.md:20), lines 20-38 and 84-85; [CYCLIC_ODD_DEGREE.md:40](/Users/jaspersands/Developer/qsearch-research-work/cyclic-odd-degree-source-2026-10-25/CYCLIC_ODD_DEGREE.md:40), lines 40-46. Primary comparison: Chen--Petit, retained PDF pages 8-10 and 12, printed pages 7-9 and 11.

The starting contract supplies more than an evaluable suborder `R <= End(E)`: it supplies an actual reference curve `E0`, its full evaluable order `O0`, and a compatible rational algebra dictionary `theta`. Clearing denominators gives `N` only AFTER those objects and their correspondence have been obtained. The new projective intertwiner construction removes the particular upstream norm-solving call needed for an arbitrary-order weak evaluator; it does not itself construct these initial objects.

The primary comparison matters here. Chen--Petit's native suborder input is efficiently represented basis maps (Section 2.3). Its Remark 17 discusses computation of the rational quaternion dictionary, with quantum factorization removing its stated factorization heuristics. Its Lemmas 8 and 10 retain GRH in the special-reference construction for general characteristic. Those are different dependencies from Proposition 26's heuristic norm equation. Bypassing Proposition 26 does not, on its own, bypass all of them.

**Exact obligation:** from the declared native input, construct `E0`, evaluable `O0`, the common rational algebra coordinates and their map to `R`, compatible fields, and `N`, with polynomial bounds in the actual input encoding length. Record every assumption and every integer factorization used. Do not obtain the dictionary by first computing the unknown `End(E)` or a connecting isogeny.

**Disposition:** keep the theorem conditional on the explicit augmented input, or supply the preprocessing reduction with its assumptions. The notes already make this limitation at lines 30-34, so this is a blocker to promotion, not a contradiction of their current conditional wording. I found no counterexample to the primitive-map lemma once the global dictionary is genuinely supplied.

### 2. P2 Repairable Omission: Construct The Initial Abstract Splitting At `m`

References: [SUBORDER_TRANSCRIPT.md:134](/Users/jaspersands/Developer/qsearch-research-work/suborder-transcript-2026-10-25/SUBORDER_TRANSCRIPT.md:134); [DOUBLE_LEVEL_SOURCE.md:35](/Users/jaspersands/Developer/qsearch-research-work/double-level-source-2026-10-25/DOUBLE_LEVEL_SOURCE.md:35), lines 35-39 and 70-96; [CYCLIC_ODD_DEGREE.md:45](/Users/jaspersands/Developer/qsearch-research-work/cyclic-odd-degree-source-2026-10-25/CYCLIC_ODD_DEGREE.md:45).

The downstream lift starts with a specified split `O0/mO0 -> M2(Z/m)` and extends it to `2m`. The suborder note's original input list does not include that split, and its small-auxiliary-prime intertwiners do not produce it: those primes deliberately avoid `m`. Merely relabeling the old split as public algebra leaves an omitted input-conversion step.

This appears repairable without secret torsion or target advice. For each odd `ell | m`, sample an element of `O0/ell O0` with distinct split characteristic roots. In `M2(F_ell)` the probability is `(ell^2-1)/(2*ell^2)`, at least `4/9`. Trace and norm are available from the source algebra. Finite-field quadratic root finding gives an idempotent

    e = (a - lambda_2)/(lambda_1 - lambda_2).

The left module `(O0/ell O0)e` has dimension two, and left multiplication gives the split. Lift the idempotent and module basis to `ell^e`, using `3e^2-2e^3` to improve precision, check the multiplication and involution tables, and combine by CRT. At 2, the constant-size search already described in the double-level note suffices. The resulting arbitrary coordinate choice consistently defines the hidden line; it need not match an inaccessible geometric point basis.

**Exact obligation:** include this algorithm, or an exact published equivalent, with expected bit cost, factorization input, and coordinate compatibility across lifting and output ideal reconstruction. A search through all `ell^4` algebra elements is not polynomial in `log(ell)` for large `ell`.

**Disposition:** a routine-looking source-algebra repair, not a restriction to small prime factors and not a new geometric assumption. The algebraic randomized construction above is a review argument; it was not implemented here.

### 3. P2 Theorem-Completion Obligation: Instantiate The Model And Uniform Oracle Contract

References: [DOUBLE_LEVEL_SOURCE.md:47](/Users/jaspersands/Developer/qsearch-research-work/double-level-source-2026-10-25/DOUBLE_LEVEL_SOURCE.md:47), lines 47-50, 169-183 and 244-252; [SUBORDER_TRANSCRIPT.md:154](/Users/jaspersands/Developer/qsearch-research-work/suborder-transcript-2026-10-25/SUBORDER_TRANSCRIPT.md:154), lines 154-166; [SMOOTH_REPOLARIZATION.md:228](/Users/jaspersands/Developer/qsearch-research-work/smooth-repolarization-2026-10-23/SMOOTH_REPOLARIZATION.md:228), lines 228-242; [PPAV_SOURCE_DECISION.md:48](/Users/jaspersands/Developer/qsearch-research-work/ppav-source-2026-10-23/PPAV_SOURCE_DECISION.md:48), lines 48-60 and 96-128.

The quotient route has the correct published interface; it does NOT require calling interpolation on an unrepresented new polarization. Nevertheless, a theorem from curve equations and evaluators must explicitly compose:

1. Effective conversion of the original elliptic models and their auxiliary points into the chosen level-4 theta model, preserving the specified field embeddings. A3 and Proposition 6.3 establish representability; A3 alone is not this conversion algorithm.
2. The field-preserving A26 quotient, A27 products and A18 point evaluations on the stated kernel lists, retaining polynomial-size map encodings and separately represented auxiliary fields.
3. A7/A8/A22/A25 with ONE common polarized isomorphism across all marks, followed by bounded reversible evaluation with all temporary choices uncomputed.

The input notes leave these obligations open rather than falsely claim their receipts implement them. The primary theorem supplies expected-time routines on represented objects, and the existing fixed-random-tape argument is a legitimate route to a bounded coherent source. It must be applied to the complete label algorithm, not just the four-square subroutine. In particular, a successful subroutine must be correct, and input/output lengths must be uniformly bounded across every query.

For a verified Las Vegas label algorithm with a uniform expected bound `B(L)`, cap an attempt at `2B(L)` and repeat `h` times. Since `|Sp4(Z/m)| < m^10`, choosing `h >= ceil(log2(m^10/epsilon))`, with additional overhead if subroutines are capped separately, gives a good fixed random tape on the whole query domain with probability at least `1-epsilon`. Reversibly evaluate, copy the canonical label, and reverse the workspace. This is not the same as knowing that individual tested inputs terminate quickly.

**Exact obligation:** state the initial elliptic-to-theta conversion and a uniform polynomial `B` for the composed fixed-field algorithm, with verified failure handling. Either discharge this by exact algorithms and a bit-length analysis or retain it as a theorem hypothesis. No new polarization-completion construction is demanded by this finding.

**Disposition:** conditional mathematical composition is defensible with these algorithms as hypotheses. The files do not yet justify treating their finite controls as a bounded native quantum implementation. I found no separate counterexample to joint canonicalization once the published represented-object primitives and the fixed-field contract are honored.

## Composition Audit

Notation in this report distinguishes `D = deg(psi)` from the smooth auxiliary quotient multiplier `Delta`, called `D` in the double-level note. Set `m = N/p^v_p(N)` and `U = p*m`.

### Native Dictionary To One Primitive Global Map

References: [SUBORDER_TRANSCRIPT.md:40](/Users/jaspersands/Developer/qsearch-research-work/suborder-transcript-2026-10-25/SUBORDER_TRANSCRIPT.md:40), lines 40-89.

The existence proof is not circular. Any geometric isogeny `u:E0 -> E` gives a rational algebra identification. Skolem--Noether compares it with `theta`, so one rational homomorphism line implements the prescribed dictionary. Its intersection with the integral Hom lattice is saturated of rank one; its generator `psi` is primitive and unique up to sign. None of `u`, the inner conjugator, or `psi` is needed as computational input.

For `ell != p`, primitivity forces the kernel's Smith exponents to have minimum zero. Otherwise `E0[ell]` lies in the kernel and `psi/[ell]` is integral. Thus the `ell`-part is cyclic of order `ell^k`. Since all `theta(Na)` are integral, all `Na` preserve this subgroup. Fullness of `O0` gives the entire `M2(Z/ell^k)` action; sending its generator to a complementary basis vector forces `ell^k | N`.

At `p`, the argument must use subgroup schemes, not just geometric points. A supersingular elliptic curve has no nontrivial etale p-primary kernel. A degree at least `p^2` purely inseparable component contains `ker[p]`, since the dual of relative Frobenius is also inseparable. It would again allow scalar division. Therefore

    D = p^epsilon * d,   epsilon in {0,1},   d | m.

This is an existence bound for the primitive implementer, not an algorithm to infer its degree. The notes' `psi` versus `2psi` control correctly excludes that inference. Lack of primitivity of the suborder inclusion does not invalidate the argument.

### Small-Prime Intertwiners

References: [SUBORDER_TRANSCRIPT.md:91](/Users/jaspersands/Developer/qsearch-research-work/suborder-transcript-2026-10-25/SUBORDER_TRANSCRIPT.md:91), lines 91-126; [suborder_transcript.py:68](/Users/jaspersands/Developer/qsearch-research-work/suborder-transcript-2026-10-25/suborder_transcript.py:68), lines 68-107.

For `r` avoiding `pN`, the primitive map is invertible on `r`-torsion. The normalized actions of the four scaled source basis elements generate `M2(F_r)`. An intertwiner exists by the global map, and Schur's centralizer calculation shows its solution space is exactly one-dimensional, consisting of scalar multiples of `psi_r`. The direction of the equation `B_i T = T A_i` is correct.

The advertised eight evaluations at each endpoint and two `r^2` coordinate tables are accurate for this interface, excluding separately charged point generation and evaluator costs. The table cost is polynomial only at the bounded auxiliary primes. Reuse the same normalized tuple across both copies and every query. No weak evaluation at a large kernel prime is produced or required.

The local checks establish only local representations. They cannot authenticate a global dictionary or genuine native evaluator provenance. This limitation is stated correctly, not an undisclosed circularity.

### Double-Level Lift And Half-Polarization

References: [DOUBLE_LEVEL_SOURCE.md:52](/Users/jaspersands/Developer/qsearch-research-work/double-level-source-2026-10-25/DOUBLE_LEVEL_SOURCE.md:52), lines 52-145; [SUBORDER_TRANSCRIPT.md:134](/Users/jaspersands/Developer/qsearch-research-work/suborder-transcript-2026-10-25/SUBORDER_TRANSCRIPT.md:134), lines 134-152.

The even-modulus correction is valid: its error is alternating, the first-order correction cancels it modulo `2m`, and the quadratic correction is divisible by `2m` when `m` is even. The split-lifting and elementary-commutator construction produce an actual integral automorphism, not a formal modular matrix. Its Gram operator has

    S = sigma^dagger sigma = I + 2m T0.

Let `Psi = psi x psi` and `H = Psi S Psi^-1`. Since `Psi` is a polarization similitude of multiplier `D`, conjugation preserves the relevant involution and positivity. Away from `p`,

    (H-I)/2 = (m/D) Psi T0 Psi^dagger

is integral. At `p`, use the unique maximal order in the QUATERNION DIVISION ALGEBRA, entry by entry. One must not assert uniqueness of maximal orders in `M2(B_p)`, which is false. The actual argument only needs the former fact and therefore works. As `p` is odd, division by 2 is harmless there.

The Moore determinant calculation gives `t = 2 mod 4`; with `s=(t-2)/4` and `A_H=(H-I)/2`,

    A_H^2 = sH,   (A_H+I)^2 = (s+1)H.

At `t=2`, positivity gives `H=I`. The degenerate formal quadratic ring is not being mistaken for a nontrivial geometric polarization. The stronger congruence at `2m` is essential; the insufficient-congruence counterexample in lines 129-134 remains relevant.

### Smooth Quotients Actually Model The Changed Polarization

References: [DOUBLE_LEVEL_SOURCE.md:147](/Users/jaspersands/Developer/qsearch-research-work/double-level-source-2026-10-25/DOUBLE_LEVEL_SOURCE.md:147), lines 147-183; [PRIME_ONLY_SOURCE.md:118](/Users/jaspersands/Developer/qsearch-research-work/prime-only-source-2026-10-25/PRIME_ONLY_SOURCE.md:118), lines 118-167; [SMOOTH_REPOLARIZATION.md:115](/Users/jaspersands/Developer/qsearch-research-work/smooth-repolarization-2026-10-23/SMOOTH_REPOLARIZATION.md:115), lines 115-152 and 171-206.

Choose an odd squarefree `Delta > T^2` avoiding `pN`. The coin identity `(s+1)X+sY=Delta` and two four-square representations produce the eight commuting coefficients. The norm identity then gives

    C^dagger C = C C^dagger = Delta H8,
    F = H8^-1 C^dagger,
    FC = CF = Delta I,   F^dagger H8 F = Delta I.

Integrality of `F` comes from integrality of `H^-1`, not from reduction modulo auxiliary primes. Positivity and principality come from the actual `H`, not from the formal norm certificate. Thus `F` is an actual polarized isogeny from the OLD modeled `X=(E^2)^8` to the changed-polarization object, with multiplier `Delta`.

At each `r | Delta`, `FC=Delta I` makes the Tate-module Smith exponents of `F` zero or one. Its determinant valuation is 16, so exactly 16 are one. Consequently `ker(F_r)=im(C_r)` is a 16-dimensional maximal isotropic subgroup. This does not assume that the quadratic polynomial for `H` is semisimple modulo `r`.

A26 accepts that full `r^16`-point subgroup list on the old model. Successive prime quotients give `q:X -> Y` with the same kernel and multiplier as `F`. The universal property supplies `u:Y -> (E^2,lambda H)^8` with `u q=F`; this `u` is only a proof object. It is NOT an input to the algorithm. The construction therefore avoids the genuine circularity of applying Theorem 7.1 to an as-yet unrepresented new polarization.

The prime-only construction also avoids the old nonfree prime-square CRT-loop issue. The cost remains at least the explicit `r^16` kernel-list size, plus fixed-dimensional theta arithmetic. These are theoretical fixed-dimension polynomial costs, not practical estimates.

### Fields And Joint Markings

References: [FIELD_NORMALIZATION.md:9](/Users/jaspersands/Developer/qsearch-research-work/elliptic-field-normalization-2026-10-25/FIELD_NORMALIZATION.md:9), lines 9-68 and 104-121; [SOURCE_FIELD_AUDIT.md:84](/Users/jaspersands/Developer/qsearch-research-work/source-field-audit-2026-10-23/SOURCE_FIELD_AUDIT.md:84), lines 84-114; [RETAINED_MARKED_RIGIDITY.md:94](/Users/jaspersands/Developer/qsearch-research-work/one-endomorphism-access-audit-2026-10-25/RETAINED_MARKED_RIGIDITY.md:94), lines 94-129.

For supplied supersingular elliptic endpoints over one explicit `F_q`, `p>3`, their twelfth Frobenius powers are both `[q^6]`. This is supported by the standard trace classification and the note's direct calculations, including the repeated-root case in the division algebra. It implies descent of all geometric homomorphisms between the fixed endpoints, even inseparable ones. It is stronger than merely saying that each endpoint has all endomorphisms defined somewhere.

Since `q^6 = 1 mod 8`, full 8-torsion is rational over `F_(q^12)`. The computed quotients inherit the same scalar Frobenius. Separate prime-level point fields of relative degree dividing `r-1` suffice; their compositum is unnecessary. Fixed embeddings and actual field conversion remain computational requirements. No claim about arbitrary surface endpoints follows from this elliptic argument.

At a marking prime, form the weak tuple `Z` for `(Psi sigma^-1)^8` in the old model and output

    q([Delta^-1] C Z).

Under the proof isomorphism `u`, this is exactly the original projective tuple. Hence it marks an actual `D`-polarized map from `E0^16` to `Y`. The unknown `D` is the SAME for every query. The trace-free rigidity proof uses only this common multiplier, not its primality or separability. Substituting its upper bound `U=p*m` into

    Rmark^2 > 8 * 16^3 * U^2

therefore suffices. ONE polarized isomorphism must align every marking level. Independent automorphisms, coefficient-field Frobenius minimization, or unpolarized isomorphisms are not allowed; the retained counterexamples explain why.

This proves the desired conditional equality relation for subgroup SCHEMES. The connected p-part is fixed by every integral source endomorphism via relative Frobenius naturality. Thus only the doubled separable kernel moves. Unknown degree or a connected kernel does not by itself spoil separation.

### Unknown Depth And Hidden Subgroup Recovery

References: [SUBORDER_TRANSCRIPT.md:173](/Users/jaspersands/Developer/qsearch-research-work/suborder-transcript-2026-10-25/SUBORDER_TRANSCRIPT.md:173), lines 173-199; [CYCLIC_ODD_DEGREE.md:143](/Users/jaspersands/Developer/qsearch-research-work/cyclic-odd-degree-source-2026-10-25/CYCLIC_ODD_DEGREE.md:143), lines 143-242; [DOUBLE_LEVEL_SOURCE.md:185](/Users/jaspersands/Developer/qsearch-research-work/double-level-source-2026-10-25/DOUBLE_LEVEL_SOURCE.md:185), lines 185-224.

For `K_ell = ell^(e-k) R v`, the two unipotent tests give thresholds `max(0,k-2 val(y))` and `max(0,k-2 val(x))`. A primitive vector has a unit coordinate, so their maximum is exactly `k`. There is no parity condition on `e-k`. Reusing the older scalar-content formula would be wrong, but the new note expressly prohibits it.

The receiver's affine queries lift to determinant-one matrices at the full ambient level. No ring section `Z/ell^k -> Z/ell^e` is assumed. The scaled kernel depends only on the reduction of a query modulo `ell^k`, which is exactly what is required.

On a good chart, the source fibers are those of `t*z+u`. Fourier sampling at unit frequency followed by the full additive-ring Fourier transform has correct-candidate probability `(ell-1)^2/(2*ell^2) >= 2/9` for odd `ell`. This does not require finite-field Gauss-sum results over a local ring. Trying both charts and using the full doubled-source certificate is important: the restricted one-factor `SL2` stabilizer alone can collide modulo 9.

The second certificate query enforces `xy=0`; the first enforces `y^2=0`. For primitive `(x,y)` over a local ring, together they force the candidate line exactly. The scaled-prefix version enforces the claimed prefix. The deterministic small-prime recovery cost is `2(ell*k+1)` comparisons, so bounded-small-prime families do not support a superpolynomial quantum advantage from this receiver.

This is a specialized recovery argument conditional on the exact label oracle, not a claim that arbitrary nonabelian HSP is efficient. No native classical hardness is established at large primes.

### Exact Target Order And Effective Basis Maps

References: [SUBORDER_TRANSCRIPT.md:201](/Users/jaspersands/Developer/qsearch-research-work/suborder-transcript-2026-10-25/SUBORDER_TRANSCRIPT.md:201), lines 201-221; [CYCLIC_ODD_DEGREE.md:244](/Users/jaspersands/Developer/qsearch-research-work/cyclic-odd-degree-source-2026-10-25/CYCLIC_ODD_DEGREE.md:244), lines 244-258.

Recovering the separable kernel determines its LEFT annihilator ideal `I_sep`, of norm `d`. At every prime other than `p`, the pulled-back target Tate lattice gives exactly its right order. At `p`, both orders are the unique maximal order of the quaternion division algebra. Equality of all localizations gives equality of the actual rational lattices:

    O_R(I_sep) = theta^-1(End(E)).

This is stronger than saying that the orders are abstractly isomorphic. It does not select an isogeny/Frobenius branch. For `m=1`, the same argument gives `O0` directly. The known-principal-ideal fixtures are checks of a special case, not the proof of this general statement.

The final effective-output dependency can be made explicit without target-order advice. Since `d O0 <= I_sep <= O0`, any `x` in the right order satisfies `a=d*x in O0`. Compute a basis of the right order by the linear lattice conditions `I_sep*a <= d I_sep`. For each resulting basis element, construct the KNOWN map

    alpha = theta(N*a) in R,
    theta(x) = alpha/(N*d).

Its evaluator is assembled from the original known `theta(N*b_i)` evaluators and integer coefficients. Its degree is obtained from the rational algebra norm. For a nonzero integral output basis element and denominator `b=N*d>1`, `deg(alpha)=b^2*deg(theta(x)) >= b^2 > b`, meeting the division theorem's size condition; `b=1` needs no division.

Herledan Le Merdy--Wesolowski, [Theorem 4.1 and Algorithm 1, version 4](https://arxiv.org/html/2309.11912v4#S4), take an efficiently represented isogeny and an integer divisor and return an efficiently evaluable quotient when it exists. The stated interface does not require the divisor to avoid `p`. The auxiliary levels avoid `p*deg(alpha)`, not the divisor's prime factors alone. Theorem 4.22 explicitly charges torsion generation and evaluations. Thus the final division is a legitimate imported algorithm, not a disguised solution of EndRing. It has not been executed here.

Bound the HNF/right-order coefficients, numerator evaluator lengths, denominator bit lengths and norm heights in the theorem's resource statement. This closes the effective-output argument conditionally on the cited exact evaluator contract; an abstract quaternion order alone is still not an effective output.

## Published Interfaces Checked

The retained primary PDFs, not just their abstracts, were read for the interfaces used above.

| Dependency | Exact inspected interface | Review conclusion |
| --- | --- | --- |
| Corte-Real Santos--Piasecki--Wesolowski, [ePrint 2026/1142](https://eprint.iacr.org/2026/1142), retained 44-page PDF, pp.10-15 | Remark 3.2; A1-A8; A18-A20; A22/A25/A26/A27 | Semantic representability is not conversion. A26 really accepts a full maximal-isotropic subgroup list and specifies the subgroup's definition field. Composition encodings have an explicit additive length bound. |
| Same PDF, pp.24-28 and 33-36 | Theta encodings; Proposition 6.3; Lemmas 6.17/6.22; Proposition 6.19; Proposition 6.24; Theorem 6.25 | Fixed-dimensional represented-object isomorphism, automorphism, canonicalization and quotient algorithms are the relevant imports. These statements do not directly turn arbitrary informal polarization data into a model. |
| Same PDF, pp.36-38 | Theorem 7.1 and Algorithm 6 | Both polarized endpoints must already be represented; multiplier and auxiliary order are coprime to characteristic, auxiliary order exceeds multiplier, and exact basis images are required. This is not a direct converter for the unknown-degree repolarized object. The proposed quotient route avoids invoking it there. |
| Chen--Petit accepted manuscript, retained PDF pp.4, 8-18 (printed pp.3, 7-17) | Theorems 1/3; Section 2.3; Definition 13; Remark 17; Lemmas 18/20/22; Propositions 24-26; Remark 27 | Prior quantum full-suborder/weak-IsERP results and their heuristics remain relevant. Pointwise weak generators are not a common-scalar basis promise. The new direct intertwiners avoid that interface mismatch in this application. |
| Herledan Le Merdy--Wesolowski, arXiv:2309.11912v4, Section 4 | Theorems 4.1/4.22, Algorithm 1 and proof of Theorem 4.1 | A precise effective-output dependency exists. Use exact known suborder maps as its input, not projective samples or a supplied unknown isogeny. |
| Pollack--Trevino, [Finding the Four Squares in Lagrange's Theorem](https://math.colgate.edu/~integers/sjs15/sjs15.pdf), pp.1-2 | Unconditional randomized variants and bit-cost conversion | Expected polynomial four-square construction need not introduce ERH. This does not certify the clock of the local SymPy witness finder. |
| Morrison--Panny--Sotakova--Wills, [arXiv:2501.16321v2, Section 2.2](https://arxiv.org/html/2501.16321v2#S2.SS2) | Supersingular Frobenius classification context | The note's explicit twelfth-power derivation, rather than a blanket six-power fixed-endpoint claim, is the appropriate field argument. |

I did not independently re-prove all algorithms inside these papers or all their cited dependencies. Published algorithm hypotheses remain assumptions of the composition. No claim of a correction to a paper or of novelty follows from this audit.

## Resource And Evidence Ledger

- **Deductive, with stated mathematical hypotheses:** primitive global implementer; `D | p*m`; projective auxiliary intertwiners; half-polarization integrality; the norm/quotient/mark transport identities; joint marked separation; depth and line certificates; exact transported right order.
- **Conditional algorithmic claims:** source evaluation using the published PPAV model; uniformly bounded coherent compilation; the initial native-input and theta conversions; effective target maps via published division. Findings 1-3 specify the missing theorem-level contracts.
- **Finite-tested by this review:** a separate in-memory exact-arithmetic check for primes 2, 3, 5, ambient exponents 1 through 3, every permitted kernel depth, and every projective direction. It checked 342 depth cases, 26,283 full-level candidate/true-line certificate pairs, and 76,323 candidate-prefix pairs in total. All passed. The tests used explicit finite subgroups and determinant-one frames, not an oracle that simply returned the formula under test.
- **Previously reported, not rerun here:** the 451-test aggregate and receipt results in the suborder verification note. Reading those records does not turn them into independently reproduced geometric results.
- **Unexecuted:** native elliptic-to-theta conversion, actual small-prime curve transcript, geometric quotient sequence, canonical marked label, coherent source circuit, unknown-kernel quantum recovery, and effective target order on an unknown native input.
- **Not established:** a native classical lower bound, a quantum advantage over all matched native algorithms, practical dimension-16 performance, or novelty.

For resource accounting, `log(T)` is polynomial in `log(m)` and the paid source basis heights. Excluding prime divisors of `pN` removes at most `O(log(pN))` total logarithmic prime mass. Successive-prime products therefore reach both the quotient and marking thresholds using polynomially bounded primes and polynomially many levels. Retain the explicit dependence on the input basis/evaluator lengths, not just `log(p)` and `log(m)`.

The `r^2` transcript tables, `r^16` quotient lists, fixed-dimensional theta coordinates and automorphism orbit, per-level point-field degrees, and all known-map evaluation costs belong in that polynomial. None is polynomial in the bit length of an arbitrary large auxiliary prime. The plan works by selecting small auxiliary primes, not by making large-prime torsion cheap.

The unknown actual degree does not require a search over its divisors. `m` controls the lift and recovery domain; `p*m` controls marking separation; `Delta` controls computed quotients; learned `d` controls the separable ideal. Conflating these quantities would invalidate the reduction.

## Dependency Inventory And Scope

Read from the permitted local research root:

- [RESEARCH_CHECKPOINT_2026-10-23.md](/Users/jaspersands/Developer/qsearch-research-work/RESEARCH_CHECKPOINT_2026-10-23.md), first 180 lines.
- [SUBORDER_TRANSCRIPT.md](/Users/jaspersands/Developer/qsearch-research-work/suborder-transcript-2026-10-25/SUBORDER_TRANSCRIPT.md), [HANDOFF.md](/Users/jaspersands/Developer/qsearch-research-work/suborder-transcript-2026-10-25/HANDOFF.md), and [VERIFICATION.md](/Users/jaspersands/Developer/qsearch-research-work/suborder-transcript-2026-10-25/VERIFICATION.md); the transcript implementation and supplied-map controls; selected test/replay declarations.
- [DOUBLE_LEVEL_SOURCE.md](/Users/jaspersands/Developer/qsearch-research-work/double-level-source-2026-10-25/DOUBLE_LEVEL_SOURCE.md), its handoff, source arithmetic implementation and selected verification declarations.
- [PPAV_SOURCE_DECISION.md](/Users/jaspersands/Developer/qsearch-research-work/ppav-source-2026-10-23/PPAV_SOURCE_DECISION.md), its handoff and retained primary PDF.
- [LARGE_PRIME_AUDIT.md](/Users/jaspersands/Developer/qsearch-research-work/large-prime-source-audit-2026-10-25/LARGE_PRIME_AUDIT.md), [SOURCE_MANIFEST.md](/Users/jaspersands/Developer/qsearch-research-work/large-prime-source-audit-2026-10-25/SOURCE_MANIFEST.md), and the retained Chen--Petit accepted manuscript.
- [SMOOTH_REPOLARIZATION.md](/Users/jaspersands/Developer/qsearch-research-work/smooth-repolarization-2026-10-23/SMOOTH_REPOLARIZATION.md), [PRIME_ONLY_SOURCE.md](/Users/jaspersands/Developer/qsearch-research-work/prime-only-source-2026-10-25/PRIME_ONLY_SOURCE.md), [CYCLIC_ODD_DEGREE.md](/Users/jaspersands/Developer/qsearch-research-work/cyclic-odd-degree-source-2026-10-25/CYCLIC_ODD_DEGREE.md), and [ODD_CONTENT_REDUCTION.md](/Users/jaspersands/Developer/qsearch-research-work/odd-content-reduction-2026-10-25/ODD_CONTENT_REDUCTION.md).
- [FIELD_NORMALIZATION.md](/Users/jaspersands/Developer/qsearch-research-work/elliptic-field-normalization-2026-10-25/FIELD_NORMALIZATION.md), [SOURCE_FIELD_AUDIT.md](/Users/jaspersands/Developer/qsearch-research-work/source-field-audit-2026-10-23/SOURCE_FIELD_AUDIT.md), and [KERNEL_TO_OUTPUT.md](/Users/jaspersands/Developer/qsearch-research-work/kernel-output-2026-10-23/KERNEL_TO_OUTPUT.md).
- The locally retained [RETAINED_MARKED_RIGIDITY.md](/Users/jaspersands/Developer/qsearch-research-work/one-endomorphism-access-audit-2026-10-25/RETAINED_MARKED_RIGIDITY.md) snapshot, solely to inspect the original rigidity dependency without accessing its Desktop pointer. Its SHA256 matches the checkpoint's recorded snapshot.

I did not follow the snapshot's missing original-source pointers into Desktop. I did not review the new polarization-completion lead. The older surface-output and field notes were inspected only for dependencies used by the requested doubled-elliptic composition; their unrelated research directions were not audited.

Selected SHA256 identifiers checked during this review:

| Input | SHA256 |
| --- | --- |
| Suborder transcript note | `3c47ff597405c0b8efe9b944d86c086d4df10822fe5304e6021a4e8def5539b1` |
| Double-level source note | `af20f05d6a1c0ee7a88658d045ebc8b32d6ce4bf682c83a22fe3f7bf05fc5aac` |
| PPAV decision note | `67dc27018fe5e796315ffd670977bbff42532b52eb119b16171ae6055e31c37c` |
| Retained PPAV PDF | `4504310844c227e0d49c8c628b03e9942894f14fcd6f5881dc5c0122ed645318` |
| Retained Chen--Petit PDF | `554c6a9f0f49cc13a59e38bf20a351a797137938dce18bd546a9ecf47a656402` |
| Retained marked-rigidity snapshot | `7dc0b41c1dc76dddb6b8ec385fbf25f11ca814da02cf8d27fdef0065b3a0d034` |

## Final Assessment

The reviewed algebra supports a conditional route from the explicitly equipped full-suborder input to the exact effective target order, with no identified circular use of the hidden map or target order. The unknown degree and inseparable component are handled coherently. The source construction is materially more than an algebraic fixture: its quotient and marking formulas have the right geometric semantics under the published model interfaces. Conversely, fixtures alone have not executed those interfaces.

Retain the narrow input and algorithmic hypotheses until Findings 1-3 are closed in a single resource-accounted theorem statement. Preserve the native/classical comparison and all execution-status distinctions. This review neither supplies a formal proof certificate nor establishes novelty or advantage.

Changed paths: only `/Users/jaspersands/Developer/qsearch-research-work/combined-source-independent-review-2026-10-25/REVIEW.md`.
