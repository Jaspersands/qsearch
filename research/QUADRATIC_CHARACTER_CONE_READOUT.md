# Odd-dimensional quadratic-character copies: dual-cone readout

Follow-up, 2026-11-06: the separate reviewed composition in
AFFINE_QUADRATIC_CHARACTER_SLICE_READOUT.md handles every affine quadratic
with invertible quadratic part, n>=3 and p>=256T=O(n^2), from global pure
copies, including both parities. It uses measured random slices and paid
homogenization. This note's stronger direct-cone threshold and its
odd-dimensional mechanism remain unchanged; its extension gates refer
to this direct operation, not that separate slice-lift construction.

Derived 2026-11-05; independently reviewed and checkpointed 2026-11-06.
This note gives a bounded polynomial-time
receiver for a specified global pure-copy source. It attributes the mechanism
to standard quadratic Gauss sums, finite-field quadratic geometry, and linear
learning of a quadratic vanishing relation. It makes no novelty, separation,
quantum-execution, or new BIT/raw-phase-oracle upper-bound claim.

## 1. Exact contract and theorem

Let `p` be an odd prime, let `n >= 3` be odd, and let
`A in Sym_n(F_p)` be unknown and invertible. Write

\[
 Q_A(x)=x^T A x,\qquad
 \lambda(t)=\begin{cases}1&t=0,\\ \chi(t)&t\ne0,\end{cases}
\]

where `chi` is the quadratic character, extended by `chi(0)=0` when used
separately from `lambda`. The input is a supply of **fresh exact pure copies**

\[
 |\phi_A\rangle=p^{-n/2}\sum_{x\in\mathbb F_p^n}
                 \lambda(Q_A(x))|x\rangle.
\]

The required output is `A` up to multiplication by a nonzero field scalar.
The receiver receives neither field values of `Q_A` nor samples from its
zero cone. It uses no controlled unknown unitary, no chosen-line source, and
no additional unknown-function queries.

**Theorem.** For every such `A`, every prime `p >= 16 n^2`, and every
`0 < eta < 1`, a bounded receiver returns a matrix proportional to `A` with
probability at least `1-eta`, using polynomially many elementary gates and
classical bit operations in `n`, `log p`, and `log(1/eta)`. Define

\[
 d=\frac{n(n+1)}2-1,\qquad
 R=\left\lceil\log_2(4/\eta)\right\rceil,\qquad
 K=\left\lceil8\ln(4R/\eta)\right\rceil.
\]

At most `L = R(d+K)` source copies are consumed. A failed bounded run reports
ABORT; both ABORT and an incorrect output are included in the failure budget.
The source promise is exact and tensor-product fresh. This note makes no
extension to even dimension, singular forms, small primes, or noisy sources.

A native padded-character BIT oracle, or an uncontrolled phase oracle for
`lambda(Q_A(x))`, can prepare the source with one query on a uniform input,
with ordinary preparation precision charged below. That implication is not
the distinctive claim here: the accompanying source audit already obtains
the BIT/raw-phase oracle upper bound from existing univariate degree-two
reconstruction on `O(n^2)` chosen affine lines. The present theorem starts
from global copies alone.

## 2. Exact Fourier distribution

Put `k=(n-1)/2`, `B=A^{-1}`, and

\[
 q(y)=y^TBy,\qquad
 \epsilon=\chi((-1)^k\det A)\in\{+1,-1\}.
\]

Use the normalized additive Fourier transform with kernel
`p^{-n/2} exp(-2 pi i x.y/p)`. Standard completion of the square and the
quadratic Gauss-sum identity give, for every `y`,

\[
 \sum_x\chi(Q_A(x))e_p(-x\cdot y)
 =\epsilon p^k
 \begin{cases}p-1&q(y)=0,\\-1&q(y)\ne0,\end{cases}
 \tag{1}
\]

and

\[
 \sum_{Q_A(x)=0}e_p(-x\cdot y)
 =p^{n-1}{\bf1}_{y=0}+\epsilon p^k\chi(q(y)).
 \tag{2}
\]

For completeness, write the character as a normalized additive Gauss sum
and the zero indicator as `p^{-1} sum_t e_p(t Q_A(x))`. For `t != 0`,

\[
 \sum_x e_p(tQ_A(x)-x\cdot y)
 =\chi(\det A)\chi(t)^n G^n e_p(-q(y)/(4t)),
 \qquad G^2=\chi(-1)p.
\]

Since `n` is odd, the remaining sum in (1) is the elementary sum over
nonzero additive characters, while that in (2) is a quadratic Gauss sum.
This proves both identities including their values at `y=0`; no Gauss
phase has to be estimated or supplied to the receiver.

Because `lambda(Q_A)=chi(Q_A)+1_{Q_A=0}`, the Fourier amplitudes are exactly

