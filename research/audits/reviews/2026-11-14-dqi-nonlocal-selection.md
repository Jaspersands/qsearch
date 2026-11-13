# Native nonlocal DQI versus scalar random-table OPI

2026-11-14. STATE/TRAPS and the parent's corpus-before-baselines files
/tmp/qsearch_dqi_selection_{prior,baselines}.txt were read first. The fuzzy
formal-power-completion match does not apply to IID half-set tables. Actual
primary: audits/sources/nov14_decoder_selection/local_decoder.txt,
arXiv2611.12718v1. Read its decoding/output definitions, Conj6.7, §§7.1--7.5
and scope discussion; relevant existing BPQM and scalar-OPI notes were checked.
No network/API/Git, numerical scan, code or implementation was performed.

**Selection:** no new end-to-end algorithm is admitted. Sparse nonlocal DQI
is the higher-upside question, but a concrete preparation operation tested
below reduces to a classical heat-bath sampler whenever its proposed gap
proof succeeds. The remaining nonlocal decoder question is NOT refuted. Scalar OPI retains a paid quantum endpoint and an unmatched full-input
classical question, but this pass supplies no new table-exploiting operation.
A fresh decoder/preparation construction is needed before another paid
confirmation or implementation task; a threshold plot is not that operation.

## 1. The sparse native target and what the new source actually proves

Input: an explicit binary m-by-n configuration-model matrix B, k ones per
row and D per column, mk=nD, fixed3<=k<D; one may condition on no parallel
edges. The offset x0 is an independent uniform m-bit word. Native size is
O(mk log n), not an unknown state oracle. For fixed beta, output a classical
assignment z approximately distributed as

                 mu_beta(z) proportional to exp(-beta |Bz+x0|).

Total-variation accuracy is the task; an average energy or a good optimizer
alone does not solve it. A potential advantage hypothesis is polynomial
quantum sampling at a CERTIFIED temperature strictly between reconstruction
beta_d and condensation beta_c, where a matched classical sampler is unknown.
No numerical threshold in Table6 is silently promoted to such a certificate.
This source uses overlap tanh(beta/2); the old BPQM note's Ising coupling is
beta/2. Temperature conventions must be converted before comparing curves.

The native quantum reduction pays linear algebra for C=ker(B^T), uniform
codeword preparation, and product channel states
 |psi_c>=Z^c tensor_j(sqrt(p0)|0>+sqrt(p1)|1>), p1=1/(1+exp(beta)).
The unpaid operation is a decoder with small BLOCK error and a coherent
implementation plus its ACTUAL adjoint, retaining all internal records.
No unknown inverse or independent copies of overlapping tree wires are free.
Actual Theorem3.3 (LF1119--1160) gives offset-averaged TV <=sqrt(decoder error).
Its restart check has the same success for every offset. A fixed clock must
cap retries and budget synthesis for the complete capped circuit. A generic
decoder's average-offset conclusion is not an all-offset guarantee.
Exact coherent PGM has a stronger heralded all-offset guarantee, Prop7.3.
A binary violation sample is lifted to an assignment by a public linear
solve and a uniform kernel sample, so that readout is not an extra oracle.

Theorem7.7 (LF4136--4153) proves PGM success1-o(1) below beta_c and exponential
failure above beta_c for the CONFIGURATION model, also conditioned simple.
It does not prove the same theorem for Gallager's ensemble. Cor7.9 proves
beta_d<=beta_c; a specific strict window still needs certified parameters.
The stated o(1) alone is not a finite error bound for arbitrary supplied
accuracy. Table6's classical optimization values are Gallager benchmarks,
not a theorem matching configuration-model Gibbs laws.

Conj6.7 (LF2523--2575) remains explicitly CONDITIONAL: classical efficient
sampling throughout non-reconstruction is not proved for k>=3. Worst-start
spectral-gap failure would not refute its permitted warm-start/some-sampler
claim. Conj7.11 for small-block measurements is likewise not a theorem.
The source's local obstruction has its actual LT/TP/local-estimate and
reliable-block-decoding hypotheses; it does not exclude arbitrary deep cycle-dependent decoders or every constant-success postselected decoder.
Thus the title does not close native sparse DQI in general.

## 2. One concrete operation screened: filtered code-check projectors

Try to deform the beta=0 commuting-check code subspace into all weighted
coset states, then use its frustration-free gap for preparation. This has
an explicit native circuit/term description, so it can be tested algebraically.
Let K=im B, let v_i be column i of B, and work on any coset X=x0+K. Set
w(x)=exp(-beta |x|). On each pair {x,y=x+v_i}, define the rank-one projector

 h_i|_{x,y} = 1/(w(x)+w(y))
             [[w(y), -sqrt(w(x)w(y))],[-sqrt(w(x)w(y)), w(x)]].

