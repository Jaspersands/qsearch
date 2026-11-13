# Stable top-degree Kronecker inputs: existing small-LR baseline

13 November2026. Candidate question: can the full polynomial quantum dimension
ratio promise support an unmatched family with growing Durfee, using stable
near-row labels? Native inputs alpha[n]=(n-a,alpha), beta[n]=(n-b,beta),
gamma[n]=(n-s,gamma), with a=|alpha|, b=|beta|, s=|gamma|=a+b,
n>=4s (empty cases separately), explicit numerical-n model. Output exact g.
Oriented ratio R=f^(alpha[n])*f^(beta[n])/f^(gamma[n])<=n^K for fixed K.
Known quantum mechanism measures multiplicity with probability g/R; cited
Larocca--Havlicek upper bound O(n^4 R^2) gates. This is an existing quantum
candidate family, not a new mechanism or claimed separation.

Corpus been-tried and baseline lookups preceded detailed source checks.
They exposed the known counting-versus-transform and same-hidden-source-law
warnings; this problem asks only one ordinary integer, not an HSP decoder.
No exact sampler record was found, which is not a novelty claim.

## Decisive existing classical attack

The actual Briand--Orellana--Rosas arXiv0907.4652v2 Theorem1.2 (LF238--248,
proofLF430--491) gives stability by a+b+alpha1+beta1<=2s. Actual
Ikenmeyer--Panova2024 journal source LF72--81 and190--196 identifies the
top-degree stable coefficient with c_(alpha,beta)^gamma. Thus g=c here.
The representation dimension identity gives g<=R on EVERY triple.

Actual Ikenmeyer arXiv1209.1521v1, section3 (LF373--450 onward), gives a
polynomial-delay neighbor generator on the connected integral hive-flow
graph; its breadth-first search visits all c points in O((c+1)^2 poly(ell))
arithmetic operations, including the zero case. It does not require a supplied
hive: it first finds one or certifies emptiness using the described positivity
algorithm. Source explicitly measures arithmetic operations. Native input
coordinates here are<=n. The completed audit below pays flow coordinates, feasibility arithmetic
and bit complexity; no free counting/hive oracle.
Panova2502.20253v2 Theorem4.8 (LF785--791) already highlights this baseline.
Therefore a new LR sampler is not justified merely to match this region.
Independent narrow source/bit audit CLOSED; no full-ratio theorem claimed.

The journal has an editorial erratum DOI10.1007/s10801-016-0690-x. Its primary
landing page confirms publication but full text was inaccessible; a mirrored
publisher preview reports line-number/symbol corrections. Do not treat that
mirror as independent primary verification. The actual2012 preprint used
here already has the corrected algorithm line references for section3.

## Optional sampler derivation, not selected for implementation

A secondary route was derived before the stronger baseline was located.
Sample uniform standard tableaux of shapes alpha,beta; assign a uniformly
chosen a-subset of labels1..s to the first tableau and the complement to the
second, preserving order. Multiply their plactic classes by row insertion.
Lothaire Algebraic Combinatorics on Words, actual rendered printedpp156--157,
Theorem5.4.5 says each fixed target tableau of shape gamma has exactly
c_(alpha,beta)^gamma such factorizations. Multilinear content forces disjoint
labels; each input pair is equally likely. Hence the output shape law is
 c_(alpha,beta)^gamma f^gamma/[binom(s,a) f^alpha f^beta].
This is an induction law; the inverse restriction/rectification normalization
is different. Both must not be confused with a hidden-subgroup source law.

Write D_theta=prod_(j<=theta1)(1+theta'_j/(n-|theta|-j+1)). The hook formula
gives f^(theta[n])=binom(n,|theta|) f^theta/D_theta. Then
 R_ind/R = [binom(s,a)binom(n,s)/(binom(n,a)binom(n,b))]
           *D_alpha*D_beta/D_gamma <= exp(2s/n)<=exp(1/2)<2,
because n>=4s, D_gamma>=1, logD_theta<=2|theta|/n, and the bracket<=1.
This supports a Monte Carlo alternative if desired, but existing small-LR
enumeration already removes the blocker. No sampler implementation, sweep,
paid confirmation, new asymptotic advantage or novelty claim is justified.

Sources retained under audits/sources/2026-11-13-lr-induction/ and prior
kronecker-ratio/. The Lothaire text extraction has corrupt font encoding;
actual renderedpp154,156,157 were read. Do not attach its corrupted text to
an API packet. The source theorem is imported, not inferred from a snippet.

Next: finish the narrow strongest-baseline audit; compare independent
high-upside quantum directions before another Kronecker variant. No full
polynomial-ratio, arbitrary stable deficit, growing-Durfee general exact
count, coherent transform, hardness or quantum advantage conclusion.


## Closed native BIT audit

Full112LF independent proof parent read:
`audits/reviews/2026-11-13-stable-lr-baseline-audit.md`. Actual BI12
arxiv1204.2484 section4.4 Algorithm1 starts at zero and uses integral shortest
residual path augmentations. At most s unit augmentations produce an integral
capacity-achieving seed or certify zero; no generic LP-to-integer inference.
The original source's sharper capacity-scaling bound is unnecessary here.

Ikenmeyer's actual NeighGen implementation (section5.2 Algorithm3, including
its shortest-path fallback and exhaustion bound) enumerates the connected
integral hive-flow graph. Each discovery changes O(ell^2) integer coordinates
by O(ell^2). A discovery tree has at most g vertices, so stored and candidate
values are O((s+g+1)ell^2); slacks and graph operations have polynomial bit
cost. Explicit duplicate detection/queue storage/output are paid. Thus exact
poly(n,g+1) BIT including g=0; g<=R<=n^K gives polynomial numerical-n time.
No compact-binary or arbitrary-deficit claim. No sampler implementation,
new finite sweep or paid confirmation was warranted.

The full162LF independent opportunity comparison was also parent read:
`audits/reviews/2026-11-13-post-binary-selection.md`. Its LR sampler proposal
is withdrawn. Class-two group common-frame alignment and operator-spreading
wrappers supplied no new complete mechanism; scoped rank/path falsifiers
are not broad no-go results. A scalar-relative-norm recheck found the already
closed solver, so it was not reopened. Native local Selmer halving still has
its earlier conditioning blocker; no repeat of that paid task was launched.
