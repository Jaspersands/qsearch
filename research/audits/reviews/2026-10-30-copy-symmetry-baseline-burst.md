# Copy-Only MPS Symmetry: Stronger Baselines And Their Boundary

2026-10-30. Focused written deductions, primary-literature checks, and small
in-memory numerical controls. No implemented symmetry learner, hardness
claim, novelty certification, or oracle separation. Only this note was created.

## Result And Input Discipline

There are two complete polynomial competitors under explicit extra promises:

1. **Contiguous-window parent filter:** the existing local-parent/color
   argument extends to logarithmic interaction range for fixed local dimension
   and finite local group. Sitewise actions remove the expensive enumeration
   of arbitrary site subsets. It returns subgroup generators, not just tests.
2. **Paid reconstruction plus polynomial index:** copies of an unknown pure
   polynomial-bond MPS admit polynomial reconstruction using learned block
   operations. With a polynomial bound on the symmetry subgroup's index and
   efficient public group sampling, this gives polynomial generator recovery.
   A corresponding low-rank mixed-state version is stated below.

Neither conclusion says that every polynomial-bond complex MPS symmetry
problem is solved. The explicit obstruction below has bond three, an odd-prime
sitewise group, constant global symmetry gap, and indistinguishable proper
marginals. It refutes the unconditional marginal-tomography shortcut, not
copy-only learning or quantum computational advantage.

Read alongside [the finite-field TT filter](../../TENSOR_TRAIN_CLASSICAL_FILTER.md)
and [the low-rank application filter](../../LOW_RANK_SYMMETRY_APPLICATION_FILTER.md).
The former takes **exact classical finite-field cores**. It does not take
copies of an unknown complex state. The
[ring-to-field reduction](../../UNIFORM_RING_TO_FIELD_RANK_REDUCTION.md)
supersedes direct mixed-order receiver comparisons; none are made here.

Use fresh IID copies of rho=P/r, supplied correct rank r, and the target

    H = {g : U(g) rho U(g)^dagger = rho},
    U(g) = tensor_i u_i(g),
    TD(rho, U(g)rho U(g)^dagger) >= delta  for every g outside H.

Here TD=||.||_1/2; n sites, local dimension d>=2, and delta^-1 are charged.
For pure MPS r=1 and the bond bound chi is supplied, not the cores.
The target is a density/ray stabilizer, NOT a vector stabilizer: nontrivial
p-power scalar phases are possible over C. No source preparation inverse,
conjugate copies, support basis, or exact numerical cores are initial input.
These are quantum-measurement/classical-processing competitors, not purely
classical algorithms supplied only a state description.

## A. Contiguous-Window Generator-Recovery Theorem

**Additional promises.** The known group is a generator-described p-subgroup
G<=K^n, with explicit local labels and a known unitary representation of the
finite group K, |K|=kappa. Local multiplication, representations, and
observable measurements must be efficient at the charged dimensions. Suppose

    L = sum_(j=1)^t Q_j,
    0 <= Q_j <= I,  ker L = im P,  L >= lambda (I-P),

where every Q_j is supported inside an interval of length at most s, 1<=s<=n.
The parent itself need not be supplied. Its entire-kernel property and bounds
t>=1, s, lambda>0 are promises. Put

    D = d^s,
    M = (n-s+1) (kappa*d^2)^s.

There is a bounded-error generator-recovery algorithm polynomial in
M+n*kappa, t, D, lambda^-1, delta^-1, the public input, and inverse constant
failure probability. In particular, constant d,kappa and s=O(log n), with
t and both inverse gaps polynomial, suffice. Bond dimension is not otherwise
needed by this theorem.

**Proof and resources.** Let sigma=U(g)rho U(g)^dagger. Equal-rank projector
geometry gives

    TD(rho,sigma)^2 <= 1-Tr(P sigma)
      <= Tr(L sigma)/lambda
      <= sum_j TD(rho_(S_j),sigma_(S_j))/lambda.

Thus some s-site window changes by at least a=lambda*delta^2/t when g is
outside H; extending a smaller support to a window cannot reduce the
available distinguishing information. All n-s+1 windows suffice even when
the locations of the parent terms are unknown.

Choose a Hermitian Hilbert--Schmidt orthonormal single-site basis B_a with
operator norm <=1. On each window retain every indexed product

    O_(W,k,a) = tensor_(i in W) u(k_i) B_(a_i) u(k_i)^dagger,
    k_i in K,  a_i in {1,...,d^2}.

Duplicate operators retain separate labels. Conjugation by G permutes these
labels by exact group multiplication; windows never move. If every original
basis coefficient of a D-dimensional marginal difference is <=v, then
TD<=D^(3/2)*v/2. Consequently some table means differ by at least

    tau = lambda*delta^2/(t*D^2)

