# Fixed-prime affine AJT witness extraction: bounded independent audit

Date: 2026-10-27. Field: F_p with p = 100003. Dimension n is unbounded.

## Conclusion

**Existence is established; this audit did not identify a published polynomial-time witness extractor for arbitrary invertible M and arbitrary b at this fixed prime.** The inspected proof does not provide such a running-time guarantee. This is a bounded literature/proof audit, not a claim that no algorithm exists, a hardness result, or an exhaustive statement about the literature.

There is an elementary deterministic extractor for **n <= p-2 = 100001**, described and checked below. There are also easy structural subclasses. Neither settles the unbounded-dimension problem. The current AJT bridge should therefore remain an existence reduction, not be promoted to a general classical dequantization on this evidence.

## Exact scope and cost model

Input is an explicit matrix M in GL_n(F_p) and b in F_p^n. Output must satisfy

```text
x_i != 0 and (Mx)_i != b_i for every i.
```

Field operations have constant bit cost here; dense input length is Theta(n^2). A witness is checked in O(n^2) field operations. A bound C(p)n^{d(p)} would qualify as polynomial for fixed p, even with impractical constants. Conversely p^n, (p-1)^n, and c^n for fixed c>1 do not qualify. Precomputing finite subsets of this one field is not itself an asymptotic obstruction; dimension-dependent search is.

Read the supplied [AJT_BRIDGE.md](/Users/jaspersands/Developer/qsearch-research-work/systematic-full-support-2026-10-27/AJT_BRIDGE.md). Did not edit that note, the original repository, Git, UI, or migration state. Did not investigate the parent's high-distance affine-code sampling/repair route. Native code construction and its distance promise were taken as supplied, not independently re-proved.

## Main theorem and proof inspection