\[
 \langle y|F|\phi_A\rangle=
 \begin{cases}
 p^{-1}+\epsilon(p-1)p^{-(n+1)/2},&y=0,\\
 \epsilon(p-1)p^{-(n+1)/2},&y\ne0,\ q(y)=0,\\
 \epsilon(-1+\chi(q(y)))p^{-(n+1)/2},&q(y)\ne0.
 \end{cases}
 \tag{3}
\]

An odd-dimensional nondegenerate quadratic has exactly `p^{n-1}` zeros.
Consequently a Fourier measurement lands in the **nonzero dual cone**

\[
 Z=\{y\ne0:q(y)=0\}
\]

with probability

\[
 \alpha=\frac{(p^{n-1}-1)(p-1)^2}{p^{n+1}}
        =(1-p^{-(n-1)})(1-p^{-1})^2
        \ge 1-\frac2p.
 \tag{4}
\]

Conditional on that event the label is exactly uniform on `Z`. Indeed, for
`n>=3`, the expression in (4) is at least
`(1-p^{-2})(1-p^{-1})^2 = 1-2/p+2/p^3-1/p^4`.
The event `y=0` is not silently discarded or renormalized: it is included
in the probability at most `2/p` outside `Z`.

## 3. Uniform escape from every proper relation subspace

Let `C` be any homogeneous quadratic not proportional to `q`. We prove

\[
 \Pr_{y\text{ uniform on }Z}[C(y)=0]\le\frac5p.
 \tag{5}
\]

Every nondegenerate quadratic form of dimension at least three over a
finite field of odd characteristic is isotropic. A Witt change of
coordinates therefore writes

\[
 q(u,v,z)=uv+h(z),\qquad z\in\mathbb F_p^{n-2},
\]

where `h` is nondegenerate. This change of coordinates is used only in the
proof; the algorithm does not know or compute it.

Write

\[
 C=a u^2+buv+cv^2+u\ell(z)+v m(z)+H(z),
\]

where `ell,m` are homogeneous linear and `H` is homogeneous quadratic.
The polynomial

\[
 P(z)=C(1,-h(z),z)
     =a+\ell(z)+(H(z)-bh(z))-h(z)m(z)+ch(z)^2
 \tag{6}
\]

has total degree at most four and is nonzero. To see nonzeroness, its
homogeneous terms of degrees zero through four would otherwise give
`a=0`, `ell=0`, `H=bh`, `h m=0`, and `c h^2=0`. The polynomial ring is a
domain and `h != 0`, so these identities force `C=bq`, a contradiction.

On the cone chart `u != 0`, write `z=u w` and `v=-u h(w)`. Homogeneity gives
`C(u,v,z)=u^2 P(w)`. Schwartz--Zippel therefore bounds the number of
`C`-zeros in this chart by

\[
 4(p-1)p^{n-3}.
\]

On the remaining chart `u=0`, one has `h(z)=0` and arbitrary `v`. Since
`n-2` is odd, `h` has exactly `p^{n-3}` zeros. There are thus at most
`p^{n-2}-1` nonzero cone points on this chart. Dividing by
`|Z|=p^{n-1}-1` gives

\[
 \Pr_Z[C=0]
 \le\frac{(5p-4)p^{n-3}-1}{p^{n-1}-1}
 \le\frac5p,
\]

as required. All constants are uniform in both `A` and `C`.

Let `D=n(n+1)/2`, and let `nu(y)` be the vector of degree-two monomials
`y_i^2` and `y_i y_j` for `i<j`. The coefficient vector of `q` annihilates
`nu(Z)`, so these vectors lie in its `(D-1)`-dimensional hyperplane `H_q`.
For every proper vector subspace `W` of `H_q`, its orthogonal complement
contains a quadratic `C` not proportional to `q`. Therefore

\[
 \Pr_Z[\nu(y)\in W]\le\Pr_Z[C(y)=0]\le5/p.
 \tag{7}
\]

In particular the full cone spans `H_q`. This proves uniform rank escape,
not an average-case claim about the hidden matrix.

## 4. One reconstruction attempt

Take `d=D-1` fresh copies, Fourier transform each, and measure labels
`y_1,...,y_d`. Form the matrix whose rows are `nu(y_i)`.

If its rank is not `d`, reject this attempt. Otherwise compute its
one-dimensional kernel, normalize its nonzero coefficient vector
projectively, and interpret it as a quadratic `C(y)=y^T M y`. Off-diagonal
matrix entries are half the corresponding monomial coefficients; `p` is
odd. If `M` is singular, reject the attempt. Otherwise `M^{-1}` is the
candidate output, subject to the fresh validation below.

