# Post-bosonic opportunity selection — 2026-11-13

Scope: compare three independent native problems; choose a concrete next mathematical
operation, not a new quantum implementation. No network, APIs, Git, sweeps or archives.
STATE/TRAPS and targeted corpus `been-tried`/`baselines` queries were consulted.
Catalog misses are not evidence of novelty or absence of classical algorithms.

**Decision.** Prioritize the fixed-Durfee classical Kronecker compiler already under
independent review. It directly tests a published remaining comparison regime and
has a complete proposed operation, unlike the two alternatives below. Do not yet
select a new quantum speedup candidate. Full polynomial dimension-ratio Kronecker
computation remains a worthwhile question; neither a new advantage nor its full
classical resolution follows from the restricted compiler. This review does not
redo the separately assigned hook-Schur proof.

## 1. Exact Kronecker multiplicities under a public dimension-ratio promise

Native input: explicit partitions lambda, mu, nu of numerical n (unary n charged),
fixed K, and failure probability eta. Reorder so f_lambda is largest; promise
R=f_mu*f_nu/f_lambda <= n^K. Output the exact integer g(lambda,mu,nu).
Dimensions and R are exactly computable by the hook formula. If R<1 then g=0.
There is no hidden permutation, unknown state, tableau oracle or internal
multiplicity-basis transform in this contract.

Actual primary source: Larocca–Havlicek 2407.17649v5, Theorem 1 and equation (10)
(LF148–202), Kronecker specialization (14) and clock (LF247–255), retained at
`audits/sources/2026-11-13-kronecker-ratio/larocca_havlicek.txt`.
Take G=S_n x S_n and H=diagonal S_n. Public-label maximally mixed irrep preparation,
controlled regular action and weak Fourier measurement give probability g/R.
Estimating it to <1/(2R) and rounding costs O(n^4 R^2) source gates at constant
success; repetition supplies log(1/eta). This is the source's gate-model theorem,
not a fresh independent finite-gate compiler audit. In particular, it is an exact
integer output from repeated native samples, not the previously rejected RSK
composition or a promised coherent Kronecker transform.

External value: a basic representation-theoretic counting problem, with no
artificial quantum data source and an existing complete polynomial quantum clock
on the promised class. A superpolynomial classical gap here would be substantive,
but current evidence does not establish one.

Actual primary classical comparator: Panova 2502.20253v2, Theorem 1.1 LF85–94
matches every min(f_lambda,f_mu,f_nu)<=n^constant regime. Conjecture 1.3 and
Question 2 LF122–145 explicitly distinguish the FULL ratio promise. Section 7.1
LF1019–1026 confirms the distinction. Section 7.5 LF1065–1071 leaves exact
fixed-Durfee computation open in that source. These are statements of this source,
not a claim about exhaustive present literature or priority.

**Concrete new operation.** For two fixed Durfee bounds d,e, specialize the
Kronecker coproduct to hook alphabets of sizes (d,d) and (e,e), compute the resulting
polynomial in 2d+2e variables, and extract its coefficients in the product hook-Schur
basis. There are polynomially many monomials/hook partitions at fixed d,e. The
parent's `KRONECKER_FIXED_DURFEE_CLASSICAL.md` proposes exact determinants and
linear algebra giving n^O(d+e) BIT time (a conservative unspecified polynomial
exponent is sufficient). It handles arbitrary third partition and would be a
complete classical algorithm on its stated input, not an intermediate primitive.
The hook specialization's injectivity and exact BIT bounds are being independently
audited against Moens–Van der Jeugt and the symmetric-function identities.
Their proof and status are deliberately not assumed here.

Cheapest decisive tests: noninjectivity/aliasing of the hook basis, a parity error
in the tensor alphabet, or an exponential coefficient/determinant intermediate
would defeat this proposed compiler. Finite controls alone do not settle any of
those. If it survives, it removes all triples with two fixed Durfee bounds; it
still says nothing uniform for growing d,e. The next ratio question must escape
this newly tested classical class and Panova's small-dimension class.

### Exact falsifier of a proposed ratio-to-tail shortcut

For k>=3, n=k^3, put mu=nu=(n-k,k) and lambda=(n-2k,k,k). Then

    g(lambda,mu,nu)=1,
    k+1 <= R <= 4e(k+1),
    min aft = k = n^(1/3),

where aft(rho)=n-max(rho_1,length(rho)); f_lambda is the largest dimension.
Thus positivity does NOT imply R>=exp(c*min aft)/(n+1)^C for fixed c>0,C.
This family is classically easy, not evidence for an advantage.

Proof of g=1: let M_a be the permutation representation on a-subsets. For a<=n/2,
M_a=sum_{j=0}^a [n-j,j], so [n-k,k]=M_k-M_(k-1). Orbits of ordered a,b-subsets
are indexed by intersection r; their permutation modules have contents
(n-a-b+r,a-r,b-r,r). Multiplicity of [lambda] is the corresponding Kostka number.
In M_k tensor M_k every r>0 content has a part larger than lambda_1, forcing zero
by dominance. The same holds for every orbit in either cross term or M_(k-1)^2.
The r=0 content in M_k^2 is lambda itself, with Kostka number one.

