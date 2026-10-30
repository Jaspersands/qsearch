# Coset Multiplicity Scope And Structured Pair Access

2026-10-30. The former **exhaustive trilemma is retracted**. Its original
negative record is preserved, hash-bound, in
`registry/quarantined_campaign_negatives.json`. The historical filename and
CLI locate the correction; they no longer denote a general no-go theorem.

This pass retains three narrow identities, corrects two invalid numerical
checks, and specifies efficient access to structured noncommuting operators.
It supplies neither a useful hard-coset receiver nor a new quantum speedup.
Independent automated reviewers checked the information model and the
access construction; this is not human peer review or formal verification.

## 1. Correct State And Invariance Statement

For H<=G use normalized coherent cosets and the mixed regular coset state:

    |gH> = |H|^(-1/2) sum_(h in H) |gh>,
    rho_H = (1/|G|) sum_g |gH><gH|
          = (1/|G|) sum_(h in H) R_h,
    R_a|g> = |g a^-1>.

These operators are positive and trace one. For conjugation C_x|g>=|xgx^-1>,
rho_(xHx^-1)=C_x rho_H C_x^dagger. The original note instead used an
incoherent mixture over a translate of a fixed H; its asserted covariance
did not hold. It is not the state used here.

If every FINAL POVM effect E_y commutes with C_x^(tensor k), then

    Tr(E_y rho_(xHx^-1)^(tensor k)) = Tr(E_y rho_H^(tensor k)).

Thus outcomes contain zero information about H WITHIN one conjugacy orbit,
for any prior on that orbit. They can distinguish different orbits. On a
Fourier carrier, use the corresponding specified diagonal representation.
Commuting with LEFT regular translations alone is not the required condition:
the informative effects (I+/-R_t)/2 already commute with all left translations.

### Effects Are Not Instruments

For an instrument J_y, invariant immediate effects J_y^*(I) imply only that
its immediate classical label is blind. A later carrier effect F_(z|y)
has total effect J_y^*(F_(z|y)), which need not be invariant.

Weak-irrep projectors P_lambda give a concrete native example. Their labels
are conjugacy-blind, but sum_lambda P_lambda rho_H P_lambda=rho_H. They do
not erase orientation. A subsequent public-transposition Hadamard test
remains informative. In the exact S_3 regular-state control, the weak-label
law is (1/3,0,2/3); the later test has about0.251629 bits, and retaining both
outputs gives about0.306099 bits. These tiny controls falsify an asserted
universal inference; they are not a new oracle problem or hard-GI algorithm.

## 2. Physical Replacement For The Old Information Check

The old producer used V(tau) tensor I as a "state". It has negative
eigenvalues and trace (n-1)(n-3), not one. It then assigned zero, or a range
of traces, to a mutual-information field. No Shannon information was measured.
The difference basis e_i-e_(n-1) is also nonorthonormal, with Gram matrix
I+11^T; its integer representation matrices are not computational unitaries.

The replacement uses an orthonormal Helmert basis and the actual conditional
standard-irrep column state for a hidden transposition:

    sigma_tau = (I+V(tau))/(2(n-2)),
    P_inv = |Omega><Omega|,    |Omega>=sum_j |jj>/sqrt(n-1).

The binary POVM {P_inv,I-P_inv} on sigma_tau tensor sigma_tau has

    Pr(inv | tau)=1/((n-1)(n-2)),
    Pr(standard irrep on one native copy)=2(n-1)(n-2)/n!.

The producer checks PSD, trace one, normalized Born probabilities, and
effect invariance, and calculates Shannon mutual information from those
probabilities. Floating-point residuals are finite controls; exact zero
information follows from the covariance proof. Conditional standard blocks
are NOT free native copies; their source probability is reported.

## 3. Noncommutation Survives, The Old Proof Does Not

For the standard S_n representation, K=sum_tau V(tau) tensor V(tau), with
tau ranging over transpositions. Define K_12=K tensor I, K_23=I tensor K.
In the difference basis the indicated entry satisfies

    [K_12,K_23]_(000,001)=n,      n>=3.

The earlier proof incorrectly set the reverse product to zero. The correct
entry computation is

    (K_12 K_23)_(000,001)=binom(n-1,2)+2,
    (K_23 K_12)_(000,001)=binom(n-2,2).

For a direct check put d=n-1. When m=0, the four entries
K_(00,0m), K_(m0,01), K_(00,m1), K_(m0,00) are respectively
(1+binom(n-1,2),1,1,1+binom(n-1,2)). When m=1 they are (1,1,2,-1);
when m>=2 they are (1,0,1,-1). Subtracting the two products and summing
gives 0+3+(n-3)=n. The entries follow by separating transpositions that
swap two of the first d labels from those swapping one with the last label.

This excludes a common eigenbasis, not sequential operations, Hamiltonian
simulation, or every circuit implementing a specified change of basis.
Both pair class sums themselves lie in the GLOBAL diagonal commutant.

## 4. Dimension Is Not A Circuit Lower Bound

Character orthogonality gives the valid algebra-dimension identity

    dim End_Sn(V^(tensor k))
      = sum_nu multiplicity(nu)^2
      = (1/n!) sum_g (fix(g)-1)^(2k)
      >= (n-1)^(2k)/n!.

At k>=n the lower bound is exponential in n log n. It is an ALGEBRA
dimension, not the dimension of every multiplicity block or the gate cost
of a structured operation. In particular it says nothing of that size
about just three fixed standard-carrier registers.

The corrected producer evaluates the exact sum using rencontres numbers:
the number of permutations with f fixed points is binom(n,f)*D_(n-f),
where D_0=1,D_1=0,D_m=(m-1)(D_(m-1)+D_(m-2)). It does not enumerate n!
permutations. The identity-term bound is stored as an exact rational.
At n=k=16 its base-two logarithm is about80.77036, not the earlier84.10362;
the old truncated Stirling expression was not a certified lower bound.

