## Verdict

**Yes: the requested charged running-time form can be obtained in a nonempty growing-\(\ell\) regime.** The conditional-covariance proposal is valid, and the classical certificate can be repaired directly, without importing the defective proof.

Two qualifications matter:

1. **The contract’s literal fair clone halves the SNR.** For \(p=4\), optimizing the classical hierarchy on the original input can erase the nominal quartic exponent advantage.
2. A **declared biased-placement variant** of the same cloning operation avoids that constant SNR loss. I prove its law below rather than silently treating it as the contract’s fair operation.

This establishes a detector and a comparison with an explicit native spectral implementation—not hardness, novelty, recovery, or superiority to every classical algorithm.

## 1. Cheapest falsifiers first

These falsify shortcuts in the supplied proof, not the detector.

### Mask splitting is not conditional independence

For one edge, write \(A=(Y-q)/\sqrt{q(1-q)}\), with conditional mean \(\delta/\sqrt{q(1-q)}\). Then
\[
\operatorname{Cov}(MA,(1-M)A\mid x)
=-\zeta(1-\zeta)\frac{\delta^2}{q(1-q)}.
\]
Conditioning on the mask instead changes the guide mean. Neither interpretation supplies the independence needed by the original argument.

### Brennan Lemma 14 does not give exact native multilevel cloning

A fixed randomized map from one Bernoulli bit has output-event probabilities affine in the input bias. Two independent attenuated Bernoulli outputs would have an \(11\)-probability quadratic in that bias.

Already for \(p=4,k=3\),
\[
f(aaaa)=2/9,\qquad f(aaab)=-1/9,\qquad f(aabb)=1/9.
\]
A nonconstant quadratic cannot agree with an affine function at all three biases. Thus the supplied two-bias lemma cannot automatically give the proposed exact multilevel product output.

### The primary ordered-certificate calculation loses a multiplicity

For \(p=4,\lambda=1\), take \(S=\{1,2,3,4\}\), \(T=\{1,2,5,6\}\). With the supplied normalized symmetrized encoding,
\[
\langle S|\mathcal K|T\rangle=2A_{\{3,4,5,6\}},
\]
not \(A_{\{3,4,5,6\}}\): there are \(24\cdot2\) compatible ordered pairs, divided by \(24\).

Consequently, the passage from the ordered sum (54) to the unweighted expression (56) is not an identity. This alone need not invalidate the asymptotic certificate constant, but its proof cannot simply be imported.

Also, matrix Bernstein must bound the summands \(A_E\mathcal K^{(E)}\), not just \(\mathcal K^{(E)}\). Its boundedness parameter contains \(q^{-1/2}\). The \(q\)-dependent fourth moments in the guide analysis likewise cannot be hidden in uniform constants.

The construction below replaces these steps.

## 2. Parameters and the single-input transformation

Let
\[
d=p/2,\qquad M=\binom np,\qquad \lambda=\ell/p,
\]
with fixed even \(p\ge4\), fixed \(k\ge3\), and
\[
(\log n)^{2/(p-2)}\ll\ell=o(\sqrt n).
\tag{1}
\]
Choose a sufficiently large, computable constant \(C=C_{p,k}\), and target matrix SNR
\[
b=Cn^{-p/4}\ell^{1/2-p/4}\sqrt{\log n}.
\tag{2}
\]
Constant-factor slack in (2) accommodates rational implementation.

Write the original SNR as
\[
\beta_0=\frac{\epsilon_0}{\sqrt{q(1-q)}}.
\]

Choose a placement probability \(0<\zeta\le1/2\). The guide receives the original attenuated bit with probability \(\zeta\); the matrix receives it otherwise. Require
\[
\beta_0\ge \frac b{1-\zeta}.
\tag{3}
\]
If the signal is stronger and known, first retain each original bit with probability
\[
t=\frac{b}{(1-\zeta)\beta_0},
\]
otherwise replacing it by a fresh \(\operatorname{Bern}(q)\) bit. This gives
\[
\beta_a=t\beta_0=\frac b{1-\zeta}.
\]

For each edge independently, randomly place the attenuated bit and a fresh \(\operatorname{Bern}(q)\) bit in the two outputs. **Discard the placement mask.** The two marginal SNRs are
\[
\beta_K=b,\qquad
\beta_G=h=\frac{\zeta}{1-\zeta}b.
\tag{4}
\]

