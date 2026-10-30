# Independent Review: Dilation-Averaged Source Conversion

2026-10-25. Same single independently authorized reviewer as the earlier frozen Rees review. No other agents were used. The earlier review is complete, preserved and not a certificate for this new argument.

Scope: mathematical correctness of the new pure-state source lemma, its two spectral arguments, and the dependencies needed to connect its output to the existing receiver. Not novelty, applications, classical hardness, formal verification, or quantum implementation.

## Findings, Ordered by Severity

**No fatal counterexample was found to the source-conversion lemma under an exact unitary linear representation, fresh independent packet scales and the stated pure-state robustness promise.** Both spectral proofs survive the checks below, including their exceptional branches. One resource-scope qualification is needed if the final cost statement is read literally.

### F1. The Total Gate Bound Must Include Native Register Width and Coherent-Action Cost

Classification: repairable resource/accounting qualification; not a counterexample to the overlap bound or the native-copy count.

Locations: [DILATION_AVERAGED_SOURCE.md, lines 16-17](/Users/jaspersands/Developer/qsearch-research-work/rees-dilation-average-2026-10-25/DILATION_AVERAGED_SOURCE.md:16), [lines 250-263](/Users/jaspersands/Developer/qsearch-research-work/rees-dilation-average-2026-10-25/DILATION_AVERAGED_SOURCE.md:250); [dilation_average.py, lines 184-207](/Users/jaspersands/Developer/qsearch-research-work/rees-dilation-average-2026-10-25/dilation_average.py:184). The input says that U(g) is efficiently controlled, but the final list of polynomial parameters does not explicitly include the native state-register width or the cost of this supplied action. The planner bounds copies and scale samples; it does not establish that stronger gate bound.

Counterexample to interpreting the list as a complete, dimension-independent elementary-gate bound: fix p=131, dim L=1, delta=1/2 and a fixed sufficiently small total error. For arbitrary q congruent to 1 modulo p, let

    U_q(t) = diag(1, exp(2*pi*i*t/p)) tensor-power q,
    psi_q = (|0^q> + |1^q>)/sqrt(2).

This is an exact linear representation of C_p with an efficient O(q)-size controlled implementation. Its ray stabilizer is trivial. The only nontrivial subgroup twirl dephases the two components, giving trace distance exactly 1/2, so (P) holds with the same delta for every q. Nevertheless, implementing the supplied controlled action to sufficiently small fixed worst-case error requires touching all q data qubits. With bounded-arity gates this costs Omega(q), while the explicitly listed Lie dimension, log p, delta and total error stay fixed. This concerns the stated compiler's paid action gates, not an impossibility theorem for other symmetry-learning algorithms.

Repair: state a controlled-action query bound and a separate gate bound. Let q be the native register width and C_U(eta) the cost of a **uniform coherent** evaluation

    SELECT(U): |g>|v> -> |g> U(g)|v>

at the required whole-channel precision. The source uses at most Q=B*k*M native copies and Q such evaluations, with total action cost O(Q*C_U(eta)) plus the charged public arithmetic, sampling and receiver. Allocate eta across those Q uses. If U is a unit-cost oracle, say so and report query complexity; if it is a circuit, include its description/width and implementation cost among the inputs. Pointwise availability of separately controlled U(g) for classical g is not, by itself, a statement of uniform coherent SELECT access.

If "explicit dimension" was intended to include the native register and action description, F1 is an exposition correction. On the usual reading dim L, the literal all-cost statement is too broad. The group-dimension-independent *spectral estimate* itself is valid.

### Classification and Verdict

- Fatal counterexample to the new mathematical source lemma: none found.
- Unclosed mathematical obligation in the reconstructed conversion: none identified, relative to the imported results listed below. The old design implementation is not certified by this review; an independent sufficient constant-size design argument is supplied below.
- Resource/exposition issue: F1. The source-copy formula is consistent; its promotion to total gate time requires the stated access-cost qualification.
- No conclusion here certifies the old receiver implementation, the new bundle's implementation, or arbitrary approximate/noisy native sources.

