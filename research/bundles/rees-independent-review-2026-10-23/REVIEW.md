# Independent Adversarial Review of the Frozen Rees HSP Proof

Date: 2026-10-23. One reviewer; no other agents. Mathematical correctness review, not implementation, endorsement, formal verification, or novelty review.

The manuscript was read and the central reduction reconstructed before reading the secondary reduction note and self-audit. Previous tests and the self-audit's conclusions were not premises. Only the three supplied snapshot files and the primary literature identified below were consulted for the mathematical claims. No Desktop, migration-staging, Git, or orthogonal-HSP work was performed.

## Findings, Ordered by Severity

**No fatal counterexample was found to the explicit prime-field fixed-class theorem or to its core Rees/central-descent composition.** I also found no incompatible input promise in the stated black-box extension after checking its large-prime and bounded-prime branches. This is a bounded review result, not a certificate that the theorem is correct.

### F1. The Variable-Class Corollary Must Use the Actual Class, Not an Arbitrary Upper Bound

Classification: low-severity, repairable parameter-convention/exposition issue with a real resource consequence under the literal input contract. It is not a fatal counterexample to the fixed-class theorem and not a new hard mathematical obligation.

Locations: [manuscript, lines 40-41](/Users/jaspersands/Developer/qsearch-research-work/rees-independent-review-2026-10-23/source/rees_hsp_review.tex:40), [lines 373-374](/Users/jaspersands/Developer/qsearch-research-work/rees-independent-review-2026-10-23/source/rees_hsp_review.tex:373), [lines 432-445](/Users/jaspersands/Developer/qsearch-research-work/rees-independent-review-2026-10-23/source/rees_hsp_review.tex:432). The original contract says class **at most** c; the parameter proof subsequently uses c <= r+1 without explicitly replacing c by the actual class.

Reconstructible counterexample to that intermediate assertion: take the three-dimensional Heisenberg Lie algebra over F_p, p >= 5, with [x,y]=z and all other basis brackets zero. Its derived dimension is r=1 and its actual class is 2. It satisfies the original contract with c=p-1, but c <= r+1 would say p-1 <= 2. If the stipulated c-evaluation lift is literally run with that c, even one lifted source costs p-1 original inputs. For fixed n=3 and r=1 this is not polynomial in log p, as the auxiliary parameter bound requires. Extra zero grades do not eliminate the expressly counted c evaluations by themselves.

Local repair, with proof: first compute successive lower-central spaces by field linear algebra and let ell be the last nonzero index. If gamma_d=gamma_(d+1) is nonzero, all subsequent terms coincide, contradicting nilpotence. Thus the nonzero terms strictly decrease. Starting from dim gamma_2=r, this gives ell <= r+1 and dim gamma_d <= r-d+2 for 2 <= d <= ell. Replace c by ell in the cover, evaluation points, BCH truncation and copy counts. This preprocessing takes polynomial time in n and log p, with at most n strict decreases, and the displayed parameter proof then goes through. No source reads are needed for this correction.

If the authors intended c to mean the actual class throughout Section 6, this is just an unstated convention. It should still be explicit because the inherited input promise is different. No source manuscript was changed here.

### Classification Summary

- Fatal counterexample to the advertised fixed-class theorem: none found.
- Actual unproved mathematical obligation in the core: none identified in the arguments reconstructed below, relative to the stated published ingredients. Uninspected proofs inside imported algorithms are residual review limits, not evidence of a gap.
- Exposition/resource qualification: F1 above. Its correction is constructive and does not require a new theorem.

## Independent Reconstruction of the Core

### 1. Input and Access Promises

Locations: [manuscript, lines 40-71](/Users/jaspersands/Developer/qsearch-research-work/rees-independent-review-2026-10-23/source/rees_hsp_review.tex:40), [lines 142-207](/Users/jaspersands/Developer/qsearch-research-work/rees-independent-review-2026-10-23/source/rees_hsp_review.tex:142).

