# High Temperature Does Not Give Output-Bit Dobrushin Contraction

2026-10-25. Local written deduction with exact arithmetic controls. Not
independently reviewed, formally verified, or a novelty claim. This rules
out one proposed proof strategy, NOT classical sampling or quantum
preparation. No new candidate or toy search problem is introduced.

## Decision

The native HDQI output law can have a conditional influence exactly one
at EVERY positive temperature, including arbitrarily small beta^2(d+1).
Its worst-boundary influence matrix has spectral radius strictly greater
than one. Thus neither unweighted nor weighted Dobrushin contraction of
the OUTPUT-BIT heat bath follows from the published small-occupation
bound or the preceding FLUX heat-bath theorem.

These are different chains on different variables. The existing flux
theorem is unchanged. The counterexample itself is classically easy,
including an extensive product family. No sampling hardness follows.

More generally, EVERY native graph containing an induced three-vertex path
with nonzero couplings has the same obstruction for all positive beta
outside a locally finite exceptional set. This includes connected,
extensive-cycle-rank supplied-root inputs, not just disconnected fixtures.

## Same Native Model

Use the canonical independent generators for the three-vertex path:

    A = X_1, B = Z_1 X_2, C = Z_2 X_3, H = A+B+C,
    psi = exp(-t H)|000>/sqrt(Z), t=beta/2,
    Z = <000|exp(-2tH)|000>.

All couplings are one, d=2, and this is also a LINE GRAPH: its supplied
root is a four-vertex path. It lies inside the earlier fermion baseline
and inside the flux-preparation input class. Its purpose is to test an
assertion about those exact input classes, not to supply a hard instance.

Set D=AC. It is a central involution in the generated algebra, and

    H^2 = 3I+2D, P_+=(I+D)/2, P_-=(I-D)/2,
    H^2 P_+=5P_+, H^2 P_-=P_-.

Writing c_a=cosh(sqrt(a)t), s_a=sinh(sqrt(a)t)/sqrt(a) gives

    exp(-tH) = P_+(c_5-s_5 H)+P_-(c_1-s_1 H).

Ordered words A^y1 B^y2 C^y3 send |000> to |y>. Since DH=A+C-ABC,
the ONLY nonzero amplitudes before normalization are

    w_000 = (c_5+c_1)/2,
    w_100 = w_001 = -s_5,
    w_010 = -(s_5+s_1)/2,
    w_101 = (c_5-c_1)/2,
    w_111 = (s_5-s_1)/2.

In particular w_110=w_011=0 EXACTLY, at all beta. Every listed magnitude
is strictly positive for t>0: use the power series, whose differences
have coefficients 5^k-1. The normalization is

    Z = [cosh(2 sqrt(5)t)+cosh(2t)]/2.

The executable checks the algebra with exact physical matrices, compares
the entire Taylor coefficient vector through order sixteen, and encloses
the positive quantities with rational Taylor tails. It does not decide
that an amplitude is zero by a floating-point tolerance.

## Perfect Conditional Dependence

Let mu(y)=w_y^2/Z. Both conditioning events below have positive probability:

    Pr(Y_1=1 | Y_2=1,Y_3=0)=0,
    Pr(Y_1=1 | Y_2=1,Y_3=1)=1.

The first boundary permits only 010; the second permits only 111. Hence
the influence C_13 is exactly one, and by reflection C_31=1. Impossible
conditioning events are not used.

Put c=w_101>0, e=w_111>0, a=s_5>0 and define

    r = c^2/(a^2+c^2), u = 1-r > 0,
    v = e^2/(c^2+e^2) > 0.

Comparing the boundaries (Y_2,Y_3)=(0,1),(1,1) gives C_12>=u.
Comparing (Y_1,Y_3)=(0,1),(1,1) gives C_21>=v. Reflection gives
the other two inequalities. Consequently the nonnegative influence
matrix dominates

    M = [[0,u,1], [v,0,v], [1,u,0]].

On vectors (x,y,x), M acts as [[1,u],[2v,0]]. Its positive eigenvalue is

    lambda = (1+sqrt(1+8uv))/2 > 1.

Monotonicity of the Perron root gives rho(C)>=lambda>1. There cannot be
positive coordinate weights making the uniform influence bound contract:
if Cw<=a w with a<1, Collatz--Wielandt would give rho(C)<=a. In fact the
endpoint row sum is at least 1+u>1. This is a failure of that sufficient
criterion, NOT a lower bound on the chain's actual mixing time.

At t->0, c=t^2+O(t^4), e=t^3/3+O(t^5), a=t+O(t^3). Thus u->1 and
v~t^2/9. The forbidden contraction persists however small the nonzero
temperature. For any proposed kappa_0>0, choose beta>0 with
3 beta^2<kappa_0. It also persists under independent tensor products of
this component, yielding arbitrarily large native instances at d=2.

## Extension To Connected Native Inputs

For any real canonical Hamiltonian, S=exp(-tH) is a real symmetric matrix.
An ordered word P(y) is real and obeys

    P(y)^T = (-1)^(number of induced anticommutation edges in y) P(y).

Consequently its coefficient tau(P(y)^T S) is EXACTLY ZERO when that
edge count is odd: the trace of a real skew matrix times a symmetric
matrix vanishes. Orthonormality of the independent words and
P(y)|0>=|y> identify this coefficient with the actual output amplitude.
This uses neither a truncation nor a high-temperature approximation.