## Exact Contract Used in This Review

The mathematical argument requires a unitary, genuinely linear representation U: G -> U(V), not a projective representation with an uncontrolled multiplier. The ideal native state is one fixed pure rho, and the consumed copies and packet scales are fresh as specified. L is an explicit prime-field Lie algebra of class at most three and p>=131. The cost discussion must use the coherent action interface in F1. I use TD(rho,sigma)=||rho-sigma||_1/2.

H is the ray stabilizer of psi and is a subgroup. The Lazard correspondence makes h=log H an F_p Lie subalgebra. No description of H, h, its ray character, or a subgroup twirl is an operational input. Promise (P) is universal over subgroups not contained in H; it is neither checked nor inferred from the finite controls.

## Independently Checked Algebra and Spectral Arguments

### 1. The Universal Curve Really Covers Arbitrary Ambient Lie Dimension

Location: [DILATION_AVERAGED_SOURCE.md, lines 35-54](/Users/jaspersands/Developer/qsearch-research-work/rees-dilation-average-2026-10-25/DILATION_AVERAGED_SOURCE.md:35).

For A_1 in L, A_2 in gamma_2(L), A_3 in gamma_3(L), put W_0=[A_1,A_2]. All brackets except [A_1,A_2] vanish among these four elements: W_0 lies in gamma_3, and any bracket involving A_3 or W_0 has weight at least four. Also [A_2,A_2]=0. Their span is therefore a quotient of the four-dimensional Lie algebra with only [X_1,X_2]=W nonzero. It is exactly Lie<A_1,A_2,A_3>, even when coefficients vanish or are dependent.

Passing through BCH gives the claimed homomorphism F -> K and sends gamma(t) to exp(t A_1+t^2 A_2+t^3 A_3). No assumption bounds dim L by four: the image of this *one coefficient-generated subalgebra* has dimension at most four, regardless of the ambient dimension. The induced image of uniform F is uniform K, so the invariant projection after pullback is precisely T_K.

Three distinct nonzero t values have an invertible coefficient matrix (t,t^2,t^3). The Lie algebra generated by their logarithms contains X_1,X_2,X_3 and then W. Thus the curve generates all F. This uses subgroup/Lie-subalgebra correspondence, not the false claim that arbitrary group products are ordinary sums of logarithms.

### 2. Nonlinear Irreducibles and the Cubic-Hankel Bound

Location: [DILATION_AVERAGED_SOURCE.md, lines 58-114](/Users/jaspersands/Developer/qsearch-research-work/rees-dilation-average-2026-10-25/DILATION_AVERAGED_SOURCE.md:58).

With ZX=omega XZ, multiplication of the displayed pi_(k,ell) contributes the extra phase k*b*a'. Substituting the group law into -kw+kab/2 gives exactly that phase. The sign of the central coordinate is therefore consistent with the stated group law. For k nonzero, clock and shift generate all matrix units, giving irreducibility. The two central characters distinguish (k,ell). There are p^3 linear characters and p(p-1) such p-dimensional representations; their squared dimensions total p^4. Standard finite-group representation theory then gives completeness.

For the curve mean, the column y moves to x=y+t, so the phase is c0*(x-y)^3+k*(x-y)^2*y. Expanding gives precisely the two mixed coefficients alpha=k-3c0 and beta=3c0-2k. If both are nonzero, x=(beta/alpha)u makes both mixed coefficients equal to beta^2/alpha. Subtracting the two pure cubics leaves lambda*(u+y)^3 with lambda=beta^2/(3alpha), which is nonzero. These are unitary row permutations and row/column phase multipliers, not similarity transformations whose singular values might change.

Column reversal yields the circulant with entries omega^(lambda*(u-y)^3)/p. Its singular values are the moduli of the normalized additive sums in the note, with no missing sqrt(p) normalization. The degree-three Weil estimate gives 2/sqrt(p).

