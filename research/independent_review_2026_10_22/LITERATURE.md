# Primary-literature comparison

Checked online on 22 October 2026. This is a targeted comparison, not an
exhaustive novelty certificate. The native problem here always retains its
explicit inverse-trace predicates, public points, arbitrary target bits,
and polynomial cost in n=log2(q), not in q.

| Primary source | Established contribution relevant here | Boundary for this construction |
|---|---|---|
| [Yamakawa–Zhandry, Verifiable Quantum Advantage without Structure, v3](https://arxiv.org/html/2204.02063v3), Sections 4–6 | Fourier source preparation, code addition, coherent decoding/erasure, and random-oracle search separation. Their suitable-code lemma uses complete list decoding to obtain average-error unique decoding. | The oracle lower bound cannot be imported for an explicit algebraic predicate. The coherent mechanism and singleton selection are prior art. |
| [Jordan et al., Optimization by Decoded Quantum Interferometry, v5](https://arxiv.org/html/2408.08292v5), Sections 8, 10, 14 | Decoding-based preparation of optimization-biased states; imperfect-decoding analysis; extension-field and balanced-oracle state preparation. | The new work must be a particular theorem about this explicit relation and its error terms, not discovery of the DQI framework. Tables of q local values would be exponential in this input length. |
| [Jo, Efficient Exact Quantum Sampling from the Sun–Wootters Distribution for Optimal Polynomial Intersection, v2](https://arxiv.org/html/2607.16541v2), Theorem 5.2 and Remark 5.3 | Complete lists, a single padded list length, reversible indexing, and uniform index projection implement exact coherent fiber sums with the explicit probability cost. | This directly anticipates the full-list operation audited here. Variable list normalization distorts the distribution. Its principal OPI guarantees concern prime fields; the operation itself is the relevant prior art. |
| [Horinaga–Yamakawa, Worst-Case Quantum Algorithm for Optimal Polynomial Intersection Beyond Decoded Quantum Interferometry](https://arxiv.org/pdf/2607.14650), Theorem 5.1 | A generic prime-power-field theorem gives polynomial quantum success from a list decoder, negligible ordinary and coherent tails, and a near-unit target normalization. | All three hypotheses are verified by this review for the native family. The separate OPI specialization assumes growing characteristic and does not apply directly to characteristic two. |
| [Chailloux–Tillich, Quantum advantage from soft decoders, v2](https://arxiv.org/html/2411.12553v2), Theorem 5 | A general decoding-to-dual-coset-sampling reduction with source preparation and decoding costs, and an average-over-syndromes faithfulness guarantee. | The theorem explicitly pays for averaging over the inhomogeneous syndrome. It does not by itself prove good readout in the fixed zero syndrome. The deterministic support-mask bound addresses that extra obligation here. |
| [Briaud et al., Quantum Advantage via Solving Multivariate Polynomials, v1](https://arxiv.org/html/2509.07276v1), Theorem 4.3, Lemmas 4.5–4.8 | The same code-constrained local-equation framework; separate ordinary and coherently coalesced failure bounds; a decoding lemma for nonzero error distributions with bounded point mass. | Their stated guarantee is over independent shift-invariant, pairwise-independent predicate distributions. Inverse trace fixed at every coordinate is not that distribution. The per-instance signed support-cell estimate and its specialization are the plausible incremental contribution, subject to broader literature review. |
| [Marwaha et al., On the Complexity of Decoded Quantum Interferometry, v2](https://arxiv.org/abs/2509.14443) | Coding identities and complexity analysis of DQI, including the limits of natural simulation strategies. | Classical source sample/query access is not the same as sampling the final native witness distribution. This paper supplies no hardness theorem for the present explicit relation. |
| [Gil-Fuster et al., Approximate sampling from decoded quantum interferometry via MCMC](https://arxiv.org/abs/2607.28120) | Empirical block-Gibbs comparisons for DQI optimization, including exponential-looking OPI runtime in the studied regime. | Those approximation scores do not certify all-constraint success on this native inverse-trace problem, and empirical growth is not an all-algorithm lower bound. |
| [Zhou et al., Gibbs Sampling in the Shattered Phase by DQI](https://arxiv.org/html/2609.40345v1), Appendix B | A latent active-constraint mixture gives a classical Prange sampler beyond barriers for some local/stable samplers. | This motivates the concrete native mixture derived in `CLASSICAL_SAMPLING.md`. Their random XORSAT theorem is not transplanted: the native derivation uses MDS projection and explicit root sampling instead. |
| [Mazumder–Niroula, Discovering New Problems for DQI](https://arxiv.org/html/2610.06753v1), Sections 4 and 7 | Screening comparisons with Prange and accepted affine subspaces, with explicit rank and distributional qualifications. | Its licensed-radius rules require worst-case unique recovery; they do not exclude this paid full-list protocol. Its random/translation-invariant accepted-set assumptions also cannot be substituted for the fixed inverse-trace predicates. The sections inspected supply no inverse-trace solver or hardness theorem. |
| [Shang–Stilck França, Homomorphic Polynomial Transduction via Relative Decoding](https://arxiv.org/html/2609.35101v1), Section 2 | An operator-algebra formulation distinguishes source relations, relative decoding, physical trace normalization and target sampling. Proposition 2.2 gives an exact degree-window isometry criterion. | That criterion does not automatically cover the native paid list projection beyond unique recovery. It reinforces the need to charge normalization and uncomputation, and does not establish classical hardness of inverse-trace search. |
| [Kothari, O'Donnell and Wu, No exponential quantum speedup for SIS-infinity anymore](https://arxiv.org/html/2510.07515v1), Theorems 1.5, 1.12–1.13 and Section 5 | Classical attacks on interval-constrained linear systems and some dense allowed-set variants; generalizations include coordinate-dependent sets. | These theorems have different alphabet, density, matrix-distribution and dimension requirements. Their general allowed-set bounds depend polynomially on q and use sets missing a constant number of symbols; here q is exponential and half the symbols are excluded. The interval theorem also needs substantially more columns relative to check dimension. It does not establish a native attack. |

The standard arithmetic inputs are [McEliece's GS/Roth–Ruckenstein
treatment](https://ipnpr.jpl.nasa.gov/progress_report/42-153/153F.pdf) and
[Carmon's characteristic-two Artin–Schreier statement, Theorem 3.1 and
equation 3.6](https://arxiv.org/html/1409.3694v1). For the latter, a rational
function with two simple poles has genus one. Applying the usual point-count
bound to 1/x+d*x, d!=0, gives the nonzero-domain Kloosterman bound 2 sqrt(q).
Totalizing zero adds exactly one to its Walsh sum. This verifies the
constant and convention used in the quantum audit.

## Assessment of significance

**Established:** a uniform ideal polynomial-time quantum solver for the
specified large-field relation follows from the independently reconstructed
proof and standard ingredients. Exact reversible arithmetic is available
in principle; an executed large quantum circuit is not required for this
complexity statement.

**Candidate incremental theorem, not a certified novelty claim:** the explicit
inverse-trace specialization with every-target guarantees and polynomial
cost in log(q). The generic quantum conclusion is already implied by
Horinaga–Yamakawa Theorem 5.1 once the native estimates are proved. The
full-list primitive is directly present in Jo Theorem 5.2. The independent
exact pattern-channel calculation is a useful simplification of the native
analysis, but uses the local discrepancy basis already present in DQI;
independent derivation does not establish novelty.

Here is the precise Theorem 5.1 substitution, using OUR notation to avoid
confusing their block length n with our field degree n. Take their code to
be C=D^perp, dimension N-K; W the normalized native product-root state;
and radius r=w/N. Their equation (19) is delta. Their equation (20) is
exactly ||A(1_tail*a)||², at most (1+eta)*delta by the relative norm bound
in EXACT_PATTERN_CHANNEL.md (the older delta+eta estimate also suffices).
Their equation (21) is |lambda_b-1|<=eta. Each is negligible for the audited
fixed rate K/N<1/4. State preparation and complete list decoding are supplied
explicitly in QUANTUM_AUDIT.md. Their output is inverse-polynomially close
enough in trace distance to a state supported entirely on native witnesses
to give inverse-polynomial verified success. Thus applying that generic
theorem needs no growing-characteristic premise.

**Still needed for significant advantage:** a serious classical complexity
case for the same explicit relation (or a meaningful standard-problem
reduction), an input distribution and finite resource comparison if making
a practical claim, and scrutiny beyond this single independent review.
No oracle lower bound, generic NP-hardness statement, local mixing barrier,
or finite solver failure establishes that case.

**Classical consequence of this review:** SUBFIELD_EXTENSION_ATTACK.md
gives polynomial witness algorithms on arbitrary supplied points when
n is even, n>=8, with at least 2K zero targets, or when 3 divides n,
n>=6, with at least 3K zero targets. The latter algorithm is deterministic.
These conditions hold with overwhelming probability for uniform target
bits along their respective degree families. Consequently a claim of
search advantage on the unrestricted native family needs to confront
these algorithms. Restricting to prime degrees or one-heavy targets is a
new proposed hard subfamily, not an original input promise. The attack
uses standard subfield arithmetic, Rado's independent-transversal theorem,
and constructive matroid union/intersection; no novelty is claimed for
those ingredients. This does not settle exact uniform native sampling.

Self-attack result: the earlier novelty falsifier was partly FOUND. The
two July 2026 papers already supply the full-list operation and a generic
worst-case theorem covering the reconstructed estimates. The explicit
predicate analysis remains the candidate increment. The next decisive
falsifier is an existing theorem or constructive classical algorithm for
this exact fixed inverse-trace relation; this targeted comparison is not
an exhaustive novelty certificate.