The field must be the prime field. For the exponent-p Lazard group, subgroup closure corresponds to Lie-subalgebra closure, hence F_p-linearity. Arbitrary subgroups need not be linear over a larger coordinate field; that stronger promise is not used here. Genuine structure constants, c<p, and the charged public arithmetic are substantive assumptions, not properties inferred from finite checks.

The ordinary oracle is a coherent fixed-width XOR oracle separating left cosets gH. The alternative resource is fresh independent mixed coset states, not an inverse state-preparation circuit. These are different interfaces; the proof does not reconstruct the first from the second.

With R_g|x>=|x g^(-1)>, one has R_a R_b=R_(ab) and Tr(rho_H R_g)=1_H(g). If phi_i are public evaluation homomorphisms, controlled R_(phi_i(a)) on independent target copies gives the address matrix

    rho_out[a,b] = |A|^(-1) product_i 1_H(phi_i(b)^(-1) phi_i(a)).

The order b^(-1)a is correct; H need not be normal. Cleanup of public evaluation workspaces is essential and is explicitly required. The product uses independence, not merely correct one-copy marginals.

The weaker raw-bank promise at lines 160-186 is also sufficient: the independent left-twirl channel maps each ideal |aH><aH| to the same rho_H. Applying it to each factor in the stated positive operator-valued mixture yields rho_H tensor powers, tensor the unchanged side-information marginal. The translation records must be discarded. This argument does not extend to arbitrary separable banks. The opposite-character example at lines 193-200 is consistent with that limitation.

### 2. Rees Lift and Final Quotient

Locations: [manuscript, lines 79-125](/Users/jaspersands/Developer/qsearch-research-work/rees-independent-review-2026-10-23/source/rees_hsp_review.tex:79), [lines 284-292](/Users/jaspersands/Developer/qsearch-research-work/rees-independent-review-2026-10-23/source/rees_hsp_review.tex:284).

The bracket on A=sum_(r=1)^c t^r gamma_r(L) is inherited from L[t]. For r+s>c the bracket is actually zero, since [gamma_r,gamma_s] lies in gamma_(r+s)=0. Evaluation therefore preserves brackets and BCH; there is no illicit evaluation of a truncated coefficient ring at a nonzero scalar.

For C=log(a^(-1)b), tuple equality is equivalent to E_(s_i)(C) lying in h for every i. Work in the vector-space quotient L/h; h need not be an ideal. The invertible nonzero-point Vandermonde matrix forces every coefficient C_r to vanish in L/h. Thus the exact hidden subalgebra is

    h_tilde = direct_sum_r t^r (h intersect gamma_r(L)).

It is closed under brackets and preserved by every nonzero dilation. Its description is used in the proof, not queried by the algorithm.

Let J_(>d)=sum_(r>d) A_r. This is a homogeneous ideal; in A/J_(>d), A_d is central and is scaled by s^d. The image of h_tilde stays dilation invariant. At the last quotient, A/J_(>1)=tL is additive. Projection of h_tilde is exactly t h, not h modulo [L,L]. This establishes why successive quotient conversion recovers the original hidden subspace rather than just its abelianization.

### 3. Central Branch Law and Pointwise Cancellation

Locations: [manuscript, lines 210-282](/Users/jaspersands/Developer/qsearch-research-work/rees-independent-review-2026-10-23/source/rees_hsp_review.tex:210).

For a central elementary abelian Z, the character sums Pi_lambda are a complete family of orthogonal spectral projectors for the right action of Z. They commute with rho_H. Put K=H intersect Z. Taking the regular trace gives

    Pr(lambda) = |Z|^(-1) sum_(z in K) chi_lambda(-z),

which equals |K|/|Z| on K-perp and zero elsewhere. Division by this positive branch mass gives the manuscript's coefficient 1/(|G||K|). In Tr(rho_lambda R_g), nonzero terms require hz=g^(-1); for g=h0 z0, their character is chi_lambda(z0), with exactly |K| equal contributions. This establishes the trace formula, including its sign and normalization, without assuming normality of H or a trivial central intersection.