The exceptional cases also check: alpha+beta=-k excludes simultaneous vanishing. For example, after removing the pure cubics, K[x,y]=omega^(beta*x*y^2)/p. Orthogonality of additive characters gives

    (K^* K)[y,z] = 1/p if y^2=z^2, and 0 otherwise.

The zero square fiber has size one; every occupied nonzero square fiber has size two. Thus ||K||^2=2/p. The other case is its transpose, which has the same singular values. No division by a zero mixed coefficient is justified or needed.

Every nontrivial linear character restricts to a nonconstant polynomial of degree at most three. Because p>3, it cannot become a constant polynomial function by reduction modulo t^p-t. Linear phases sum to zero; degree two and three obey their respective Weil bounds. Direct sums, multiplicities and pullbacks along F -> K preserve the operator bound on the complement of invariants. This also explains why neither large native Hilbert dimension nor nonfaithful U invalidates the spectral estimate.

### 3. Four-Step Regular Fibers: An Independent Derivation

Location: [DILATION_AVERAGED_SOURCE.md, lines 116-192](/Users/jaspersands/Developer/qsearch-research-work/rees-dilation-average-2026-10-25/DILATION_AVERAGED_SOURCE.md:116).

I derived the word using the upper-triangular Heisenberg matrix with (1,2) entry a, (2,3) entry b and (1,3) entry w+ab/2, keeping c as a separate additive coordinate. This independently gives the signed word polynomial in the note. Its Jacobian is

    6*(t0-t1)*(t1-t2)^2*(t2-t3)*(t0-t1-t2+t3).

Set d=t1-t0, e=t3-t2, g=t2-t1, m=(t0+t1)/2, n=(t2+t3)/2, D=n-m. In these variables D=g+(d+e)/2. Regularity is d*e*g*(e-d) nonzero. Counting choices t0,d,g,e gives exactly p*(p-1)^2*(p-2) regular inputs and singular mass 4/p-5/p^2+2/p^3.

Writing A=d+e, direct multiplication gives

    W = -(m^2*d+n^2*e)/2 + (d^3+e^3)/8 + d*e*D,
    C = 3*(m^2*d+n^2*e) + (d^3+e^3)/4,
    R = C+6W-A^3 = 6*d*e*(D-A/2).

For A nonzero, the quantity E in the note satisfies

    E = (R/(2A))*(D+A/2).

Thus D and q=d*e are uniquely recovered before choosing the at most two roots d,e of z^2-Az+q. Regularity makes them distinct. Once ordered, B=2(md+ne) fixes m and n. Every division used here has a nonzero denominator on an actual regular preimage.

For A=0, e=-d and D=g are nonzero. Hence B=-2dD is nonzero, R=3Bd, and C=(3B/2)(m+n). These identities give the stated unique inverse branch. This does not claim that singular fibers have bounded size; the p^2 identity examples remain singular and are charged to bad mass.

For unnormalized finite-group Fourier transforms hat(f)(pi)=sum_x f(x)pi(x), Plancherel gives sum_pi dim(pi)||hat(f)(pi)||_HS^2=|F|sum_x|f(x)|^2. Since nu_good<=2/p^4 and its mass is at most one, the right side is at most two. Each nonlinear block therefore has norm at most sqrt(2/p); the bad part adds at most 4/p by the triangle inequality for an average of unitaries.

Finally hat(mu_-)=hat(mu_+)^*. The alternating convolution is (M^*M)^2, whose operator norm equals ||M||^4. It is not M^4 and the proof does not confuse eigenvalue radius with singular-value norm. The numerical inequalities claimed for p>=131 are conservative and valid. Linear characters still need the separate additive-sum argument, so this alternate proof does not eliminate the linear-character use of Weil. No quasirandom-group theorem requiring absence of linear characters has been imported.

## Pure-State and Source-Channel Reconstruction