This uses one observed hypergraph, null randomness, and \(O(M)\) edge operations. It uses no labels or second planted sample.

If \(\epsilon_0\) is not known sufficiently accurately, the construction instead needs a declared near-threshold SNR interval; arbitrary stronger unknown signals are not covered by the attenuation claim.

### Exact law and TV budget

For one edge, let \(\delta=\epsilon_a f_x(E)\). The marginals have parameters
\[
r_K=q+(1-\zeta)\delta,\qquad r_G=q+\zeta\delta.
\]
Relative to their independent product, the joint probabilities differ by
\[
(-,+,+,-)\,\zeta(1-\zeta)\delta^2.
\]
Therefore
\[
\chi^2(R_E\|\operatorname{Bern}(r_K)\otimes\operatorname{Bern}(r_G))
=
\frac{\zeta^2(1-\zeta)^2\delta^4}
{r_K(1-r_K)r_G(1-r_G)}.
\tag{5}
\]

For the literal fair operation, this is exactly the formula in the contract, and
\[
\operatorname{TV}\le
\frac12\sqrt{\exp(M\beta_a^4)-1}.
\tag{6}
\]
At \(\beta_a=2b\), its exponent is
\[
O\!\left(\ell^{2-p}\log^2 n\right)=o(1)
\]
under (1).

For the biased variant, Hölder gives the uniform native bound
\[
|f|\le F_{p,k}:=\frac{(k-1)^p+k-1}{k^p}<1.
\]
Thus every denominator in (5) is bounded below by a fixed-\((p,k)\) multiple of \(q^2(1-q)^2\), giving
\[
\operatorname{TV}\le
\frac12\sqrt{
\exp\!\left(C_{p,k}M\zeta^2(1-\zeta)^2\beta_a^4\right)-1}.
\tag{7}
\]
With \(L=\lceil\log n\rceil\) and \(\zeta=1/L\), the exponent is \(O(\ell^{2-p})\), hence vanishes for growing \(\ell\).

These bounds hold **uniformly for each fixed label vector**. They therefore also bound TV for the joint law containing the hidden labels, and after averaging over the primary planted prior. Under the null, the ideal transformation gives two exactly independent null graphs; finite sampling precision adds its separately budgeted error.

TV is transferred once through the entire subsequent algorithm. It is not multiplied by the number of guide or filter calls. Conversely, quantum repetition does not remove a nonvanishing model-TV budget.

## 3. The proposed conditional covariance bound is valid

Work in the Hilbert space indexed by ordered tuples of unordered edges. Let \(\Pi\) retain vertex-disjoint tuples. For independent real coordinates
\[
A_e=m_e+\xi_e,\quad \mathbb E\xi_e=0,\quad
D=\operatorname{diag}(\mathbb E\xi_e^2)\preceq vI,
\]
put
\[
U=\Pi A^{\otimes\lambda},\qquad V=\Pi m^{\otimes\lambda}.
\]
Because every retained tuple has distinct edge indices,
\[
\mathbb E U=V.
\]

Expand the centered products. A term survives only when the selected noise-edge indices on the row and column sides match as sets. For \(j\) selected indices, choose the row positions, column positions, and their bijection. Each resulting matrix is
\[
\Pi R\left[
D^{\otimes j}\otimes
|m^{\otimes(\lambda-j)}\rangle
\langle m^{\otimes(\lambda-j)}|
\right]C^*\Pi,
\]
where \(R,C\) are coordinate-permutation unitaries.

These are **two-sided permutations, not partial transposes**. The matrices need not individually be positive semidefinite; the operator-norm triangle inequality suffices. Overlaps among remaining mean indices are retained in the rank-one factor.

Hence
\[
\|\operatorname{Cov}(U)\|
\le
\sum_{j=1}^{\lambda}
\binom{\lambda}{j}^{2}j!\,
v^j\|m\|^{2\lambda-2j},
\tag{8}
\]
and, when \(m\ne0\),
\[
\|\operatorname{Cov}(U)\|
\le
\|m\|^{2\lambda}
\left[
\exp\!\left(\frac{\lambda^2v}{\|m\|^2}\right)-1
\right].
\tag{9}
\]