## 5. Constructive Access Without A Dense Racah Transform

Let lambda_1,...,lambda_k be partitions of n and let states ALREADY be
encoded in orthonormal standard Young tableaux, with row/column locations
of labels stored in O(n log n) qubits per tableau. No arbitrary state
preparation, representation conversion, QRAM or dense matrix oracle is free.
For two known register positions a,b set

    T=binom(n,2),
    A_ab=(1/T) sum_(p<q) rho_lambda_a((pq))_a tensor rho_lambda_b((pq))_b.

### Coherent Group Action

For s_i=(i,i+1), write d=c_T(i+1)-c_T(i), where c is column minus row.
The Young orthogonal action has diagonal 1/d and off-diagonal
sqrt(1-1/d^2). For d=+/-1 it is the corresponding scalar with no invalid
tableau component. Otherwise choose the tableau with d>0 as the canonical
representative of {T,s_iT}, assign it orientation zero, retain the orientation
bit, and apply the 2x2 reflection

    [[1/|d|,sqrt(1-1/d^2)], [sqrt(1-1/d^2),-1/|d|]],

and uncompute the canonicalization and distance. Coherent indexing can use
linear scans; an O(n)-entry angle table is polynomial, not a d_lambda table.
This is the established representation formula, not a new CG transform.
[Vershik--Okounkov, Eq.6.5](https://arxiv.org/pdf/math/0503040),
[Jordan, Sections8.1--8.2](https://arxiv.org/pdf/0811.0562).

An arbitrary (pq) is a word of at most2n-3 adjacent transpositions. Controlled
ascending/descending sweeps with comparisons against coherent p,q implement
it without measuring p,q. Rotation synthesis and reversible arithmetic give
polynomial gates in n and log(1/delta). A conservative bound for the entire
pair-action block encoding is O(n^2 log^4(n/delta)); this is an analytical
gate plan using standard synthesis, not a compiled fault-tolerant benchmark.
The fourth power accommodates [Solovay--Kitaev synthesis](https://arxiv.org/abs/quant-ph/0505030).

### Normalized PREPARE/SELECT

Prepare |u>=sum_(p<q)|p,q>/sqrt(T), and let SELECT apply the two controlled
irrep transpositions. Extend unused encodings unitarily. Then

    (<u| tensor I) SELECT (|u> tensor I)=A_ab.

Every summand is a Hermitian unitary. Therefore ||A_ab||<=1, and the block
encoding has normalization ONE for A_ab but T for the unnormalized K_ab.
Polynomial-size PREPARE can use a binary tree of integer subtree counts.
No postselection probability is assumed: applying the block by heralding
would have probability ||A_ab psi||^2, which can vanish.
[Gilyen et al., Lemma52](https://arxiv.org/pdf/1806.01838).

Hamiltonian simulation of exp(-it A_ab) uses a sufficient query budget
O(1+|t|+log(1/epsilon)) with qubitization; full-oracle errors must be
O(epsilon/Q) across Q queries. Separately request ideal simulation-block
error O(epsilon^2) to obtain clean-output state error O(epsilon); this does
not change the displayed query asymptotics. For K_ab replace |t| by T|t|. A polynomial-length
sum of pair operators has coefficient normalization sum_j |h_j|; charge it
and the extra PREPARE/SELECT work. No mutual commutation is required.
[Low--Chuang](https://arxiv.org/pdf/1610.06546).

The finite producer explicitly verifies PREPARE/SELECT in the natural
permutation encoding, restricted also to the standard subspace. Its
overlapping sums do not commute, yet its SELECT is a permutation unitary.
Dense matrices are used ONLY by the bounded verifier. This is structured
access, not a simultaneous eigenbasis, Racah transform, PGM, or decoder.

## 6. The Universal Copy Claim Is False

The [existing regular-coset counterexample](NONABELIAN_BARRIER_SCOPE_AUDIT.md)
already supplies a legal public-candidate Hadamard test for hidden
transpositions. With M=binom(n,2), testing each candidate on
r=ceil(log2((M-1)/delta)) fresh copies leaves the true candidate always,
and any false one with probability2^-r. Union bound gives error<=delta
with M*r=O(n^2 log(n/delta)) copies, product measurements and polynomial
decoding. This contradicts a UNIVERSAL factorial-copy assertion.

The matched classical algorithm uses only M+1 oracle queries. This is a
counterexample to an overbroad theorem, not a new speedup. It does not solve
the long-involution ensemble relevant to graph isomorphism. Known
[single-copy limitations](https://arxiv.org/abs/quant-ph/0501056) and the
[Omega(n log n) collective-copy requirement](https://arxiv.org/abs/quant-ph/0511148)
retain their ensemble hypotheses. The [general polynomial-query upper
bound](https://arxiv.org/abs/quant-ph/0401083) does not supply polynomial time.

## 7. Research Consequence And Replay

Structured joint operations are not ruled out by these dimensions or
commutators. A viable continuation must give a carrier-sensitive FINAL
effect, useful mass on the actual hard ensemble, a decoder, and charged
precision/source costs. Simulating another invariant alone cannot meet
that requirement. All speedup, general-receiver, and generic-Racah claims
remain false or unresolved.

Run `python qsearch.py coset-multiplicity-carrier-trilemma`. Its normal
registry action now invokes the existing hash-bound quarantine, never
reinserts the old negative. `--no-registry` writes evidence without registry
changes. Tests cover physical states and effects, informative sequential
readout, both commutator products, exact dimensions, structured block access,
bounded allocation and non-reinstatement. No synthetic oracle candidate is
created. The current handoff records the final validation scope.