[Nagy-Pach, Theorem A](https://arxiv.org/html/2107.03956) applies to every invertible matrix over a prime field with 61<p!=79, allowing one arbitrary excluded value per input/output coordinate. Set input exclusions to zero and output exclusions to b.

The inspected proof has these relevant steps:

1. Proposition 1 translates nonexistence into a complex group-ring identity, then a mod-p identity.
2. Lemma 4 and Corollaries 2-3 choose dilations of small arithmetic sets so two Cartesian products do not intersect in the specified bases.
3. Lemma 10 chooses u in the product of the A_i with I_u={i:(M^{-T}u)_i is in B_i} inclusion-maximal. Under the assumed vanishing identity, it deletes a factor.
4. Theorem 1(i) descends to an invertible minor and contradicts induction; parts (ii)-(iii) establish avoidance.

No polynomial selector for u or witness-lifting procedure is supplied. The choice is globally inclusion-maximal, not merely locally maximal under single-coordinate moves. The argument is a contradiction proof, not a recursive solver on smaller witnesses. [Proof, Sections 4-6](https://arxiv.org/html/2107.03956#S6)

Publication status was checked separately: [JEMS DOI 10.4171/JEMS/1640](https://ems.press/journals/jems/articles/14298707), published online 11 April 2025. Proof numbering above follows the accessible arXiv text, not an asserted pagination match with the subscription version.

## What remains unimplemented

The following is this audit's algorithmic accounting, not a complexity lower bound.

**Extremal selection.** Given the auxiliary sets, a direct implementation would seek u in A_1 x ... x A_n satisfying as many prescribed B-memberships of M^{-T}u as possible in the inclusion order. An improvement search from a current u asks for another point preserving all current memberships and adding at least one. At most n successful improvements says nothing about the cost of finding one or certifying that none exists. Linear inversion is easy; satisfying the simultaneous finite-set constraints is the unimplemented operation. Enumerating the product costs prod_i |A_i| candidates. Even solving this subproblem would not, by itself, constitute a proved AJT extractor: one must also give the transformations back to the requested x and their costs.

**Auxiliary random choices.** Randomly choosing the dilation parameters is cheap. Certifying that the associated Cartesian products have no collision is a separate finite-set feasibility problem. A union-bound existence argument does not supply that certificate or an output x. This does not rule out a randomized constructive reformulation.

**Explicit algebra.** The group algebra has p^n basis elements. A dense implementation has exponential storage; expanding 2n binomial factors produces up to 4^n pre-collection terms. A compact product expression is not an efficient coefficient, identity-testing, or Fourier-support-search oracle. These are costs of literal representations, not lower bounds on all representations.

**A precise sufficient oracle.** Independently define

```text
Q(X) = product_i X_i * product_i ((MX)_i - b_i).
E(prefix) = whether Q is nonzero at some F_p-completion of that prefix.
```

An exact algorithm for E taking T(n) time yields witness extraction with at most n(p-1) calls by preserving E=true while fixing coordinates. The missing task is E on the restricted instances, not E at the unrestricted root, whose answer is already known. Equivalently one needs to test nonzeroness after reduction modulo X_j^p-X_j for every remaining variable, with polynomial total cost from the compact matrix input. No such implementation was obtained from the inspected sources.

Formal polynomial nonzeroness is insufficient: X^p-X is a nonzero formal polynomial vanishing at every field element. Expansion can also be exponential in an easy instance: for M=I and b=1, Q=product_i X_i(X_i-1) has 2^n distinct monomials although a witness is immediate. Thus representation blowup alone cannot establish hardness.

## Other primary sources checked

- **Nagy-Pach (2026), [On a group ring identity related to the Alon-Jaeger-Tarsi conjecture](https://arxiv.org/html/2604.26320).** Theorem 1 proves an implication from a group-ring conjecture to AJT for small primes, by a minimal-counterexample argument. It supplies no general extraction routine or polynomial runtime for p=100003. This is a preprint, not a new constructive theorem for the present prime.
- **Nagy-Pach-Tomon, [Additive bases, coset covers, and non-vanishing linear maps](https://arxiv.org/html/2111.13658), Theorem 5.1 and its proof.** The multi-matrix/list extension assumes a cover, selects an irredundant subcover, and contradicts a rank bound. There is no uncovered-point algorithm in that argument. Turning subcover deletion into computation would require testing coverage, not just computing normal-vector ranks. The [author publication list](https://cs.bme.hu/~ppp/publications/) says this work is contained in **Hyperplane covers of finite spaces and applications**, [Trans. AMS 379 (2026), 137-156](https://doi.org/10.1090/tran/9483). The current publication was verified, but its full PDF timed out here; the detailed proof inspection used the accessible predecessor. No claim of complete inspection of the journal version is made.
- **Important withdrawn source:** [Irredundant hyperplane covers, arXiv:2205.03389](https://arxiv.org/abs/2205.03389) was withdrawn on 31 October 2022. The authors identify a mistake in Claim 4.5, Section 4.2, invalidating most of the paper. Its archived v1 was inspected for provenance only. Do not rely here on its p^alpha-forbidden-values assertion or its p=79 appendix. The old author-hosted combined manuscript *Coset covers, restricted linear maps, and additive bases* includes that work; its cached abstract is not evidence that the withdrawn claims were repaired. This does not invalidate the separate Nagy-Pach theorem used above.
- **Alon-Tarsi (1989), [A nowhere-zero point in linear mappings](https://web.math.princeton.edu/~nalon/PDFS/Publications/A%20nowhere-zero%20point%20in%20linear%20mappings.pdf), Theorem 1.** Covers proper prime powers, not the prime 100003. **DeVos (2000), [Matrix Choosability](https://www.sfu.ca/~mdevos/papers/pliant.pdf), Section 1 and Corollary 1.3**, also does not supply the required extractor: the (p,1)-pliant consequence needs p allowed input values, while F_p minus zero has p-1. Existence over an extension field is not witness descent to F_p.
- **Fang-Feng-Shao (2011), [Generalizations and applications of the nowhere zero linear mappings in network coding](https://doi.org/10.1016/j.laa.2010.09.048).** The publisher abstract advertises a polynomial network-coding construction but explicitly assumes field size at least the matrix row count plus two. It does not establish the unbounded-n fixed-p result. Full paper not obtained; the algorithm below is independently derived, not attributed to an unread proof.
- **Schauz (2007), [Algebraically Solvable Problems](https://d-nb.info/985226862/34), Section 10, Algorithm 1, p. 68.** The Nonzero-Finder successively specializes a nonzero polynomial whose individual degrees fit the grid, retaining a nonzero specialized polynomial. The author explicitly warns that resulting algorithms for other existence statements can take exponential time. Applying this to a matrix product requires an efficient suitable representation and specialization/nonzeroness tests; polynomial time in an exponentially expanded polynomial is not polynomial time in M. The related [2008 journal article](https://www.combinatorics.org/Volume_15/PDF/v15i1r10.pdf) is a distinct, shorter text; do not silently transfer the dissertation's algorithm numbering to it.
- **Recent algorithmic near-match screened:** Pant-Chakrabartty-Singh, [A Permanental Analog of the Rank-Nullity Theorem for Symmetric Matrices, STACS 2026](https://drops.dagstuhl.de/storage/00lipics/lipics-vol364-stacs2026/LIPIcs.STACS.2026.70/LIPIcs.STACS.2026.70.pdf), abstract and Sections 2-3. Its tractable classes are nonnegative symmetric/positive-semidefinite matrices and balanced signed-graph adjacency matrices, over the real-number setting used there. This is not an AJT witness algorithm for arbitrary finite-field matrices.

## Actual algorithms with limited scope

### Greedy extraction when n <= p-2

For each nonzero row i let j(i) be its last nonzero column in a chosen column order. Assign x_1,...,x_n in that order. At stage j forbid zero, and, for every row with j(i)=j, forbid

```text
(b_i - sum_{t<j} M_it*x_t) / M_ij.
```

At most n+1 field values are forbidden, so a choice exists when p>=n+2. Each row is finalized once and cannot subsequently change. This proves correctness for arbitrary b; invertibility is only needed here to ensure nonzero rows.

Using a length-p Boolean table per variable gives O(n^2+np) operations at fixed p, including scanning rows/choices and checking the answer. There are n field inversions; their cost is constant at the fixed prime (or polynomial in log p if charged separately). Storage beyond the input is O(n+p). More generally the same algorithm succeeds whenever fewer than p-1 output rows have their last nonzero in each column; this is a checkable sufficient condition, not a promised property of arbitrary M.

At n=5e+3 this covers integer **8<=e<=19999** under the supplied distance-to-two-bases reduction. It says nothing about all larger e. These numerical cutoffs are mathematical scope, not a claim that an explicit 100001-square matrix is practical to store.

### Other elementary baselines

For already triangular invertible M, solve in the corresponding forward/backward order: each variable avoids at most zero and one affine root, giving O(n^2) time for p>=3. Arbitrary Gaussian row operations do not preserve the output exclusions, so triangularization is not a reduction to this case.

For uniformly random x in (F_p^*)^n, condition on all but one nonzero-coefficient input in each row. Its forbidden-output probability is at most 1/(p-1). A union bound therefore gives success at least 1-n/(p-1), useful when n<p-1, and at least 1/2 when n<=(p-1)/2. It gives no positive uniform bound for unbounded n. Exhaustive enumeration always works with O(n^2(p-1)^n) time and polynomial working space, but is exponential.

## Counterexamples to unjustified extraction shortcuts

These examples address algorithms for arbitrary AJT inputs. They are not asserted to come from the native complete AG code.

1. **Many solutions need not mean efficient rejection.** M=I and b=1 has (p-2)^n solutions. Uniform nonzero-input sampling succeeds with probability ((p-2)/(p-1))^n, exponentially small at fixed p, despite the immediate witness x=2. Even the homogeneous case can have exponential rejection time: for r diagonal blocks [[1,1],[1,-1]], success is (1-2/(p-1))^r because each block forbids x_1=+/-x_2. Neither example is a hardness result.
2. **Pinning coordinates destroys the totality promise.** Set n=p-1 and M=[[I_{p-2},1],[0,1]]. Index the first p-2 rows by t=1,...,p-2; set b_t=1+t and b_n=p-1. Fix x_t=1 for the first p-2 coordinates. Every nonzero last value s is forbidden: s=t violates row t for s<=p-2, and s=p-1 violates the last row. Yet the original instance has witness (2,1,...,1), with last coordinate 1. The matrix is invertible and all partially assigned coordinates are nonzero. Thus arbitrary prefixes need not extend, and a smaller invertible minor does not retain all residual constraints. This also shows why a bad column order can trap the forward greedy algorithm outside its guarantee, even on a triangular matrix.
3. **Invertibility is not nonzero permanent.** [[1,1],[1,-1]] has determinant -2!=0 and permanent zero in this odd characteristic. A permanent-lemma algorithm needing a specified nonzero coefficient cannot simply substitute the determinant test.

## Affine versus homogeneous extraction

There is no extra asymptotic obstacle caused by arbitrary b. This direct reduction is independently verified:

```text
N = [[M, -b], [0, 1]].
```

N is invertible. A homogeneous AJT witness (y,t) for N has t!=0; x=y/t satisfies the required affine exclusions because My-bt=t(Mx-b). Conversely an affine witness gives the homogeneous witness (x,1). Construction costs O(n^2), normalization O(n), and changes dimension by one. A genuine polynomial extractor for homogeneous AJT at this same prime would therefore suffice; the literature audit did not find one.

## Consequence for the native reduction

The supplied rowspace distance satisfies 12e-3>5e+3 for integers e>=1; hence certainly for the specified e>=8. With full row rank, deleting a k-column basis leaves rank k: otherwise a nonzero rowspace vector would be supported on at most k deleted coordinates. Select another basis from the remaining columns. With the bridge's notation,

```text
s' = s - B_R*1;  b = B_I^{-1}s';  M = B_I^{-1}B_J;
z_R = 1;  z_J = x;  z_I = b-Mx.
```

Basis selection and solving these systems cost O(k^2 m + k^3) by ordinary elimination, and direct native verification costs O(km). Here k=5e+3 and m=22e, so this overhead is O(e^3). A general extractor of cost T(k) would give O(e^3+T(5e+3)) native witness extraction. The existence theorem does not supply T. Conversely, no hardness conclusion for the special matrices follows from the extraction gap for arbitrary matrices.

## Verification and audit boundary

The companion [checks.py](/Users/jaspersands/Developer/qsearch-research-work/ajt-extraction-review-2026-10-27/checks.py) checks the restricted greedy algorithm, affine homogenization, and counterexamples using only Python's standard library. It is not a general extractor and does not construct or test the native AG family.

Executed successfully with exit code 0:

```text
python3 -B /Users/jaspersands/Developer/qsearch-research-work/ajt-extraction-review-2026-10-27/checks.py

12,000 exhaustive GL(2,5) / arbitrary-target greedy checks passed.
250 seeded invertible-matrix greedy checks passed, including p=100003.
1,600 affine/homogeneous witness-equivalence points passed.
Rejection counts at p=5,n=4: affine 81/256; homogeneous 64/256.
Prefix dead ends: p=3,5,7 exhaustive last-coordinate checks passed.
p=100003 prefix dead end and global witness checked implicitly and exactly.
```

The large-prime counterexample check does not allocate a dense 100002-square matrix. The tests corroborate the displayed elementary arguments; they do not certify a new algorithm for unrestricted inputs or a literature nonexistence claim.

Searches used the theorem's hyphenated/unhyphenated names with `algorithm`, `polynomial-time`, `constructive`, `algorithmic`, `search`, and `complexity`, plus title/author follow-up searches. Evidence above is from authors' papers, arXiv records, publisher pages, and the author's publication list. Unofficial AI proof/review websites and their snippets were not used as evidence. Search absence was not treated as proof of algorithmic nonexistence. Some full-text fetches failed as noted; the review is intentionally bounded, not an exhaustive citation-network survey.

**Recommended status:** keep "total search by affine AJT; polynomial extraction not established in this audit" for unbounded e. Record the explicit low-dimension greedy guarantee separately, and do not import the withdrawn stronger cover claims.