It kills (sqrt(w(x)),sqrt(w(y))). Since the columns generate K,
H=sum_i h_i has exactly the weighted Gibbs vector as its ground state on X.
At beta0, h_i=(I-X^{v_i})/2. For fixed D each term depends on only D bits;
its entries use the local energy difference and have polynomial finite-bit
access. This is a legitimate candidate preparation Hamiltonian, not a
supplied ground state, Gibbs oracle or exponentially precomputed decoder.

But define the explicitly samplable generator
 (Lf)(x)=sum_i [w(x+v_i)/(w(x)+w(x+v_i))]*(f(x+v_i)-f(x)).
For S=diag(sqrt(pi(x))), pi=w/sum_X w, DIRECT substitution gives

                         H=S(-L)S^{-1}.

Thus the proposed quantum gap is EXACTLY the continuous-time heat-bath gap.
The discrete update choosing i uniformly has gap gap(H)/n and is positive
semidefinite, since 0<=H<=nI. Moreover
 log(1/min_X pi)<=rank(B)log2+beta*m=O(m) at fixed beta.
Consequently a proved inverse-polynomial gap gives a classical sampler from
ANY starting assignment in poly(m,log(1/epsilon)) steps. Every step computes
one native energy difference and one finite-precision coin. Polynomially small per-step error, charged over the fixed mixing cap, pays total variation.
If B has a kernel, sampling violations then uniformly lifting pays that too.

The same argument holds for ANY polynomial list of public binary moves
v_i spanning K, including nonlocal moves obtained by Gaussian elimination;
energy differences then cost O(m) each. Making this particular parent
nonlocal does not remove its classical counterpart. This is a scoped
algorithmic identity, not a general theorem about quantum decoders, and it
neither proves nor disproves a gap for the random model. It is the cheapest
decisive falsifier of this specific proposed preparation route as an
unmatched mechanism; no spectrum sweep is warranted.

A direct PGM shortcut is no better established: source Lemma7.2 diagonalizes
its Gram matrix with eigenvalues |C| times coset masses, but Prop7.4/Cor7.5
(LF3960--4013) identify the needed basis change with coherent normalized
Gibbs preparation on all cosets. Near-uniform coset MASSES do not implement
that basis change or provide conditional amplitudes. This is more precise
than saying only that an efficient PGM circuit has not been found.

## 3. Strong baselines and comparison with scalar OPI

Sparse baselines include native Glauber at the proved small-beta uniqueness
range, the existing exact-stationary affine-cluster chain (mixing unproved),
Prange matching product USD/rank completion, and Turbo Prange matching the
specific FGUM/block-amplitude OPTIMIZATION curve (§7.1). Neither Turbo Prange
nor simulated-annealing scores automatically provide the full Gibbs sampler.
Planted sparse-LPN recovery in §7.4 needs an additional posterior-correlation
claim; its first-moment inequality is not that proof and changes the offset law.

Scalar comparison: q=2^t,m=q-1,k_RS=floor(Rm), IID uniform q/2-element tables
S_i supplied in FULL, output P of degree<k_RS with many P(a_i) in S_i.
SCALAR_OPI_RANDOM_TABLE_LIST_SAMPLER pays known complete-list DQI, global
index erasure and full input loading in poly(mq), with limiting score
 1/2+sqrt(a(1-a)), a=min(1/2,1-sqrt(1-R)).
At R>3/4 its separate shell argument finds perfect witnesses with polynomial
repetition. These are known mechanisms, not a new result of this selection.
The present sparse fixed-alphabet/locality theorem does not cover this
growing-alphabet dense RS/full-table source. Conversely, scalar all-pattern
count concentration supplies no coefficient-prefix conditional-count oracle.

The strongest allowed classical attacks use ALL tables: published systematic
line search/annealing, retained soft decoding, list recovery and adaptive
algebraic methods. The rejected affine-flat full-row-rank certificate is
only one attack; its failure proves no hardness. No new source-correct
conditional-count or adaptive-table algorithm was derived here.

**Next admission criterion:** an explicit nonlocal coherent decoder operation
that avoids both the normalized-Gibbs basis-change circularity and the exact
heat-bath correspondence above, with finite block-error/preparation clocks
on the original random ensemble. Until such an operation is specified,
neither direction justifies a new quantum subsystem. All presently needed
source statements were available locally; no additional fetch is requested.