Now fix a positive-probability tuple of labels and any nonzero witness satisfying sum_i s_i^d lambda_i=0. For g=sigma(r)^(-1)sigma(q), an active factor has zero trace when g is outside HZ because Delta_s preserves HZ. If g=h z, its trace is chi_lambda(s^d z); their product is one. Therefore the address kernel is precisely

    |Q|^(-1) 1_(HZ/Z)(r^(-1)q).

This works for a nonhomomorphic section: only its projection to q or r is used. It does not use an average phase, a typical tuple, or a hidden coset representative.

Zero scales are discarded, not applied as automorphisms. An all-zero witness would make the empty product one off the correct support and is rightly forbidden. A zero character is a legitimate branch. If H contains Z, it is the only character and has probability one. Forbidden characters cannot be normalized and are not inputs to the branch identity.

### 4. Adaptive Records, Character Support and Density

Locations: [manuscript, lines 247-282](/Users/jaspersands/Developer/qsearch-research-work/rees-independent-review-2026-10-23/source/rees_hsp_review.tex:247), [lines 330-345](/Users/jaspersands/Developer/qsearch-research-work/rees-independent-review-2026-10-23/source/rees_hsp_review.tex:330).

Let T include the complete current label tuple and solver randomness. On every successful exact record t, the retained state is the same rho_(HZ/Z). Consequently the joint classical-quantum output is

    sum_t Pr(T=t, success) |t><t| tensor rho_(HZ/Z).

Conditioning on any collection of successful records does not bias the retained state. With disjoint fresh inputs this gives the induction needed for independent source states at the next level, even when scale selection uses all labels. This is stronger than an unconditional averaged identity.

No inverse-polynomial mass bound for any particular field character is needed. The support K-perp can be tiny or huge, and the zero-label mass can be exponentially small. The diagonal solver accepts every label list of the sufficient arity. There is no favorable-character postselection in the field core.

Classical retries use saved labels and independent classical seeds before the controlled actions. They do not require replacement quantum targets. The uniform expected-time hypothesis in the retry lemma is genuinely necessary for its Markov argument; the cited deterministic general SDE algorithm provides a stronger alternative. Approximate implementations must be compared as complete instruments with records and abort outcomes; normalized rare-branch error estimates would not suffice.

### 5. Uniform Complexity and Output

Locations: [manuscript, lines 294-367](/Users/jaspersands/Developer/qsearch-research-work/rees-independent-review-2026-10-23/source/rees_hsp_review.tex:294).

The stated sufficient arity B_d(r) is consistent with the collision construction in the primary SDE paper. For delta=gcd(d,p-1), choose u with du=delta modulo p-1; applying x->x^u to nonzero witness entries and retaining zero entries gives the required dth powers. For delta=1 the required solver is just linear dependence. For r=0 any nonzero scale vector works.

At fixed c, D<=cn, each B_d(r_d) is a fixed-degree polynomial in n, and P=product_(d=2)^c B_d(r_d) is polynomial. There are mP lifted leaves and the stated sum of merge counts: a stage-d merge requires product_(j=2)^(d-1) copies of that merge per terminal root. Each lifted leaf consumes c original calls or copies. This is a time/copy bound, not a claim that the tree is practically small.

The final quotient state has uniform Fourier distribution on h-perp. For a space of dimension k<=n and m=n+t independent samples, union-bounding over the (p^k-1)/(p-1) nonzero dual directions up to scalar gives rank failure less than p^(-t)/(p-1). Nullspace recovery returns the full h. Taking more samples supplies log(1/epsilon) amplification without voting on noncanonical bases.

The source, merge and terminal-readout counts all enter the precision allocation. Contractivity through the adaptive channel composition bounds total deviation by the sum of complete-channel errors, without dividing by small outcome probabilities. The solver-abort and rank budgets fit the remaining allocation. The c=1 case requires only abelian readout and has no SDE retry expression to evaluate.

## Auxiliary Extensions Checked

### Derived-Dimension Extension

Locations: [manuscript, lines 376-445](/Users/jaspersands/Developer/qsearch-research-work/rees-independent-review-2026-10-23/source/rees_hsp_review.tex:376).