under every nonsymmetry. This conservative rational threshold suffices.

Use the noise-safe randomized offset coloring from the application filter:
h=tau/4, e=beta*h/(16M), theta=h*J/Q with uniform J in {0,...,Q-1}, and
Q a power of two >=16M/beta. Estimate all M means to error e. Except with
probability at most beta, each computed floor((mean-theta)/h) equals its
ideal color. Equal true means are therefore not split by measurement noise.
Every true symmetry preserves the colors; any nonsymmetry moves a pair of
means separated by >=tau>h and cannot preserve all colors.

Append n regular K-fibers of one reserved color. This makes the permutation
representation faithful without imposing a new constraint. The polynomial
p-group color-stabilizer algorithm returns exactly H on the good event;
recover original tuple coordinates from its action on these fibers. This
uses [Luks, 1982](https://ix.cs.uoregon.edu/~luks/iso.pdf), the color problem
and uniform p-group argument, not the finite-field matrix theorem. An abstract
map onto G requires paid kernel generators and lift maps, as in the existing
filter; these are not silently supplied by state tomography.

Separate bounded-outcome measurements give the conservative copy bound

    O(M^3 * t^2 * D^4 / (beta^2 * lambda^2 * delta^4)
      * log(M/beta)).

Charge gate synthesis, acquisition error, matrix precision, and permutation
group work separately; reserve a fixed portion of beta for implementation
errors. Constant-success runs can be amplified using canonical subgroup
equality and a majority of independent outputs. No local support projector
or tiny local eigenvalue needs to be estimated by this proof.

**Actual improvement and exclusions.** The old table enumerates arbitrary
subsets, with size sum_(ell<=s) binom(n,ell)(kappa*d^2)^ell. Here it is only
the contiguous windows. Thus logarithmic range need not incur n^Theta(log n).
Require the displayed M to be polynomial: growing kappa,d can invalidate
that conclusion. In particular a p-level site costs polynomial in numerical
p here, not automatically polynomial in log p. A supplied polynomial-size
adjoint-observable orbit table can replace this enumeration, but must actually
be constructed and retain its group-action kernel.

An injective MPS is covered only when its boundary-correct parent has the
required entire kernel, window size, and quantitative gap. The word
"injective" or chi=poly(n) alone supplies neither s=O(log n) nor a uniform
inverse-polynomial gap. A selected state inside a degenerate ground space
does not satisfy the promise, even if the gap above that space is one.

**Stable local inverse corollary.** The parent can instead be replaced by a
proved orbit-wise stability bound, with supplied polynomial C_rec:

    TD(rho,U(g)rho U(g)^dagger)
      <= C_rec * max_W TD(rho_W,(U(g)rho U(g)^dagger)_W).

Use tau=delta/(C_rec*D^2) in the same proof. A local reconstruction map with
this Lipschitz bound on the whole relevant orbit suffices; full generator
recovery is polynomial in the displayed table and C_rec, at arbitrary index.
Pointwise identifiability, an unquantified pseudoinverse, or a good empirical
fit is not this bound. This route avoids executing a reconstruction algorithm
once its quantitative stability theorem is proved.

## B. Reconstruction Is Paid, And Does Not Require A Parent Gap

[Landon-Cardinal--Liu--Poulin, 2010](https://arxiv.org/html/1002.4632v1)
give sequential, unitary-assisted tomography of arbitrary pure MPS, including
noninjective examples. The operations are learned from copies rather than
obtained from the source. The following explicit precision accounting and
mixed-state extension use the elementary prefix-rank argument.

**Reconstruction lemma.** Assume rank(rho_[1:j])<=R for every physical prefix,
including the full chain. Allow ordinary polynomial-size quantum circuits
on the copies. Then rho can be reconstructed to TD error epsilon, with
failure beta, in poly(n,d,R,epsilon^-1,log(beta^-1)) resources. For a pure
MPS take R=chi. If a rank-r state has an eigenbasis of MPS of bond <=chi,
take R=r*chi: ranks of the reduced positive summands add. Existence of such
an eigenbasis is a promise, not access to it. Small MPO bond alone does not
imply this prefix-rank condition.

Here is a proof that does not divide by Schmidt coefficients. If
k=1+ceil(log_d R)<=n, put m=d^(k-1), D_rec=d^k<=d^2*R. At a sweep step,
apply previously learned block unitaries to a fresh copy and condition on
earlier output sites being zero. The next k-site density still has rank
<=R: previous operations and projections lie entirely to the left of its
right boundary and cannot increase the purification's Schmidt rank there.

Estimate this density omega by a Hermitian omega_hat with
||omega-omega_hat||_1<=eta. Select a top-m eigenspace with projector E and
rotate it to |0> tensor C^m using a newly synthesized k-site unitary. Since
the true support fits in dimension m, the variational principle implies

    q = Tr((I-E)omega) <= 2*eta.

This estimates retained weight, not exact support or individual eigenvectors;
no lower bound on a nonzero Schmidt eigenvalue is required. Postselect the
new zero and continue. Later unitaries do not touch earlier output sites,
so all successful projections combine into one output projector after the
learned sweep U. With <=n steps and eta=epsilon^2/(8n),

    p_success >= 1-2*n*eta >= 1-epsilon^2/4,
    TD(U rho U^dagger, successful normalized branch) <= sqrt(1-p_success).

Tomograph the final m-dimensional tail to TD error epsilon/2, and decode
with U^dagger. For a promised pure source choose a pure tail estimate, using
O(epsilon^2) density-estimation precision; its cost is covered below.
This proves total TD error <=epsilon. If k>n, full tomography
already has dimension d^n<=d*R and is polynomial under the same charging.
Learned decoder inverses are paid operations, not a supplied source inverse.

A deliberately loose tomographic bound is O(D_rec^5*eta^-2) copies per
step, up to confidence logarithms: estimate D_rec^2 orthonormal coefficients
to error eta/D_rec^(3/2). Thus total copies are

    O_tilde(n^3 * D_rec^5 * epsilon^-4).

On the good history all acceptance probabilities are >=3/4 for epsilon<=1.
Fixed rejection-sampling caps and a first-failure union bound make the raw
copy count polynomial with failure beta. Replaying <=n learned block
unitaries per trial is charged; each is a D_rec-dimensional operation with
polynomial synthesis cost. Budget circuit errors over the entire capped run.
Approximate eigensolvers need only attain the retained-weight variational
optimum to the allocated additive precision, not resolve a tiny eigengap.
The decoded pure state has MPS bond <=m; the mixed version has an MPO
description of bond <=m^2 and a tail density of dimension m. All are learned
to finite precision. No exact algebraic cores or conjugate input copies
are inferred from finitely many samples.

**From reconstruction to symmetry.** For the flat-state target define

    gamma(g) = 1-r*Tr(rho U(g)rho U(g)^dagger).

It is zero on H and >=delta^2 off H. For a normalized positive reconstruction
rho_hat with TD(rho,rho_hat)<=epsilon, uniformly for ALL g,

    |gamma(g) - [1-r*Tr(rho_hat U(g)rho_hat U(g)^dagger)]|
      <= 4*r*epsilon.

MPS/MPO contractions compute the bracket in polynomial time in the learned
bonds and charged local matrix dimensions. Choose epsilon<=delta^2/(64r)
and contraction error <=delta^2/16; threshold at delta^2/2. On the single
good reconstruction event, this is a correct classical membership test for
H for every g, including adaptively chosen candidates. Testing equality of
rounded cores instead is invalid: rounding can break exact symmetries.

**A complete additional regime.** Suppose I>=[G:H] is a supplied polynomial
bound, log|G| is polynomial, and public group arithmetic and uniform sampling
are efficient (for example from the explicit permutation presentation above).
Test O(I*(log|G|+log(1/beta))) independent uniform elements of G and output
the accepted elements. They lie in H. Until they generate H, the probability
the next sample lies in H but outside the generated proper subgroup is at
least 1/(2I). Each such success at least doubles the subgroup order, so the
displayed fixed clock suffices with high probability. This gives polynomial
generator recovery even without the parent promise. Approximate sampling
needs a total-variation budget over the clock. No hidden oracle is planted.
This small-index consequence is not MPS-specific: paid swap-test overlap
estimation also supplies the required membership decisions directly from
copies. Reconstruction's additional output is a reusable classical model.

For arbitrary exponential index, reconstruction and efficient membership
alone DO NOT establish polynomial generator recovery. Nor does the exact
finite-field subspace algorithm apply to approximate complex cores. A
general arbitrary-index algorithm needs an additional justified group
recovery argument. This is an unproved step here, not a hardness assertion.
In particular, conjugating by the learned length-O(n) decoder generally
makes the public action nonlocal. One cannot combine its simple output state
with Section A while silently retaining a sitewise action and short windows.

## C. Concrete Constant-Gap Obstruction To Marginals

For every n>=2 let d=p=3, G=(C_3)^n, and
U(a)=tensor_i X^(a_i), X|x>=|x+1 mod 3>. Consider

    |psi_0> = (|0^n> + |1^n> + |2^n>)/sqrt(3),
    |psi_i> = (|0^n> + |1^n> + i*|2^n>)/sqrt(3).

Both are pure open-boundary MPS of bond exactly three. An explicit TT uses
a three-valued virtual label copied along the chain and the three displayed
amplitudes on the first boundary. These cores describe the counterexample;
they are not furnished to its learner.

Every nonempty proper marginal of either state is exactly

    (1/3) sum_(x=0)^2 |x^S><x^S|.

If a is not constant across sites, its translated support is disjoint from
the original support, giving overlap zero. If a=(b,...,b), then psi_0 is
fixed for all b, whereas <psi_i|U(a)|psi_i>=1/3 for b=1,2. Therefore

    H_0 = {(b,...,b): b in F_3},     H_i = {0},
    min_(g notin H_0) TD = 1,
    min_(g notin H_i) TD = sqrt(8/9).

Thus no procedure whose data consist only of proper-subset reduced states
can recover H on both inputs, even with exact marginals and unlimited samples.
This includes any interval-tomography theorem with s<n. The obstruction is
not a small global symmetry gap or a small nonzero marginal eigenvalue:
all nonzero eigenvalues of those marginals equal 1/3.

The nearest-neighbor parent

    L = sum_(j=1)^(n-1) [I - sum_(x=0)^2 |xx><xx|]_(j,j+1)

has gap one and kernel span{|0^n>,|1^n>,|2^n>}, of dimension three. Both
states lie in that kernel. It does not isolate either ray. More generally,
the equal proper marginals imply equal energies for every Hamiltonian whose
terms omit at least one site; neither state can be its unique ground state
if the other has the same energy. This is the missing entire-kernel premise.

There is NO copy-only lower bound here. Measuring X at every site and keeping
the full product of outcomes estimates <X^(tensor n)>: it is 1 versus 1/3.
A constant-accuracy test needs O(log(1/beta)) copies. These globally correlated
records are not the same data as a list of proper marginals. The group is
abelian and the example is not proposed as a surviving hard application.

## Literature, Controls, And Decision

[Cramer et al., 2010](https://arxiv.org/pdf/1101.4366), Methods A--B, separate
unitary-assisted reconstruction from local-measurement certification by a
parent Hamiltonian; their GHZ discussion already identifies the phase
ambiguity of local marginals. The specific odd-prime symmetry subgroups and
gaps in Section C are the deductions used here, not a new tomography primitive.

[Baumgratz et al., 2013](https://arxiv.org/html/1207.0358v2), Theorem 1 and
Appendices A--C, reconstruct under explicit local correlation-map rank
conditions. Their discussion warns about inverting small singular values.
For a noisy polynomial competitor, charge window dimension, inverse
conditioning, and total reconstruction error propagation; exact generic
invertibility is not a uniform finite-copy guarantee. A certified polynomial
stability bound plus polynomial inversion work would feed Section B's
membership/index result. If it supplies Section A's orbit-wise local
stability bound and the table remains polynomial, that stronger route also
handles arbitrary index. Neither property follows from exact invertibility.

**Experiments, not proofs:** an in-memory NumPy control enumerated every
3^n action for n=3,4,5 and every nonempty proper subset. Marginal Frobenius
differences were 0; stabilizer orders were 3 and 1; minimum nonsymmetry TDs
were 1 and 0.9428090415820634; parent kernel dimension/gap were 3/1.
A separate 100-trial D_rec=9,R=3 noisy spectral-selection check obeyed
q<=2*eta (largest observed ratio 0.001668264879190525). These checks do not
implement tomography, the color-stabilizer algorithm, or a scalable learner.
This review changed no code, JSON artifacts, dependencies, or other notes,
and performed no Git writes.

**Precise result:** logarithmic-window, polynomial-table, entire-parent-gap
instances have a same-copy-input generator baseline; arbitrary pure
polynomial-bond MPS have paid reconstruction and robust membership, upgraded
to generators at polynomial subgroup index.

**Falsifier:** the bond-3 qutrit pair has identical proper marginals but
different H at constant delta, despite a gap-one degenerate parent. Any
unconditional local-tomography or selected-ground-state claim fails on it.

**Next action:** for the next concrete copy-source family, record
(d,chi,r,s,t,lambda,delta,kappa,[G:H]) and allowed measurement circuits first.
Run the window-table and index tests before proposing a receiver advantage.
If both fail, the specific unresolved task is arbitrary-index subgroup
recovery from a paid approximate complex MPS, with a robust original-coordinate
generator algorithm; neither marginal ambiguity nor missing classical cores
is evidence of hardness.
