# Gram-defect sampler: source-scope audit

**Disposition.** None of the five retained sources supplies the SAME theorem:
arbitrary product-pure complex Gram G, arbitrary explicit isometry U, all
collision outputs, and a uniform finite-bit TV sampler costing
exp(O(N(1-lambda_min(G)))) poly(input,1/epsilon). This is a scoped source
finding, not a novelty claim. The central positive-subset/truncation mechanism
is already in Moylett et al.; it must not be presented as a new principle.

All line references below count newline-delimited physical lines in the local
`.txt` files under `research/audits/sources/2026-11-13-gram-defect/`.
The proposed algorithm is in `reviews/2026-11-13-post-recovery-selection.md`.
No experiments, external searches, or new general-k sampler theorem enter
this audit.

## 1. Moylett: the closest result, including worst U and collisions

`moylett.txt` Sec.3 explicitly starts with the equal-overlap model
G=(1-x)I+xJ, 0<=x<=1 (LF289–290,417–418). Its Eq.(26) is a positive mixture:
choose a subset I with weight x^|I|(1-x)^(N-|I|), make I fully identical,
and make all remaining photons distinguishable from one another and I.
LF467–528 proves the matrix-element identity and normalization. Sec.3.2
(LF530–545) draws |I|~Bin(N,x), then a uniform subset of that size; it uses
Clifford–Clifford for I at O(|I|2^|I|+poly(|I|,m)) arithmetic cost and
independent |U_ji|^2 draws for the other photons.

Its Sec.5 is genuinely worst-case, not merely the Haar calculation of Sec.4.
LF764–817 bounds input-state trace distance by Pr(Bin(N,x)>k), hence bounds
every interferometer/POVM. LF830–831 explicitly includes collision outputs.
An m-by-N isometry versus an m-by-m unitary is no substantive distinction:
complete the columns conceptually; the occupied-column formulas suffice.

The published ingredients already give the proposed joint *arithmetic*
scaling on this family. Indeed E[2^S]=(1+x)^N<=exp(Nx), so a cap
k=min(N,ceil(2Nx+log2(2/epsilon))) makes the discarded mass <=epsilon/2
and the active cost exp(O(Nx))*poly(N,m,1/epsilon). One can return a legal
fallback on the tail; no rare-event conditional sampler is required.
For N>=2, lambda_min(G)=1-x, exactly the proposed spectral parameter.
N=1 is trivial. This corollary is a deduction from their algorithm and tail,
not a separately stated finite-bit theorem. Their presentation does not give
the requested capped-random-bit/coordinate-height ledger.

**Exact remaining distinction:** G=dI+H generally has high-rank H with complex
cycle phases. Conditional shared photons have Gram H_SS/(1-d), not J.
Clifford–Clifford for identical photons cannot simply be called on this data.
Moylett's general-G probability formula (LF277–290) is a preliminary identity,
not a general-G sampler. Its nonuniform-loss extension (LF1143–1164) does not
remove the equal-overlap restriction. Its note added (LF1199–1205) also credits
Shchesnovich with an independent Binomial-mixture identification; that cited
paper was not independently inspected in this audit.

## 2. Renema: interference truncation is a different guarantee

`renema2017.txt` uses G_ij=x+(1-x)delta_ij (LF117–124), truncates permutations
by their nonfixed points, and gives cost N^(2k)2^k k (LF173–178,221–242).
The error calculation concerns random-interferometer statistics (LF179–215),
and the sampling proposal feeds the approximated probabilities to Metropolis
(LF217–229). The closing discussion permits unequal and complex overlaps
(LF266–272,291–292); it does not provide a worst-U full-TV theorem or a
finite mixing/rounding cap for this new arbitrary-Gram input.

`renema2018.txt` removes any possible ambiguity about these quantifiers.
The actual full derivation assumes uniform real overlap x and uniform loss
(LF642–652), and Haar-network/Gaussian-submatrix asymptotics (LF669–671).
Theorems 1 and 2 (LF982–1012) bound *average over a random network* trace
distance. LF1055–1068 converts this by Markov to a small fraction of failing
networks, not a guarantee for each supplied U. Their “full output” includes
the random surviving count; it does not undo the explicitly collision-free
restriction at LF415–416 and650–652.

The sampling discussion (LF518–539) uses MCMC, clipping truncated weights,
and an N^(2k) evaluation cost. It is not a proof of a bounded mixing-time,
finite-bit sampler for every U. This audit does not invalidate its intended
average-case result; it declines to import a stronger native interface.
Moreover polynomial-in-N for fixed k is not automatically jointly polynomial
in N and1/epsilon: k grows with requested accuracy, and N^(2k) is not
2^O(k) poly(N). No source label erases either distinction.

## 3. Heterogeneous-overlap paper: general formula, restricted sharper bound

`inhomogeneous2024.txt` is the retained March2025 v2. Eq.(9) and the derivation
through Eq.(A15) retain arbitrary pure-state Gram factors (LF236–285).
The paper explicitly notes the general maximum-overlap bound (LF295–316).
It does NOT claim that all heterogeneous matrices fit its sharper model.
LF317–335 restricts to the generalized orthogonal bad-bit model:
phi_i=sqrt(x_i)Psi_0+sqrt(1-x_i)Psi_i, with the Psi modes orthogonal;
off-diagonal overlaps factor through the single common component.
Allowing phases in this representation still does not allow arbitrary
gauge-invariant complex Gram cycles or a general shared residual H.

The bound (17) is an expected L1 error over Haar interferometers, as stated
at LF275–285 and proved using IID Gaussian entries (LF426–435).
The final summation is over noncollisional outputs (LF659–688).
The evaluation scheme retains the fixed-k permutation/subset cost and JSV
subroutine (LF173–198); the sampling proposal is Metropolis (LF129–143).
Appendix approximations at LF659–675 are not a uniform finite-N BIT theorem.
Footnote43 (LF763–772) expressly leaves interfering residual modes outside
the model. Thus its general probability identity must not be promoted to
the full claimed native sampler.

## 4. Current exact-chain paper explicitly excludes this input

`senellart2026.txt`, arXiv2611.11044v1, main LF254–270 and Sec.S9
LF1416–1426, treats the common-mode/private-mode x mixture and explicitly
excludes a general internal-state Gram matrix from its samplers.
For single photons the algorithm first draws the active subset and routes
the private photons independently. The general set-chain criterion itself
does not supply a cheap arbitrary-Gram weight evaluator: main LF234–238
explicitly distinguishes the criterion from computational cost. Accordingly
this current paper neither subsumes nor proves the proposed active-Gram DP.
Its exclusion is evidence about its own algorithms, not a literature-wide
claim that no such algorithm exists.

## 5. Scientific action and gates

The literal SAME-theorem stop condition is not met by these retained sources.
Nevertheless, the correct framing is a direct extension of an established
classical positive-mixture simulator, not a new noise mechanism. The useful
increment would be an explicit arbitrary-complex-G active-prefix contraction,
retaining collision factorials and cycle phases, with a proved singly
exponential active-size BIT clock and exact-zero/finite-coin handling.

Do not spend another pass rediscovering the Binomial mixture, the scalar
equal-overlap bound, or a Haar-only maximum-overlap result. A short focused
completion of the already concrete DP is justified as a classical benchmark;
these source findings do not justify a broad discovery/implementation batch.
Whether the proposed 4^s improvement is correct, or any stronger general-k
sampler is available, remains UNKNOWN in this source-only disposition.
No mixed/correlated-internal-state, general boson-sampling easiness, quantum
advantage, or priority claim is admitted.