### 4. Subgroup Twirl to the Gap Seen by Native Copies

Location: [DILATION_AVERAGED_SOURCE.md, lines 194-217](/Users/jaspersands/Developer/qsearch-research-work/rees-dilation-average-2026-10-25/DILATION_AVERAGED_SOURCE.md:194).

Conjugation by U is a unitary representation on Hilbert-Schmidt space. Uniform subgroup averaging P=T_K is its orthogonal invariant projection. The curve mean M commutes with P and satisfies MP=PM=P. With rho=P rho+v and v orthogonal to the invariants,

    <rho,M rho> = ||P rho||_HS^2 + <v,Mv>
                <= ||P rho||_HS^2 + (7/8)||v||_HS^2.

The left side is real and nonnegative because rho is pure and each summand is an overlap modulus squared. Taking its real part in the inequality is legitimate even though M is not Hermitian. Since ||rho||_HS=1, this is the stated defect bound.

Idempotence/self-adjointness of P gives ||rho-P rho||_HS^2=1-Tr(rho P rho). The trace-distance inequality can also be obtained without a dimension-sensitive Schatten inequality: convexity of trace distance and the exact pure/pure formula give

    TD(rho,P rho) <= E_g sqrt(1-|<psi|U(g)|psi>|^2)
                  <= sqrt(1-Tr(rho P rho)).

The second inequality is concavity of square root. Thus (P) implies HS defect at least delta^2. There is no hidden factor of the native Hilbert dimension in this conversion. Purity is essential to the proof; the corresponding inference for arbitrary mixed rho is not asserted here.

If a is outside the homogeneous lift, some coefficient A_j is outside h. K contains exp(A_j), so K is not contained in H. This is the exact logical point at which promise (P) applies. The proof does not infer (P) from a few overlaps or only from the full-group twirl.

### 5. Zero-Moment Design and Ray-Character Cancellation

Location: [DILATION_AVERAGED_SOURCE.md, lines 219-244](/Users/jaspersands/Developer/qsearch-research-work/rees-dilation-average-2026-10-25/DILATION_AVERAGED_SOURCE.md:219).

For h in H, write U(h)psi=chi(h)psi. Linearity of the representation makes chi a group homomorphism. Since H has exponent p, chi takes pth-root values. Under Lazard, it has the form chi(exp X)=omega^(ell(X)), where ell:h -> F_p is linear and kills [h,h]. This follows by applying the subgroup correspondence to ker chi, or by passing to the abelianization. Therefore, for a in the homogeneous lift, the total packet phase is

    sum_(s in S) sum_(j=1)^3 (su)^j ell(A_j) = 0.

The packet overlap is exactly one, including u=0, without estimating chi. Repeated design entries count with their multiplicities. A projective multiplier would invalidate the homomorphism argument; the stated linear-action promise matters.

The original main-repository projective-source/design implementation is not present in these isolated dependencies and was not read or hydrated. I independently closed the needed class-three existence/complexity obligation as follows. Use the scalar quadratic diagonal theorem to obtain a nonzero solution of x1^2+x2^2+x3^2=0 over F_p. For each nonzero xi, include both xi and -xi in S. Then |S|<=6, all entries are nonzero, the first and third moments cancel in pairs, and the second moment is zero. If S had at most two distinct values, they would be {x,-x}; every active xi would have square x^2, so m*x^2=0 for an integer 1<=m<=3. This is impossible for p>3. Thus S has at least three distinct values. The scalar theorem has polynomial log(p) cost at degree two and can be independently witness-checked.

This is a sufficient check of the mathematical dependency, not a certification of the author's particular M<=24 construction or its code. Either a valid supplied design or the independent construction above suffices for the new lemma. No prime-sized multiset is needed.

Off the lift, choose any fixed nonzero design entry s0. All other overlap factors have modulus at most one. Consequently

    |E_u product_s f_s(u)| <= E_u |f_s0(u)|
                           <= sqrt(E_u |f_s0(u)|^2)
                           <= sqrt(1-delta^2/8)
                           <= 1-delta^2/16.