Choose any induced path with endpoints i,k and center j, all three
couplings nonzero. Pin every other output bit to zero. The two adjacent
pair words ij and jk have zero amplitudes for every t. The center singleton,
endpoint singletons, nonadjacent pair ik, and triple ijk have respective
leading coefficients

    -J_j t, -J_i t, -J_k t, +/-J_i J_k t^2,
    +/-J_i J_j J_k t^3/3.

The signs depend on the fixed word order and are irrelevant here. For the
triple, summing its six permutations gives magnitude 2 in H^3. An outside
generator cannot enter these lowest-degree terms because it would need
to occur at least twice to leave its output bit zero. Thus none of these
five real-analytic amplitude functions is identically zero. Their zeros
are isolated; their finite union is locally finite on t>0. Away from this
exceptional set, every conditioning event used above remains legal.

We again obtain C_ik=C_ki=1. If c is the nonadjacent-pair magnitude and
e is the triple magnitude, let v=e^2/(c^2+e^2)>0 and take u to be the
smaller of the two positive endpoint bounds a^2/(a^2+c^2). The 3 by 3
principal submatrix of the FULL influence matrix dominates the same M.
Thus its Perron root, and that of the full matrix, exceed one. There is
no symmetry assumption on the rest of the graph or its couplings.

For example the root K_v, v>=4, has m=v(v-1)/2 edges and extensive cycle
rank m-v+1. Its line graph contains the induced path of root edges
(0,1),(1,2),(2,3). In ANY open positive-temperature interval satisfying
beta^2(d+1)<kappa_0, all but a locally finite set of temperatures exhibit
this failure. No inverse-temperature scale is silently restricted to
beta=O(1/m^4). Conversely, this argument does NOT certify any particular
temperature in a large input without checking for exceptional zeros.

The extensive conditioning event can be extremely rare. That is enough
to defeat a WORST-BOUNDARY criterion, not an average-case coupling or a
sampling algorithm. No hardness claim is justified by this extension.
Nor is this a robust lower bound for approximate samplers: smoothing
events below an allocated total-variation budget can destroy the exact
conditional obstruction. Such smoothing must be analyzed, not assumed
to preserve every conditional probability.
The executable also checks the lowest coefficients and forbidden pair
zeros in the actual six-generator L(K_4) extension, not only the isolated
path. These checks remain finite controls, not the all-size proof above.

## Why Sparse Occupation Does Not Repair This

[Hastings--Schmidhuber, Appendix A](https://arxiv.org/html/2610.03697v1)
provides the unconditional inclusion estimate used in the predecessor
decoder note: Pr(S subset supp Y)<=product_(i in S)(beta J_i/2)^2.
It is not a conditional stochastic-domination theorem. Here, conditioning
on the positive-probability event Y_2=Y_3=1 forces Y_1=1, violating any
conditional occupation bound below one. No conditioning-invariant version
may be substituted into a Dobrushin or disagreement-percolation proof.

For the three certified temperatures, the executable checks every nonempty
inclusion event against t^(2|S|), with rigorous rational intervals. These
finite checks are only controls; the cited general inclusion theorem is
not proved by these examples.

## Opposite Control: The Same Family Is Easy

There are only six atoms, with the closed weights above. They can be
sampled by computing the six probabilities to allocated accuracy. For b
disjoint components, the Hamiltonian terms on different components commute,
the state factors, and b independent six-atom draws sample the full word
distribution. Polynomial-bit approximations with error epsilon/b per draw
give total variation error at most epsilon. This is polynomial in b and
log(1/epsilon) for bounded rational beta. No exponential statevector or
quantum oracle is necessary.

Even the single-site heat bath is not shown to be slow. As t decreases
to zero, its six-state transition matrix has limiting eigenvalues
1, 2/3, 2/3, 2/3, 2/3, 1/3. Its gap tends to 1/3 despite the failed
Dobrushin test. The limiting matrix is an exact control; no uniform
finite-temperature gap constant is inferred from a numerical fit.

## Prior-Art Gate And Next Constructive Question

[Bravyi--Gosset--Liu](https://arxiv.org/abs/2112.08499) gives sampling
reductions using amplitudes instead of marginal probabilities. It does
not grant an efficient amplitude oracle. For the extensive-flux native
pilot, the current Gaussian formula still sums interfering flux sectors;
the old exact sampler pays exponentially in cycle rank. Nor does the
explicit flux parent give a local, classically accessible parent in the
final output-bit basis after controlled Gaussian preparation and Fourier
readout. This pass does not claim to audit all hypotheses of that paper.

The live task remains a classical sampler for the SAME connected,
extensive-cycle-rank output law, or a useful-task reduction that survives
the existing estimators. Viable approaches must cope with exact zeros
and correlations created by positive pins: block updates, an average-case
rather than worst-boundary coupling, a different positive representation,
or a priced amplitude-based sampler. None is supplied by this note.

Do not implement a general output Glauber campaign on the assumption that
the flux proof transfers. Do not run more three-site benchmarks. A future
sampler can pass this control while using an entirely different mixing
argument. This pass also rejected two rediscoveries before editing:
the polynomial derivative filter and zero-moment Rees state conversion
already exist in the authoritative research notes.