Subject to F1, the public central-flag argument is valid: every subspace of the current top grade is an ideal and is invariant under scalar dilation, even if it is not adapted to the hidden intersection. The scalar solver has the required uniform degree dependence. With actual class ell, summing dim gamma_d <= r-d+2 yields D<=n+r(r+1)/2 and at most r(r+1)/2 scalar removals. Their arities are <=r+2, giving the displayed exponential parameter factor.

I independently checked the BCH differential identity's orientation. For exp Z(t)=exp X exp(tY), the left logarithmic derivative is Y, so ((1-exp(-ad_Z))/ad_Z) Z'=Y. Inversion gives the stated +1/2 coefficient and recurrence. Working through t-degree c only requires divisions by integers <=c, hence no denominator obstruction when c<p. Polynomial bracket convolution gives O(c^4) brackets; no exponential enumeration of free words is needed for explicit input. This reasoning also applies over the torsion rings in the next section because these denominators are units.

### Explicit Prime-Power Lie Rings

Locations: [manuscript, lines 471-545](/Users/jaspersands/Developer/qsearch-research-work/rees-independent-review-2026-10-23/source/rees_hsp_review.tex:471).

Evaluation at 1,...,c has unit Vandermonde determinant modulo p^E, so the coefficient-membership argument works in the actual finite modules. It does not require free gamma_d modules. At each removed cyclic central factor of order p^a, an intersection of order p^b has annihilator p^b Z/p^a. The positive labels are uniform on that annihilator.

If a zero label occurs, that target alone works. Otherwise, on the accepted common-valuation v branch, the coefficients after division by p^v are units. A nonzero mod-p solution has at least one nonzero coordinate, whose derivative d A_j s_j^(d-1) is a unit because d<p. Hensel lifting that coordinate while keeping the others fixed preserves zero-or-unit active scales and gives exact cancellation modulo p^a. Singular nonunit dilations are not used.

For b<a, the event that every one of B<=p labels has minimum possible valuation b has probability (1-1/p)^B >= (1-1/p)^p >= 8/27 > 1/4 for odd p. For b=a, all labels are zero. Thus the asserted uniform success lower bound holds without knowing b. This is the only acceptance-density argument in these extensions; it is not a field-core character-density assumption.

Each accepted record produces the same quotient state, independent of its prior cost history. Hence fresh recursive preparations satisfy the conditional source law, and conditional expected leaf costs multiply by at most 4B per factor. The whole-run Markov cap is legitimate; it avoids pretending each individual retry has a deterministic four-fold cost. The leaf/node instrument bound, additive p-group sampling bound, and HNF-canonicalized majority amplification have the stated constant-error margins. The ring argument correctly does not infer c<=r+1 from additive generator rank.

### General Black-Box Extension

Locations: [manuscript, lines 564-684](/Users/jaspersands/Developer/qsearch-research-work/rees-independent-review-2026-10-23/source/rees_hsp_review.tex:564).

This is a separate theorem interface: unique encodings, supplied generators, coherent public operations, and paid group/presentation preprocessing. It does not follow from running an explicit Lie-table routine directly on opaque encodings.

For a local exponent-p group with p>c, inverse-BCH words can be obtained by canceling the lowest erroneous homogeneous weight of a product or commutator, then iterating through c in the free Lie algebra. Word lengths depend on c; modular rational powers cost O(log p) public multiplications. Thus at fixed c the free class-c Lie algebra on s supplied generators has polynomial dimension and a polynomial-cost forward evaluation into G. Its map is surjective because the supplied group generators generate and the Lazard operations preserve subgroup closure. The kernel and the full hidden preimage need not be graded; the subsequent Rees lift is still necessary.

The forward homomorphism phi from this free group gives the copy kernel |F|^(-1)1_H(phi(b)^(-1)phi(a)); no inverse encoder or kernel-index postselection is required. Recovering the complete preimage and projecting its Lie basis yields generators for all H, not only some hidden intersection.