No averaging over labels, entrywise covariance signs, or label-independent direction is used. In particular, this avoids both the supplied Lemma 58 counterexample and the label-dependent-direction problem in its application.

## 4. Repairing the actual classical certificate and ordered interface

Here is an independent proof of the certificate needed by the detector.

### Specify the missing tensor extension

Set
\[
T_{i_1,\ldots,i_p}=
\begin{cases}
A_{\{i_1,\ldots,i_p\}},&\text{all indices distinct},\\
0,&\text{otherwise}.
\end{cases}
\tag{10}
\]
Use the supplied ordered bosonic Kikuchi matrix with this tensor. Nonzero transitions change exactly \(d\) positions to distinct vertices outside the original tuple.

This convention is essential: a hypergraph input does not supply repeated-index tensor entries.

### A positive-semidefinite lift of the mean

For fixed labels define
\[
w_c(i)=1[x_i=c]-1/k,\qquad
F=\sum_{c=1}^k w_c^{\otimes p}.
\]
Thus \(F_{i_1,\ldots,i_p}=f(x_{i_1},\ldots,x_{i_p})\), including repeated indices in this auxiliary tensor.

On the full ordered \(\ell\)-register space define
\[
B=
\sum_{\substack{J\subseteq[\ell]\\|J|=d}}
\sum_{c=1}^k
\left(\bigotimes_{a\in J}|w_c\rangle\langle w_c|\right)
\otimes I_{J^c}.
\tag{11}
\]
Every summand is positive semidefinite, and
\[
\|B\|\le C_{p,k}n^d\ell^d.
\tag{12}
\]

Let \(\Pi_{\rm cf}\) retain ordered tuples with no repeated vertices. The actual conditional mean satisfies
\[
b^{-1}\mathbb E[\mathcal K\mid x]
=\Pi_{\rm cf}B\Pi_{\rm cf}-E,\qquad
\|E\|\le C_{p,k}\ell^dn^{d-1}.
\tag{13}
\]
For each row and each \(J\), the omitted transitions use an old changed vertex among the new changed vertices. There are \(O(n^{d-1})\) such assignments. A symmetric absolute-row-sum bound proves (13), including multiplicities.

### Energy of the actual certificate

Set
\[
|\phi\rangle=(F/\|F\|)^{\otimes\lambda}.
\]
The following bounds hold uniformly in the labels, so balanced-label averaging is unnecessary for this coarse-constant repair.

Let \(G_{ab}=\langle w_a,w_b\rangle\). Since \(p\) is even,
\[
\|F\|^2=\sum_{a,b}G_{ab}^{p}
\ge \sum_a\|w_a\|^{2p}
\ge k(n/k^2)^p.
\tag{14}
\]
Also \(|F_{\boldsymbol i}|\le1\), so \(\|F\|^2\le n^p\).

For one marked position of one block, define
\[
H_c=
\frac{\|(\langle w_c|\otimes I^{p-1})F\|^2}{\|F\|^2}.
\]
Cauchy–Schwarz and
\[
\left\langle w_c^{\otimes(p-1)},
(\langle w_c|\otimes I)F\right\rangle
=\sum_a G_{ca}^{p}\ge G_{cc}^{p}
\]
give
\[
H_c\ge \frac{G_{cc}^{p+1}}{\|F\|^2}
\ge n/k^{2p+2}.
\tag{15}
\]
For exactly balanced labels, direct calculation improves this to \(H_c=n/k^2\).

Consider only \(J\)'s marking one position in each of \(d\) different blocks. Their contribution is
\[
\langle\phi|B|\phi\rangle
\ge \binom{\lambda}{d}p^d\sum_c H_c^d
\ge c_{p,k}n^d\ell^d
\tag{16}
\]
for growing \(\lambda\). Dropping the other terms is legitimate because they are positive semidefinite.

The squared-amplitude distribution of a block \(F/\|F\|\) has:

- probability \(O(1/n)\) of an internal collision;
- maximum one-coordinate marginal \(O(1/n)\).

A union bound therefore gives
\[
\|(I-\Pi_{\rm cf})\phi\|^2=O(\ell^2/n).
\tag{17}
\]
Projection changes the normalized state by \(O(\ell/\sqrt n)=o(1)\). Combining (12)–(17), the projected certificate has conditional mean Rayleigh quotient at least
\[
c_{p,k}b\,n^d\ell^d.
\tag{18}
\]