Multiplication by s0 is a permutation of F_p. This step uses the average bound just proved, not pointwise displacement of every non-symmetry. It also handles the legitimate u=0 identity branch; that branch is not an invertible receiver dilation and is never used as one.

### 6. Kernel Orientation, Independence and Adaptive Use

Location: [DILATION_AVERAGED_SOURCE.md, lines 224-254](/Users/jaspersands/Developer/qsearch-research-work/rees-dilation-average-2026-10-25/DILATION_AVERAGED_SOURCE.md:224).

For each fixed scale u, T_u is a representation because every E_(su) is a group homomorphism, including E_0. On the uniform address, tracing the native targets yields

    rho_out[a,b] = |A|^(-1) <Psi|T_u(b)^* T_u(a)|Psi>
                 = |A|^(-1) F_u(b^(-1)a).

Discarding the classical scale gives Fbar(b^(-1)a)/|A|. The result is a density matrix because it is an actual Gram/partial-trace construction, not merely a bounded arbitrary function. Nonnormal H does not permit replacing b^(-1)a by a b^(-1).

For k independent packet scales and independent native targets, the off-diagonal factor is the product of k expectations, Fbar(g)^k. A shared scale would instead give E_u F_u(g)^k. The distinction is a necessary source assumption, not a conclusion of the spectral gap. Retaining the scale as an adaptive receiver input likewise changes the contract: conditioned on u=0, the source carries no subgroup information at all.

With discarded scale records and fresh inputs on every requested leaf, the complete supplied bank is a product of identical approximate coset states. Conditional on any earlier receiver history, the next unused leaf still has its same state. A capped adaptive receiver may therefore be compared against an ideal bank using a trace-distance hybrid. There is no assertion that every normalized rare receiver branch is individually close. The receiver must not access the discarded source records or discarded targets, and no source inverse is available from this construction.

### 7. Amplification and Resource Quantifiers

Location: [DILATION_AVERAGED_SOURCE.md, lines 246-263](/Users/jaspersands/Developer/qsearch-research-work/rees-dilation-average-2026-10-25/DILATION_AVERAGED_SOURCE.md:246); dependency [SPECTRAL_MIXTURE.md, lines 178-188](/Users/jaspersands/Developer/qsearch-research-work/rees-spectral-mixture-2026-10-24/SPECTRAL_MIXTURE.md:178).

Let N=|A| and gamma=delta^2/16. Entries on the hidden subgroup agree exactly with the ideal coset kernel. Every remaining error entry has modulus at most exp(-gamma*k)/N. Therefore the Frobenius error is at most exp(-gamma*k), and

    TD(actual leaf, ideal leaf) <= sqrt(N)*exp(-gamma*k)/2
                                <= N*exp(-gamma*k).

The stated k is sufficient: ell>=log2 N and ceil(log2(4B/epsilon)) together upper-bound ln N+ln(4B/epsilon). Each leaf error is at most epsilon/(4B); summing over a deterministic cap B gives epsilon/4. Complex off-subgroup phases cause no problem for this entrywise norm bound.

This proves the native-copy count B*k*M and the identical count of controlled native action uses. It does not prove that an arbitrary user-chosen B suffices for a receiver; B must come from a valid capped receiver plan. For class at most three, D=dim A<=3 dim L and ell can be chosen polynomial in dim L and log p. The inherited fixed-class receiver supplies a polynomial B under its promises. Native-copy availability, q and the action cost are charged as in F1.

Uniform scalar sampling can use binary rejection with success greater than 1/2, capped with a union bound across B*k samples; this is public randomness, not hidden postselection. Each source-address preparation and each coherent action approximation needs its own paid allowance. Scaling their total error below the remaining budget gives a complete-channel bound. There is no additional 1/Pr(u=0), hidden-character density, or group-enumeration charge.