The hook formula gives

    f_mu = n! (n-2k+1) / ((n-k+1)! k!),
    f_lambda = n! (n-3k+1)(n-3k+2) /
               ((n-2k+2)! (k+1)! k!),
    R = (k+1) [n! (n-2k+2)! / (n-k+1)!^2]
              [(n-2k+1)^2 / ((n-3k+1)(n-3k+2))].

The factorial ratio is a product of k-1 factors
1+(k-1)/(n-2k+2+j), j=1,...,k-1, hence lies in [1,e] for n=k^3.
The final bracket lies in [1,4] for n>=6k. Also
f_mu >= (3/4) k^(2k) > 4e(k+1), so f_lambda=f_mu^2/R>f_mu.
All three dimensions are superpolynomial in n. Their fixed Durfee sizes explain
why this is compatible with a possible fixed-Durfee classical match.

## 2. Bare supersingular isogeny search through a native orientation compiler

Native input: p, two maximal supersingular elliptic curves over F_(p^2), and a
small allowed isogeny degree ell != p. Output an explicit polynomial-length chain
of ell-isogenies connecting them (only instances admitting that output promised).
Do not supply target endomorphisms, a secret torsion correspondence or a class-group
orientation. Cryptographic external value is high; the natural input size is log p.

Proposed operation to test: recover a global arithmetic orientation by measuring
Frobenius on native torsion, then use an abelian relation/period routine to find the
path. A complete poly(log p,log(1/eta)) clock would be Shor-level in aspiration,
but neither that orientation compiler nor a full algorithm has been constructed.
Even the hypothesized abelian decoder must be paid; a hidden-shift reduction alone
is not a polynomial algorithm.

**Cheapest falsifier already applies to this operation.** For a maximal curve,
Frobenius pi over F_(p^2) satisfies (pi+[p])^2=0. End^0(E) has no nonzero nilpotents,
so pi=[-p]. Every prime-to-p torsion module therefore has the same scalar
Frobenius. Abstract symplectic torsion/Frobenius data cannot select a curve's
orientation or a connecting isogeny. This refutes that particular data-only
orientation proposal, not isogeny algorithms using other curve information.

Matched classical attacks must include graph path search and quaternion/endomorphism
methods under precisely their supplied data. The corpus's target-endomorphism
transport attack uses stronger input and cannot be transferred to this contract.
The retained comparison source, `sources/2026-11-13-opportunity-selection/compendium.txt`
LF995–1053, carefully separates ordinary class-group hidden shifts from general
isogenies. Its cited Childs–Jao–Soukharev (2014) and Castryck–Decru/Robert SIDH
papers would require actual primary reading before quantitative claims. No specific
best exponent is admitted here. Do not spend another pass on this direction absent
a concrete curve-dependent operation that survives scalar Frobenius; the existing
class-group sieve is not such an operation.

## 3. Knot-invariant approximation through intrinsic normalization

Native input: an explicit braid word beta with m crossings and n strands; output
V_trace(beta)(exp(2pi*i/5)) to absolute error epsilon, or relative error under an
explicit nonzero promise. This is an intrinsic invariant target, not accuracy scaled
by a representation dimension supplied as part of the output convention.

Proposed operation: use certified Markov moves/gluing to replace presentation-size
normalization by an intrinsic, polynomially bounded normalization, then apply the
native path-model quantum estimator. If both stages ran in poly(n,m,1/epsilon),
this would change what accuracy is algorithmically attainable. Neither stage is
newly established here. The existing additive normalized-trace algorithm alone
does not meet this changed accuracy contract.

Exact immediate test: beta_n=sigma_1...sigma_(n-1) has trace closure the unknot,
so V=1, while its normalized Markov trace has magnitude d^(1-n), d=2cos(pi/5)>1
(up to the known unit-modulus writhe phase). Therefore raw normalized-trace
estimation to constant intrinsic error incurs exponential precision/repetitions.
These examples are easy to destabilize classically; they refute presentation-only
normalization, not a general quantum lower bound. Conversely, a repair restricted
to O(log(n+m)) fusion width already permits polynomial classical contraction at
fixed level. A useful new compiler must escape both tests on an explicit family.

The retained comparison source's LF3033–3093 states the normalization and Morse/
fusion-space classical baseline. Actual source gates would be Aharonov–Jones–Landau
(2009), Kuperberg (2015), and the end-to-end Laakkonen et al. (2026) paper. They are
not newly read in this review, so their stronger precision/hardness conclusions
are not imported. Existing corpus braid-HSP “no-go” labels are not used.

## Bounded next action and gates

Finish the already launched fixed-Durfee coefficient-extraction proof and its
primary-source audit. This is the sole selected operation: a full classical
competitor with a falsifiable algebraic interface, not a generic QPE application.
Acceptance requires exact ordinary Kronecker coefficients, native unary input,
no aliasing and a polynomial BIT bound with d,e fixed. A successful proof narrows
but does not close the full ratio promise; a defect must identify the exact failed
identity or access/bit-cost step. No new quantum implementation, novelty, hardness,
full-ratio classical match or Shor-level advantage is claimed. No alternative
candidate is promoted merely because its classical baseline remains unproved.