### This is the primary certificate in the correct encoding

Map an unordered edge to
\[
J|E\rangle=\frac1{\sqrt{p!}}\sum_{\pi\in S_p}|\pi(E)\rangle.
\]
This is an isometry. After global collision projection,
\[
J^{\otimes\lambda}\Pi(f_E)^{\otimes\lambda}
=(p!)^{-\lambda/2}\Pi_{\rm cf}F^{\otimes\lambda}.
\tag{19}
\]
The scalar cancels in normalization. No full-\(\ell\) symmetrization or invariant block-symmetric subspace is being assumed. The Hamiltonian acts on the full ordered space.

### Correct noise bound

The row degree is
\[
D_\ell=\binom{\ell}{d}(n-\ell)_d=O(\ell^dn^d).
\]
For each edge, \(\|\mathcal K^{(E)}\|\le d!\), and
\[
\left\|\sum_E(\mathcal K^{(E)})^2\right\|
\le d!D_\ell.
\]
Conditional variances of the standardized Bernoulli entries are at most \(2\), while centered summands are bounded by \(O(q^{-1/2})\). Matrix Bernstein therefore gives, uniformly in \(x\),
\[
\|\mathcal K-\mathbb E[\mathcal K\mid x]\|
\le
C_p\left[
\sqrt{n^d\ell^{d+1}\log n}
+q^{-1/2}\ell\log n
\right]
\tag{20}
\]
with probability \(1-o(1)\). The same bound controls the null matrix.

Feasibility \(\epsilon_a<q\) implies \(q\gtrsim b^2\). At (2), both terms in (20) are a sufficiently small constant fraction of
\[
S=b n^d\ell^d
\]
when \(C_{p,k}\) is chosen large enough.

Thus there are explicit constant-separated null/reject and planted/pass energy windows of width \(\Theta(S)\). The repaired certificate has constant mass in the pass eigenspace: its Rayleigh quotient is \(\Omega(S)\), and the matrix norm is \(O(S)\).

**This closes the classical-certificate gate without invoking Lemmas 33–35 as proved results.**

## 5. Guide norm, preparation probability, and useful overlap

Analyze first the ideal pair, independent conditional on \(x\). Build the guide from its second graph:
\[
A_e^G=\frac{Y_e^G-q}{\sqrt{q(1-q)}},\qquad
m_e=hf_x(e),\qquad
U=\Pi(A^G)^{\otimes\lambda},\quad V=\Pi m^{\otimes\lambda}.
\]

From (14) and removal of \(O(n^{p-1})\) repeated-index entries,
\[
\|m\|^2\asymp_{p,k}h^2M.
\]
The edge weights \(m_e^2/\|m\|^2\) have vertex incidence mass \(O(1/n)\), hence
\[
\|V\|^2=(1-O(\ell^2/n))\|m\|^{2\lambda}.
\tag{21}
\]

Let \(P_{\rm hi}\) be the matrix’s pass-space projector. The preceding certificate proof gives
\[
\|P_{\rm hi}V\|\ge c\|V\|.
\]
Condition on \(x\) and the matrix graph, and take
\[
s=P_{\rm hi}V/\|P_{\rm hi}V\|.
\]
Using (9), conditional Chebyshev gives
\[
\langle s,U\rangle\ge\tfrac12\|P_{\rm hi}V\|
\]
except with probability
\[
O(\rho),\qquad
\rho=\frac{\lambda^2}{h^2M}.
\tag{22}
\]
Here
\[
\rho=
\begin{cases}
O\!\left(\dfrac{\ell^{d+1}}{n^d\log n}\right),&\zeta=1/2,\\[1ex]
O\!\left(\dfrac{\ell^{d+1}\log n}{n^d}\right),&\zeta=1/\lceil\log n\rceil,
\end{cases}
\]
which tends to zero throughout (1).

### Actual guide norm—not just its expectation

Because the guide bias satisfies \(\epsilon_G\le q/2\), its conditional coordinate second moments lie between fixed positive constants. Scalar Bernstein, followed by a union bound over vertices, gives
\[
cM\le\sum_e(A_e^G)^2\le CM,\qquad
\max_i\sum_{e\ni i}(A_e^G)^2\le CM/n
\tag{23}
\]
with probability \(1-o(1)\), provided \(qM/n\gg\log n\).