## Dependencies and Imported Results

1. **Weil's additive-character estimate is imported.** I checked the original [Weil, *On Some Exponential Sums*, PNAS 34 (1948), 204-207](https://www.pnas.org/doi/pdf/10.1073/pnas.34.5.204), especially equation (5) and the polynomial specialization on page 207. Here a nonconstant polynomial has degree d<=3<p and a nontrivial additive character; the relevant conductor is d+1, giving (d-1)sqrt(p). The cubic Hankel branch has nonzero cubic coefficient. No Artin-Schreier or characteristic-three degeneration is present. I did not reprove Weil's theorem.
2. **Finite-group representation theory is imported at the standard level:** complete reducibility, character orthogonality, the sum-of-squares completeness criterion, and Plancherel. The actual irreducible formulas, exceptional norms, Fourier normalization and use of these facts were independently checked above. No Babai--Nikolov--Pyber mixing theorem is required.
3. **Lazard subgroup/map correspondence and the existing Rees receiver remain imported dependencies.** This review checks that the new source supplies the same homogeneous hidden subgroup and an independent approximate mixed coset bank. It does not re-certify the previous receiver or convert a bag of mixed copies into an inverse preparation oracle.
4. **Scalar diagonal construction:** [Ivanyos--Santha, *Solving systems of diagonal polynomial equations over finite fields*, Fact 2](https://arxiv.org/pdf/1503.09016) explicitly states deterministic polynomial dependence on degree and log field size. I checked that interface and used it only at degree two in the independent design argument. Its underlying scalar algorithm was not independently reimplemented.
5. **Local amplification dependency:** only the source amplification/interface portions of [SPECTRAL_MIXTURE.md](/Users/jaspersands/Developer/qsearch-research-work/rees-spectral-mixture-2026-10-24/SPECTRAL_MIXTURE.md) are relevant here. Their norm argument was independently rederived above. The mixed-state spectral-filtering and density-matrix-evolution theorem is outside this review and is not certified by it.
6. **Local measurement dependency:** I read [UNIFORM_MEASUREMENT.md](/Users/jaspersands/Developer/qsearch-research-work/rees-uniform-measurement-2026-10-24/UNIFORM_MEASUREMENT.md). Its essential access distinction is correct: powers of public central translations are controlled additions by known residues, not exponentially repeated unknown-unitary calls. The compute/decode/uncompute comparison gives operator error sqrt(8rp/M) on all joint eigenspaces, and then a complete-instrument bound by contraction. This is compatible with approximate source inputs and adaptive hybrids. The address rejection and terminal rank arguments also match that contract. No compiled gate synthesis or implementation of that measurement was executed here.

## Independent Bounded Controls

Created [independent_controls.py](/Users/jaspersands/Developer/qsearch-research-work/rees-dilation-average-2026-10-25/independent_controls.py) and [independent_controls_results.json](/Users/jaspersands/Developer/qsearch-research-work/rees-dilation-average-2026-10-25/independent_controls_results.json). Command: `/opt/anaconda3/bin/python -B independent_controls.py`. Exit code 0. The program imports no code from the target bundle or related proof bundles and writes no files itself.

- The symbolic word is constructed from actual 3x3 matrix multiplication, with the additional central coordinate tracked separately. Its Jacobian and both inverse branches agree exactly with the claimed formulas. The cubic completion identity is checked as a rational-function identity, with alpha+beta=-k checked separately. These controls supplement the derivations above, not replace them.
- The source control uses G=Heisenberg(F_131), U=pi_1 direct_sum pi_2 and psi=(|1,0>+|2,0>)/sqrt(2). Its ray stabilizer is H={(x,y,z):x=z=0}, which is nonnormal. This instance satisfies (P) with delta=1/2: a subgroup with nonzero x projection has at most 1/p average squared overlap, hence trace distance at least 1-1/p; one with x=0 but nonzero central z projection dephases the two sectors, giving exactly 1/2. The remaining subgroups lie in H.
- The design is [1,130,1,130,28,103]; 28^2=-2 modulo 131. All three moments vanish, including multiplicities. Its small root search is explicitly diagnostic, not the scalable design algorithm.
- Native action on the two supported basis vectors is evaluated directly. Exact rational phase counts in Q[zeta_131] verify the kernel for 25 selected address pairs, without inserting the predicted coset matrix. For a=(1,1,0,1/2), b=(1,0,0,0) in the four-coordinate Rees cover, b^(-1)a=(0,1,0,0) gives overlap 1, whereas a b^(-1)=(0,1,0,1) gives 7/32. This detects the nonnormal orientation error rather than masking it with an abelian test.
- For the x-shift, a packet has overlap 1 only when its random scale is zero, and zero otherwise. Thus its average is 1/131, two fresh packet scales give 1/17161, and two shared scales give 1/131. This is an independently derived nonabelian negative control, not a defect in the stated fresh-scale construction. More generally a shared scale produces an error floor: the u=0 branch contributes the pure uniform address with weight 1/p. Measuring the uniform-address projector gives TD at least 1/p-|H_tilde|/|A|=1/p-1/p^3 on this instance, regardless of the number of packets.

The parent announced separate `source_independence_control.py` and `test_source_independence_control.py` during this review. They were not read, imported, run, edited or used as evidence. The author's original tests, replay receipt and finite spectra were also not run as proof premises. My controls are limited to the symbolic identities and selected exact source calculations just listed; they do not exhaust arbitrary states, groups, irreducibles or adaptive receiver transcripts.

## Explicit Certification Limits

- The conclusion is absence of a discovered fatal gap after the stated reconstruction, not formal verification or an unconditional certificate of the entire Rees program.
- The universal spectral conclusion depends on Weil and standard finite-group representation theory, not the finite controls. The arbitrary-ambient-dimension assertion follows from the quotient argument, not a test at one dimension.
- The pure input, exact linear action, robustness promise, discarded scale records and independent scales across *all* packets/leaves are substantive. None was certified for an unknown physical source. Mixed inputs, projective actions, correlated scales, coherent reuse and generic symmetry-breaking noise are not covered.
- Neither the older projective-source implementation nor its particular 24-member design was audited. The independent scalar construction above supplies a sufficient mathematical design, not a replacement implementation.
- The old Rees receiver remains a separate dependency. The new source does not grant an inverse or preserve access to discarded environments. Gate synthesis, hardware behavior, practical cost and end-to-end execution were not validated.
- No novelty, application or classical-comparison conclusion was investigated. No main/migrating repository, staging directory, prior independent review, or parent's disjoint work was changed.

## Read Versions and Created Files

The target proof and original diagnostics were fingerprinted during the review:

    d22c012b2e395738223094f7a8bf48f3210e64c80b78b238828f1d7c96dd9688  DILATION_AVERAGED_SOURCE.md
    fba379dc5cb6240cfe0209408bdc6769b60a77568a94f6ebf3e1af0702a283f4  dilation_average.py
    d3603cf2ffd8aeea0822bfad928a0c1aed0fc58764f7d3cd4d84219d0c8c96c4  test_dilation_average.py
    db4bc69012937f382349407f5fe34d82e07fe48fcdc9f84d48d0bd5c04797e9f  replay.py
    2e1f4c23539975bbfa169f6eff5e9aafc2878cc7aa69075adf8ff45ec8f19cd9  ../rees-uniform-measurement-2026-10-24/UNIFORM_MEASUREMENT.md
    b38e202c320037abd224196e13de193b9a146519a1c7c7b3427094b80b53f47c  ../rees-spectral-mixture-2026-10-24/SPECTRAL_MIXTURE.md

All reviewer writes used apply_patch in this isolated bundle. Created only REVIEW.md, independent_controls.py and independent_controls_results.json. The proof/code under review and the previous independent review were not modified.