For the large-prime outer branch, the order-p promise belongs to each local call, not the original arbitrary H. The normalizer scan preserves this promise: the first nontrivial hidden intersection above a trivial one in an index-p chain has order p. A proper subgroup of a finite nilpotent H has a strictly larger normalizer inside H, so termination with no enlargement means H has been recovered. For p>c, the order-dividing-p elements form the public subgroup used by the cited reduction. This restriction would be invalid as a one-time replacement of arbitrary H.

For the bounded-prime branch, I checked the forward conversion in Imran--Ivanyos, rather than importing its exact source-inverse theorem. Its zero-sum construction consumes source copies using public right actions. Applying the manuscript's branch calculation with all active actions equal to the identity automorphism proves the same conversion for mixed copies. For p>2, degree p-1 witnesses give binary supports by Fermat; p=2 uses linear dependence. Ordinary bounded-error Fourier sampling after central descent needs no inverse hidden source. Public preprocessing may use reversible public circuits; that is a different resource.

The torsion-preimage qualification at lines 651-675 is correct. For a complete full-rank square row-relation basis R, the map

    {a mod p : aR=0 mod p} -> A[p],    a -> (a_lift R)/p mod row_Z(R)

is well defined: changing the lift adds a row-lattice element. It is injective because (a_lift-pv)R=0 implies a_lift=pv over Q, and surjective because any p-torsion class x has px=uR. Adjoining all generators of B gives the full preimage. The presence of B in this public computation does not license quotienting the hidden source by B; only H0 is used as that kernel. The nontrivial order-p element of (H intersect K)/H0 supplies the claimed invariant after restriction.

One can retain original-group lifts of the current public quotient generators and evaluate their words directly, so forward source sections need not recursively multiply their costs. The claimed polynomial bound on adaptive calls is compatible with the finite composition length. A first-error union bound is appropriate only with the stipulated clocks on erroneous histories and conditional correctness of every preceding public and hidden-subgroup call.

## Primary Literature Checks

These checks establish that the cited interfaces match; they are not independent reproving of all imported algorithms.