This condition follows from feasibility and (2):
\[
qM/n\gtrsim (n/\ell)^{d-1}\log n.
\]
Consequently,
\[
\|U\|^2\le(CM)^\lambda,
\qquad
\eta_{\rm cf}:=\frac{\|U\|^2}{\|A^G\|^{2\lambda}}
\ge1-O(\ell^2/n).
\tag{24}
\]
Thus collision projection has asymptotically unit success probability.

Combining (21)–(24),
\[
\frac{\|P_{\rm hi}U\|^2}{\|U\|^2}
\ge h^{2\lambda}\exp(-O_{p,k}(\ell))
\tag{25}
\]
with probability \(1-o(1)\).

This is a conditional-direction argument; no signed covariance terms or overlapping-label tuples have been discarded.

## 6. An actual charged quantum implementation

Clone once, store the two resulting classical graphs, and reuse them. Do not manufacture fresh “independent samples” during amplification.

### Input, randomness, and bit costs

Read all \(M\) input bits and the parameter representations. Let \(B\) be their bit length. Generating the attenuated/cloned graphs costs
\[
O(M\,\operatorname{poly}(B,\log n))
\]
bit operations conservatively.

For truncated Bernoulli sampling, use
\[
O(\log(M/\eta_{\rm samp}))
\]
random bits of precision per probability, giving total sampling-TV error at most \(\eta_{\rm samp}\). Exact rational sampling is an alternative with its arithmetic and tail costs charged.

Arbitrarily long parameter representations are not free: the final cost retains polynomial dependence on \(B\).

### Guide preparation without QRAM

Compute the amplitude table for \(A^G\), including its normalization. A generic compiled state-preparation circuit on the \(M\)-coordinate register costs
\[
O(M\,\operatorname{poly}(B,\log M,\text{precision}))
\]
gates per invocation. Prepare \(\lambda\) copies, apply the explicit isometry \(J\), and reversibly test all vertex collisions.

Use coherent fixed-point amplification of the collision-free branch. By (24), this requires only precision-dependent logarithmic overhead, not an uncharged postselection assumption. Guide preparation and its inverse are both charged at every outer call.

### Hamiltonian access and filtering without QRAM

A row-neighbor circuit enumerates the changed positions and new vertices in \(\operatorname{poly}(\ell,\log n)\) gates. An entry circuit forms the unordered changed edge and **scans the stored \(M\)-bit table**, costing
\[
O(M\,\operatorname{poly}(\ell,\log n,B,\text{precision}))
\]
gates per lookup.

A sparse block encoding may use normalization
\[
\alpha=O(D_\ell/\sqrt q).
\]
The energy-window separation is \(\Delta=\Theta(S)\), so a coherent spectral filter needs
\[
\widetilde O(\alpha/\Delta)
=\widetilde O\!\left(\frac1{b\sqrt q}\right)
\tag{26}
\]
such calls, with logarithmic dependence on the filter error. Feasibility gives
\[
\frac1{b\sqrt q}=O(b^{-2})
=O\!\left(\frac{n^{p/2}\ell^{p/2-1}}{\log n}\right).
\]
This is polynomial in \(n^p\) in the declared regime. It is **not** a claim that the entire filter costs only \(O(n^p)\).

### Amplification and precision

From (25), the required outer guide/filter call count is
\[
R=h^{-\lambda}\exp(O_{p,k}(\ell))
\,\operatorname{polylog}(1/\eta).
\tag{27}
\]
Use a coherent acceptance flag and amplitude amplification with the known lower bound.

For null soundness, make the filter’s false-pass probability \(o(\eta^2/R^2)\). Make accumulated implementation error across all calls \(o(\eta)\). This requires
\[
O(B+\log R+\log(1/\eta))
=O(B+\ell\log n+\log(1/\eta))
\]
precision bits, not constant precision. Internal gate synthesis and simulation errors must be subdivided accordingly.