Condition on any successful prefix whose labels lie in `Z` and whose
monomial rows are independent. Equations (4) and (7) show that the next
raw Fourier label is in `Z` and increases rank with probability at least

\[
 \alpha(1-5/p)\ge1-7/p.
\]

Thus the event that all `d` labels give the correct full-rank kernel has
probability at least

\[
 (1-7/p)^d\ge1-7d/p\ge9/16>1/2,
 \tag{8}
\]

where the last bound uses `d<=n^2` and `p>=16n^2`. On this event the kernel
is precisely `span(q)`, and the candidate inverse is proportional to `A`.
The procedure does not need to recognize or label individual contaminated
training outcomes.

## 5. Paid validation from fresh copies

For a candidate quadratic `C`, take a fresh source copy, Fourier transform,
measure `y`, and declare a validation success exactly when `C(y)=0`.
Equivalently this is the public projection

\[
 F^\dagger\left(\sum_{C(y)=0}|y\rangle\langle y|\right)F.
\]

It is implemented by Fourier measurement and ordinary evaluation of the
known quadratic. No candidate phase state or comparison oracle is needed.

If `C` is proportional to `q`, its validation probability is at least
`alpha >= 1-2/p`. If `C` is not proportional to `q`, equations (4)--(5)
give validation probability at most

\[
 \alpha\frac5p+(1-\alpha)\le\frac7p.
 \tag{9}
\]

The bound assigns all mass outside `Z`, including `y=0`, to the wrong
candidate. Since the theorem's threshold implies `p>=28`, the correct
probability is at least `3/4` and every wrong probability is at most `1/4`.
After `K` independent validations accept exactly when at least half
succeed. Hoeffding bounds either type of verification error by `exp(-K/8)`.
This holds conditionally on every training history because validation
uses fresh copies.

Projective scaling causes no gap here: `C` and every nonzero scalar
multiple define exactly the same validation projector. In particular it
is unnecessary to assume unit overlap between phase states belonging to
different scalar representatives.

## 6. Bounded schedule and resources

Run at most `R` independent reconstruction attempts, validate every
nonsingular candidate as above, and stop at the first accepted candidate.
Return ABORT if all attempts are exhausted. Conceptually preassign fresh
training and validation blocks to all attempts; early stopping can only
reduce the resource use.

By (8), the probability that none of the `R` training blocks has the
correct full-rank kernel is at most `2^{-R}`. Conditional on any training
history, a wrong acceptance or a correct rejection has probability at
most `exp(-K/8)` for each validation block. A union bound gives ideal
failure at most

\[
 2^{-R}+R e^{-K/8}\le\eta/2.
 \tag{10}
\]

There are at most `L=R(d+K)` Fourier samples. Use a standard uniform
approximate abelian QFT circuit for `F_p^n`, choosing its precision so the
induced channel error per sample, in the convention bounding event
probability differences, is at most `eta/(2L)`. A hybrid bound changes
(10) by at most `eta/2`. Such precision costs polynomially many gates in
`n`, `log p`, and `log(L/eta)`; it does not require a table with `p` entries.
If source copies are instead prepared by the native oracle, allocate the
same per-sample error budget between the public uniform preparation and
the public QFT. The theorem itself supplies exact copies.

Known-label processing uses `O(n^2)` field operations to form or evaluate
a quadratic feature row, polynomial-time Gaussian elimination in dimension
`D=O(n^2)`, and polynomial-time matrix inversion. For example, naive
elimination uses `O(D^3)` field operations per attempt. Field arithmetic
has polynomial bit cost in `log p`. No unknown matrix inverse is used
before learning a candidate. All source counts, statistical repetition
counts, and precision budgets are fixed before the run. Both active
workspace and total computation are polynomial in the stated parameters.

## 7. Attribution, access comparison, and claim gates

The Fourier focusing mechanism follows classical quadratic Gauss-sum
identities; the chart argument uses Witt decomposition and
Schwartz--Zippel; learning a unique quadratic from zero samples is linear
algebra. These ingredients are not asserted to be new.

Childs--Schulman--Vazirani, *Quantum algorithms for hidden nonlinear
structures*, arXiv:0705.2784, describes a hidden-polynomial oracle constant
on each level set and distinct on different level sets, and separately
uses specific sphere/shifted-subset source models. That general labeling
oracle is not the one-bit padded-character source here. Its results and
classical lower bounds do not transfer without an explicit reduction.
The locally read source is
`audits/sources/legendre_prf/hidden_nonlinear_0705_2784.txt`, introduction
and Section 2.

Roetteler, *Quantum algorithms to solve the hidden shift problem for
quadratics and for functions of large Gowers norm*, arXiv:0911.4724,
learns Boolean quadratic forms using additive Boolean phases. Its field,
phase encoding, and query contract differ from this odd-prime
multiplicative-character copy source. The locally read source is
`audits/sources/legendre_prf/roetteler_quadratic_0911_4724.txt`, introduction
and Section 2. Neither source comparison establishes priority for this
composition.