- [d'Elbee, Muller, Ramsey and Siniora, Section 2.3, Facts 2.13-2.14](https://arxiv.org/html/2310.17595v2#S2.SS3): checked exponent p, odd prime, class <p, scalar powering, subgroup/subalgebra correspondence and compatibility of maps. These are the hypotheses used by the prime-field input, not arbitrary characteristic-p group promises.
- [Ivanyos--Santha, Fact 2 and Sections 3.1-3.3](https://arxiv.org/pdf/1503.09016): Fact 2 explicitly has deterministic polynomial dependence on the scalar degree and log field size. Theorem 11 gives G(d,m)=d^(d(d-1)/2)(m+1)^d for d dividing q-1. Section 3.3 uses G(d,m)^ceil(log2(d+1)) inputs; Section 3 gives the gcd/exponent conversion. Thus the manuscript's more precise B_d bound is supported, including arbitrary label columns. No uniform-label hypothesis or p-sized search is imported. I did not reprove the entire algorithm or van de Woestijne's underlying scalar construction.
- [Ivanyos--Sanselme--Santha, Section 3, Theorem 2 and Lemmas 1-3](https://www.irif.fr/~santha/Papers/iss12.pdf): checked closure under subgroups and quotients, the local order-p reduction, and the large-prime order-p subgroup step. The paper discusses paid refined-polycyclic preprocessing for uniquely encoded black-box groups. I did not independently reimplement or reprove its normalizer/presentation subroutines.
- [Imran--Ivanyos, Section 4, Lemma 2 and Propositions 2-3](https://arxiv.org/pdf/2304.08376): checked the semi-elementary promise and the forward central-state conversion. Proposition 2 explicitly lists inverse-oracle access; Proposition 3's bounded-error statement does not. The forward conversion plus ordinary final Fourier sampling supports the mixed-copy route. The manuscript's explicit relation-lattice qualification must be retained when using the outer descent; arbitrary generator top powers are not a replacement.
- [Garaialde Ocana--Gonzalez-Sanchez, Theorem 1](https://arxiv.org/pdf/1405.4654): checked the class <p correspondence for finitely generated Z_p Lie algebras, including finite torsion examples, and subgroup/ideal preservation. This supports the ring extension's algebraic input model.

## Narrow Independent Exact Controls

Code: [exact_controls.py](/Users/jaspersands/Developer/qsearch-research-work/rees-independent-review-2026-10-23/exact_controls.py). Recorded stdout data: [exact_controls_results.json](/Users/jaspersands/Developer/qsearch-research-work/rees-independent-review-2026-10-23/exact_controls_results.json). Command: `python3 -B exact_controls.py`. Exit status: 0.

The program imports no project modules and uses rational arithmetic in Q[zeta_3], not floating phases. It computes the two-sided spectral projection Pi rho Pi in the regular group algebra, derives traces from inverse coefficients, and then constructs all quotient density entries for each tested complete branch. Linear independence of regular translation matrices makes these coefficient calculations faithful, not a replacement of the intermediate state by the predicted answer.

1. Rees lift of the Heisenberg Lie algebra over F_3 with nonnormal hidden line span(x+z). The original group has order 27 and the cover order 81. All 6,561 address pairs were checked for tuple-oracle fibers and copy-only overlaps, with 13,122 evaluation-homomorphism checks. Central descent used a deliberately nonhomomorphic section. All 27 positive label triples and all 234 valid scale witnesses across them produced the exact quotient density. Direct Fourier probabilities had nine supported frequencies, each of mass 1/9; their annihilator recovered exactly {(0,0,0),(1,0,1),(2,0,2)}.
2. Heisenberg(F_3) times C_3 with degree-two center span(z,w) and nonnormal H=span(x,z+w). Here |H intersect Z|=3. The exact spectral calculation gives three positive labels and six forbidden labels. All 27 positive triples and all 234 valid witnesses produced the same quotient density, checking 18,954 moment values and 18,954 address entries. The H-containing-Z control has only the zero label, of mass one.

Across both controls, the all-zero-scale negative control fails the support test, as it must. Zero scales in legal witnesses and zero measured characters are included. These are small degree-two controls for action order, normalization, selected labels, quotient sections and full original-subspace recovery. They do not test arbitrary class, a general SDE implementation, the black-box outer algorithm, physical noise, or a compiled quantum circuit. No broad benchmark or prior repository test suite was run.

## Remaining Unverified Scope

- This is not a machine-checked proof. No Lean artifact or quantum implementation was inspected or executed.
- The internal proofs of public black-box presentation/normalizer algorithms, the entire diagonal-system solver, and its underlying scalar solver were not independently reproduced. Their relevant stated hypotheses were checked as above.
- No gate-level circuit synthesis or independent proof of arbitrary-modulus approximate QFT was carried out. The resource review uses the standard polynomial-precision primitive assumed in the manuscript and checks its placement in the complete-channel error budget.
- The auxiliary Dixmier--Lister integer identities, its particular free-kernel relation, the UT_9 scope example, and numerical illustrative profiles were not independently recomputed. They are not premises of the main reduction.
- No novelty, classical-hardness, application, or practical-resource conclusion follows. The parent task's disjoint classical comparison was untouched.
- The finite controls are not evidence for the universal claim beyond their stated instances. The core mathematical conclusion above rests on the reconstructed identities and explicit imported hypotheses, not those controls.

## Frozen Snapshot and Files Created

SHA-256 fingerprints of the source files read:

    9f7d0693d0a90bc5a54e288bf4e6fb2514a1c49139ce17fea08d882621336182  source/rees_hsp_review.tex
    b759e35d150f15c29edcfa9118982b24be4ac2c59a4f46665c373b201de76847  source/REES_HSP_REDUCTION.md
    6fc3546138b663cb04d9d75774c4b29ebe95256546a4c78a0bf5a90939d95896  source/REES_WHOLE_PROOF_SCOPE_AUDIT.md

All writes were made with apply_patch inside this review directory, outside source/. Created: REVIEW.md, exact_controls.py, exact_controls_results.json. No supplied snapshot file was modified.