A conservative total bound is
\[
T\le
M\,\operatorname{poly}(B,\log n)
+
R\,\widetilde O\!\left[
M\left(\lambda+\frac1{b\sqrt q}\right)
\operatorname{poly}(\ell,B,\log R,\log(1/\eta))
\right].
\tag{28}
\]
For \(B\le\operatorname{poly}(n^p)\) and inverse-polynomial \(\eta\), this has the requested form
\[
\boxed{
T=n^{\ell/4}\exp(O_{p,k}(\ell\log\ell))\,
\operatorname{chargedpoly}(n^p).
}
\tag{29}
\]

Classical storage is polynomial in \(M\) and the precision; the quantum registers need polynomially many precision/work bits in addition to \(O(\ell\log n)\) index bits. No \(n^\ell\)-length state is materialized. The output is one bit, with \(O(1)\) output cost.

Statistical, sampling, and implementation errors sum to \(o(1)\). The cloned-input TV error transfers through the complete quantum computation under both hypotheses.

## 7. Parameter losses and the same-input classical comparison

### Literal fair clone: sufficient for (29)

Here
\[
\beta_0\ge2b,\qquad h=b.
\]
The leading call count is
\[
R=
n^{\ell/4}
\ell^{\,\ell(1/4-1/(2p))}
(\log n)^{-\ell/(2p)}
\exp(O(\ell)).
\]

But the same original input has SNR approximately \(2b\). Writing \(a=(p-2)/4\), the repaired classical threshold permits hierarchy order approximately
\[
\ell_{\rm cl}=2^{-1/a}\ell
=2^{-4/(p-2)}\ell,
\tag{30}
\]
using the same threshold constant.

**For \(p=4\), \(\ell_{\rm cl}\approx\ell/4\).** Thus its native spectral leading cost \(n^{\ell_{\rm cl}}\) matches the quantum leading power \(n^{\ell/4}\), before the quantum overhead. The fair-clone repair does not establish a same-input quartic advantage in this priority case.

### Declared biased-placement modification

With \(\zeta=1/\lceil\log n\rceil\),
\[
\beta_0\ge \frac b{1-\zeta}=b(1+O(1/\log n)),
\qquad h=\frac b{L-1}.
\]
Then
\[
R=
n^{\ell/4}
\ell^{\,\ell(1/4-1/(2p))}
(\log n)^{\ell/(2p)}
\exp(O(\ell)),
\]
which still satisfies (29) under (1).

The same-input classical hierarchy becomes
\[
\ell_{\rm cl}\approx(1-\zeta)^{4/(p-2)}\ell
=\ell(1-O(1/\log n)).
\]
For subpolynomial \(\ell\), this supports a nearly quartic comparison **to this explicit repaired native spectral implementation**. The placement bias is a disclosed modification, not an invocation of Brennan’s exact two-bias lemma.

### Nonempty \(p=4\) example

Take
\[
q=1/4,\qquad
\ell=4\left\lceil(\log n)^2/4\right\rceil,\qquad
b=Cn^{-1}(\log n)^{-1/2}.
\]
Choose \(\beta_0=2b\) for the fair operation, or \(b/(1-1/L)\) for the biased variant, with harmless rational slack. Then \(\epsilon_0<q\) for large \(n\), all covariance and preparation errors vanish, and:

- fair-clone TV is \(O(1/\log n)\);
- biased-clone TV is \(O(1/\log^2 n)\);
- the charged runtime satisfies (29).

Attenuating a much stronger original signal does not justify comparing against a classical algorithm forced to use the larger, attenuated hierarchy.

## 8. Remaining obligations and scope

The central source gate is closed by the analytic construction above, subject to these explicit implementation obligations:

- enforce the zero repeated-index convention (10);
- use the ordered isometry (19), not an assumed interchangeable set/tensor interface;
- discard placement masks and analyze the product experiment only through the proved TV transfer;
- charge table scans, state-preparation inverses, filter calls, and \(O(\ell\log n)\)-scale precision;
- supply known signal information for attenuation, or declare a near-threshold promise.

Violating any of these breaks the stated proof.

Applicable planted-XOR refinements must still be evaluated on the **original** input parameters. The supplied excerpts do not establish a transfer of such refinements to this fixed-\(k\ge3\) native model, so I neither import them nor claim to beat them. Low-coordinate-degree results are not lower bounds on all algorithms.

No recovery, tomography, new-advantage, or novelty claim follows. The small counterexamples above are algebraic falsifiers of particular proof steps; no numerical enumeration or repository inspection was performed.