The stronger BIT/raw-phase access model already admits the chosen-line
composition described in the accompanying scope audit. A global copy
does not directly supply a selected affine-line copy: computational-basis
projection onto any one affine line succeeds with exactly `p^{1-n}`,
because the source has uniform magnitudes. This rules out treating that
particular projection as a free reduction; it is not a lower bound on
all possible copy-processing algorithms.

The claim gates **novelty**, **quantum/classical separation**, **new native
oracle upper bound**, **quantum implementation/execution**, **noise
robustness**, **direct even-dimensional cone-readout extension**, and **small-prime-universal
recovery** must stay false. Finite controls can check or falsify the
identities and implementation conventions; the uniform theorem rests on
the derivation above. The next external-value question is whether this
exact global-copy reconstruction composition is already covered by a
published state-learning result, together with a matched access-model
comparison; the current note leaves that priority question open.

## 8. Closed review, classical comparison and finite falsifiers

The [independent scope and actual-text review](audits/reviews/2026-11-05-quadric-classical-scope.md)
accepts the complete theorem, including the exact padding terms, uniform
Witt-chart escape, matrix convention, bounded validation and precision.
The parent independently checked the same arguments. The reviewed prime
threshold and projective output are part of the theorem, not conveniences.
Square scalar multiples of A give exactly the same source. Nonsquare
scalar multiples have the same projective cone but need not have the same
padded source or zero-frequency mass; no exact scalar recovery is promised.

A concrete classical native-oracle baseline uses a random common direction
u and the lines tu+v for v=e_i or e_i+e_j. On the constant-probability event
that these normalized quadratics are squarefree, all p SIGN values of each
line determine its coefficients by exact first and second moment formulas.
The resulting costs are O(n^2 p) native queries and a safe O(n^3 p) field
operations including query assembly, with bounded retries. The audit gives
the proof and verifies all84 signed squarefree monic quadratic instances
over F7 (588 queries). Thus when p is polynomial in n, a polynomial-time
classical oracle baseline already exists. Its p dependence remains material
in the growing-prime regime; no classical time lower bound is proved.

A hypothetical worst-case classical poly(n,logp) character-query learner
would solve padded linear Legendre hidden shift through
Q_s=x1*x2+s*x3^2 plus hyperbolic pairs. The one-query simulation, projective
ratio and exact zero-shift repair are proved in the same audit; 2058 native
simulation checks and36 projective-ratio checks over F7 passed. This is an
implication, not hardness, and it is not a copy-only source reduction.

The [four-case control](classical_baselines/quadric_cone_control.py) and
[saved artifact](classical_baselines/quadric_cone_control.json) use exact
Sage fields/matrices and floating normalized FFTs. A native classical
full-table p5,n3 baseline ran first:125 original sign queries,6200 scalar-
class candidates,775000 candidate evaluations, exactly one projective
match. The Fourier source constructor receives only the native callable;
hidden matrices and their inverses are confined to diagnostic analysis.

| Source | Nonzero dual-cone mass | Zero-frequency mass | Full-cone feature rank |
|---|---:|---:|---:|
| p5,n3,I | 384/625 | 81/625 | 5 |
| p5,n3,2I | 384/625 | 1/625 | 5 |
| p5,n3,dense nonsingular | 384/625 | 1/625 | 5 |
| p3,n5,I | 320/729 | 121/729 | 14 |

All pointwise amplitude formulas pass with maximum floating error below
2.8e-16. Each full-cone kernel gives A^-1 projectively, then inversion gives
A projectively. Replacing the actual padded source by a renormalized
chi(0)=0 source changes the measured law in all four cases. That distinct
oracle is a negative control, not a free source conversion.

Every tested prime is BELOW 16n^2. In particular, at p3,n5 both the true
dual quadratic and the prescribed nonproportional candidate have EXACT
validation acceptance49/81. The parent checked this equality from the
exact artifact. Thus the finite data explicitly refute an unqualified
small-prime verifier guarantee. They check algebra and conventions only;
no coherent source, quantum circuit or full algorithm was executed.

Primary links for the model comparison are
[Russell--Shparlinski](https://arxiv.org/abs/quant-ph/0212016),
[Childs--Schulman--Vazirani](https://arxiv.org/abs/0705.2784),
[hidden symmetry subgroup problems, Proposition5](https://arxiv.org/abs/1107.2189),
and [Rotteler](https://arxiv.org/abs/0911.4724).
The local primary texts and their exact scope are identified in the review.
No additional parity/noise/parameter sweep is requested. Any next step must
justify its external native use or introduce a concrete paid operation.
