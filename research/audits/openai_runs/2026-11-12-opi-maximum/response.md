## Verdict

**For the table ensemble exactly specified, (MAXIMUM) is correct.** The calculation correctly handles balanced halfsets without replacement, ordered pairs including the diagonal, and Vandermonde rank \(\min(j,k)\).

Its algorithmic consequence needs a quantifier qualification:

- It removes the attained-maximum advice requirement **for a high-probability analysis over native tables**.
- It does **not** certify maximum attainment for every supplied table.
- The stationary positive-filter sampler needs no maximizing codeword or target oracle. Its implementation uses the known upper bound \(1\), local score evaluations, and a paid valid normalizer.
- Conditioned initial states still require paid preparation/sampling and membership tests.
- The identity-term efficiency guarantee requires the stated weights \(w_j=1/(M+1)\), or another explicit lower bound on \(w_0\).

The following is a symbolic audit of the supplied model, not verification of an unseen implementation or source theorem.

## 1. Exact second moment

Let \(\mathcal C\) be the \(q^k\) degree-\(<k\) polynomials, identified with their evaluations at the \(m\) distinct points. Write
\[
Z=\sum_{f\in\mathcal C} I_f,\qquad
\mu=\mathbb EZ=q^k2^{-m}.
\]

For one uniformly chosen \(q/2\)-element table \(T_i\):

- For equal values,
  \[
  \Pr(u\in T_i)=\frac12.
  \]
- For distinct values,
  \[
  \Pr(u,v\in T_i)
  =\frac{(q/2)(q/2-1)}{q(q-1)}
  =\frac{q-2}{4(q-1)}.
  \]

The second formula is the required **without-replacement** calculation. Replacing it by \(1/4\) would change the result.

Set
\[
a=\frac{q-2}{q-1},\qquad \beta=2-a=\frac q{q-1}.
\]
Independence between rows gives
\[
\mathbb E[I_fI_g]
=4^{-m}\prod_{i=1}^m
\left[a+\beta\,\mathbf 1_{\{(f-g)(a_i)=0\}}\right].
\]

### Ordered differences and the diagonal

For every \(h\in\mathcal C\), including \(h=0\), there are exactly \(q^k\) **ordered** pairs \((f,g)\) with \(f-g=h\). Consequently,
\[
\frac{\mathbb EZ^2}{\mu^2}
=\mathbb E_{h\text{ uniform in }\mathcal C}
 \prod_{i=1}^m\left[a+\beta\,\mathbf 1_{\{h(a_i)=0\}}\right].
\]
There is no \(q^k-1\) denominator and no exclusion of the diagonal.

For a specified \(j\)-subset \(J\), the evaluation map
\[
h\longmapsto (h(a_i))_{i\in J}
\]
has rank \(\min(j,k)\):

- Any \(j\le k\) distinct Vandermonde rows are independent.
- Once \(j\ge k\), \(k\) of the rows already have rank \(k\).

Thus
\[
\Pr_h[h(a_i)=0\ \forall i\in J]=q^{-\min(j,k)}.
\]
Expanding the product proves the exact identity
\[
\frac{\mathbb EZ^2}{\mu^2}
=\sum_{j=0}^m
\binom mj a^{m-j}\beta^j q^{-\min(j,k)}.
\]

Now
\[
a+\frac{\beta}{q}=1.
\]
Therefore
\[
V:=\frac{\operatorname{Var}Z}{\mu^2}
=\sum_{j=k+1}^m
\binom mj a^{m-j}\beta^j(q^{-k}-q^{-j}).
\]
Every summand is nonnegative, and
\[
V
\le q^{-k}\sum_{j=k+1}^m\binom mj a^{m-j}\beta^j
\le q^{-k}(a+\beta)^m
=\frac{2^m}{q^k}.
\]
Since \(Z=0\) implies \(|Z-\mu|\ge\mu\),
\[
\boxed{\Pr(Z=0)\le \min\!\left(1,\frac{2^m}{q^k}\right).}
\]

One can sharpen the final probability conversion: Cauchy–Schwarz gives
\[
\Pr(Z=0)\le \frac{V}{1+V}
\le \frac{2^m/q^k}{1+2^m/q^k}.
\]
This is not needed for (MAXIMUM).

**Analytic control:** for \(k=m\), the variance sum is empty. Indeed, all evaluation vectors occur and
\[
Z=(q/2)^m
\]
deterministically. This checks the endpoint; it is not extrapolation from a finite example.

## 2. Growing parameters and the remaining exceptional tables

For \(q=2^t\),
\[
\frac{2^m}{q^k}=2^{m-tk}.
\]
At fixed \(R>0\), \(k=\lfloor Rm\rfloor\), \(m=q-1\),
\[
\log\frac{2^m}{q^k}
=-R\,m\log q+m\log2+O(\log q)
=-(R+o(1))m\log q.
\]
For example, once
\[
\frac{\log2}{\log q}+\frac1m\le \frac R2,
\]
the failure bound is at most
\[
\exp\!\left[-\frac R2m\log q\right].
\]

This is not uniform over arbitrary vanishing rates. For general \(k=k(q)\), the displayed bound tends to zero when
\[
tk-m\longrightarrow+\infty.
\]
Conversely, if \(tk-m\to-\infty\), Markov's inequality gives
\[
\Pr(Z>0)\le \mathbb EZ=2^{tk-m}\to0.
\]
Thus merely requiring \(R(q)>0\) is insufficient. Also, the stated model requires \(k\ge1\); \(\lfloor Rm\rfloor=0\) at small parameter values is outside it.

### A counterexample to deterministic maximum attainment

There are legal no-perfect-codeword tables for **every \(k<m\)**.

Choose \(k+1\) evaluation points. Their Vandermonde rows have a dependency
\[
\sum_{i\in J}c_i v(a_i)=0,
\]
with every \(c_i\ne0\), since any \(k\) rows are independent. Hence every allowed polynomial satisfies
\[
\sum_{i\in J}c_i f(a_i)=0.
\]

Choose a nonzero \(\mathbb F_2\)-linear functional
\(\ell:\mathbb F_q\to\mathbb F_2\), and bits \(b_i\) with
\(\sum_{i\in J}b_i=1\). Set
\[
T_i=\{y:\ell(c_i y)=b_i\}\qquad(i\in J).
\]
Each \(T_i\) has exactly \(q/2\) elements. A polynomial hitting all these tables would imply
\[
0=\ell\!\left(\sum_{i\in J}c_i f(a_i)\right)
=\sum_{i\in J}b_i=1,
\]
a contradiction. Other rows may be arbitrary balanced halfsets.

These table realizations have positive probability in the specified ensemble. They do **not** contradict (MAXIMUM), but they falsify any interpretation that the native format itself guarantees \(H_{\max}=m\).

### What is known on the good event

Let \(\mathcal E=\{Z>0\}\). On this single event,
\[
H_{\max}=m,\qquad
G(f)=\frac12+\frac{H(f)}{2m},\qquad G_{\max}=1.
\]

For uniform coefficients \(\pi\), each individual evaluation is uniform whenever \(k\ge1\). Therefore, for **every fixed balanced-table instance**,
\[
\mathbb E_\pi H=m/2,\qquad \mathbb E_\pi G=3/4.
\]
On \(\mathcal E\), the maximum-minus-mean gap is \(1/4\). That is not a claim that the standard deviation or full range is \(1/4\).

The event is independent of later choices of \(b,s,M,\nu,T,S\). Deterministic conclusions proved on it hold simultaneously for all admissible choices; no parameter union bound is needed.

Existence is not search. Indeed, the same variance estimate gives \(Z/\mu\to1\) in probability at fixed rate, so the perfect-codeword fraction is typically approximately \(2^{-m}\). Uniform rejection would therefore still take approximately \(2^m\) trials. **This is not a lower bound on other search algorithms.**

## 3. DIAGONAL and the exact stationary-output sampler

Write
\[
B=D(P_s)+bG,\qquad K=P_s+bG,
\]
and define the actual filter
\[
C=\sum_{j=0}^M w_j\nu^{-j}B^j,
\qquad w_j=\frac1{M+1}.
\]
Assume \(0\le s\le1\), \(b\ge0\), reversibility, and a supplied valid \(\nu\ge E=\lambda_{\max}(B)\).

On \(\mathcal E\), the stationary Rayleigh quotient and a maximizing basis state give
\[
E\ge1+b\mathbb E_\pi G\ge1,
\qquad
E\ge1-s+b.
\]
The second inequality uses only \(P_0(x,x)\ge0\). It does not require finding the maximizing state.

Set
\[
\rho=\frac{1+b}{\nu},\qquad
A=\sum_{j=0}^M w_j\rho^j.
\]
Then
\[
\rho\le1+\frac{s}{E},
\]
so
\[
\boxed{A\le e^{sM/E}\le e^{sM}.}
\]
This is valid for arbitrarily large \(b\), with its representation and arithmetic costs still charged.

### The sampler

Define the substochastic kernel
\[
R=\frac{K}{1+b}.
\]
One step is implemented by:

- choosing a \(P_s\) step with probability \(1/(1+b)\);
- otherwise staying and surviving with probability \(G(x)\).

Let \(d_j=w_j\rho^j\). For each proposal:

1. Sample \(x\sim\pi\).
2. Independently choose two degrees with law \(d_j/A\).
3. Run two independent killed walks from this **same \(x\)**.
4. Accept if both survive, and output the **starting state \(x\)**.

Put
\[
F=\sum_{j=0}^M w_j\nu^{-j}K^j.
\]
One walk's survival probability is
\[
p(x)=\frac{F\mathbf1(x)}A.
\]
Reversibility gives
\[
(C|\pi\rangle)_x=\sqrt{\pi(x)}\,F\mathbf1(x).
\]
Hence the accepted output law is exactly
\[
\frac{\pi(x)[F\mathbf1(x)]^2}
{\sum_y\pi(y)[F\mathbf1(y)]^2},
\]
the normalized measurement law of \(C|\pi\rangle\).

The \(j=0\) term gives, pointwise,
\[
p(x)\ge\frac{1}{(M+1)A}.
\]
Therefore
\[
\boxed{\Pr(\text{accept})\ge
\frac{e^{-2sM}}{(M+1)^2}.}
\]
The constants and the square are correct.

Neither the maximizing codeword nor the output-state norm is needed. The scalar \(A\) is computed from the supplied parameters.

Moreover, the sampler remains **correct on exceptional tables**: \(1\) is always a valid upper bound on \(G\), so the killed kernel remains valid. What may fail there is the stated uniform efficiency bound.

### Identity-term restriction

For general normalized nonnegative weights, the corresponding guarantee is
\[
\Pr(\text{accept})\ge \frac{w_0^2}{A^2}.
\]
Thus “every positive average” must retain the stipulated uniform weights, or explicitly require inverse-polynomial \(w_0\). The diagonal and amplitude bounds extend to other convex weights, but the identity-term efficiency guarantee does not automatically do so.

## 4. Conditioned targets and \(S\subseteq T\)

For nonempty \(T\),
\[
|T\rangle=\frac1{\sqrt{\pi(T)}}\sum_{x\in T}\sqrt{\pi(x)}|x\rangle.
\]
The same similarity relation gives
\[
(C|T\rangle)_x
=\sqrt{\frac{\pi(x)}{\pi(T)}}\,F\mathbf1_T(x).
\]
Because \(R\) is substochastic,
\[
0\le F\mathbf1_T(x)\le A.
\]
Thus
\[
\boxed{\|\Pi_S C|T\rangle\|
\le A\sqrt{\frac{\pi(S)}{\pi(T)}}
\le e^{sM}\sqrt{\frac{\pi(S)}{\pi(T)}}.}
\]

The inequality itself holds for any \(S\). The condition \(S\subseteq T\) is what identifies
\[
\sqrt{\pi(S)/\pi(T)}=\|\Pi_S|T\rangle\|
\]
as the original marked overlap.

This is a bound on the **unnormalized heralded branch**. It must not be restated as a constant-factor bound on marked probability after free postselection. With the identity term one can instead deduce
\[
\Pr(S\mid\text{herald})
\le
\min\!\left(1,(M+1)^2e^{2sM}\frac{\pi(S)}{\pi(T)}\right).
\]
Postselection success costs remain part of the algorithm.

### Projected conditioned sampler

If \(x\sim\pi_T\) is available, run the same two walks and additionally require both endpoints to lie in \(T\). Then
\[
p_T(x)=\frac{F\mathbf1_T(x)}A.
\]
For \(x\in T\), both zero-degree choices pass the endpoint test, yielding the same acceptance lower bound.

The resulting law is exactly the normalized measurement law of
\[
\Pi_T C|T\rangle.
\]

It is **not** the complete law of \(C|T\rangle\) outside \(T\). Also, the walks may leave and reenter \(T\); replacing the endpoint test by “never leave \(T\)” generally changes the operator.

This does not remove a target-preparation oracle:

- Sampling \(\pi_T\) must be implemented and charged.
- Membership in \(T\) must be implemented and charged.
- Quantum preparation of \(|T\rangle\) must be implemented and charged.
- A global perfect codeword does not guarantee one inside an arbitrary restricted \(T\).

For \(T\) equal to the full coefficient space, uniform sampling/preparation is explicit. For a nontrivial target-conditioned \(T\), the second moment supplies no preparation method.

## 5. Normalizer, runtime, precision, and source-level obligations

### Known normalizer

The proof does not compute \(E\). It requires the numerical \(\nu\) actually used by the filter and a valid guarantee \(\nu\ge E\).

A simple safe choice is available:
\[
E\le1+b,\qquad \nu=1+b.
\]
For that choice \(A=1\), even without attainment. But substituting this value for another source normalizer generally changes the filter and its output law. It cannot silently establish equivalence to a differently normalized source algorithm.

### Charged runtime

On \(\mathcal E\), the expected number of proposals is at most
\[
(M+1)^2e^{2sM},
\]
and each proposal uses at most \(2M\) walk steps. Add:

- stationary or conditioned initial sampling;
- score evaluation and table access;
- mixer updates;
- degree-distribution preparation and sampling;
- endpoint membership tests;
- normalizer construction/certification;
- output of the \(kt\)-bit coefficient vector.

For example, straightforward score evaluation uses \(m\) polynomial evaluations and \(m\) table-membership accesses; it is not a free score oracle.

Thus the walk-count bound is \(O((M+1)^3e^{2sM})\), not automatically polynomial in the native input size. To obtain that conclusion, one additionally needs \(M\) and all paid primitives polynomial in the actual input size. Bounded \(sM\) alone permits enormous \(M\) when \(s\) is tiny.

High probability over tables also does not automatically imply polynomial **unconditional expected runtime**: exceptional-instance costs have not been bounded. A capped sampler can instead report failure. With
\[
a_0=\frac{e^{-2sM}}{(M+1)^2},
\]
a cap of \(a_0^{-1}\log(1/\delta)\) proposals has failure probability at most
\[
\Pr(\mathcal E^c)+\delta
\]
over tables and sampling randomness.

### Precision

For rational \(b,s,\nu\) and exact native tables, the degree probabilities and survival probabilities are rational. Exact arithmetic and exact rational sampling have bit costs polynomial in \(M\) and the parameter description lengths; those costs must be included.

For approximate primitives, rejection conditioning can amplify errors. To obtain output total-variation error \(O(\epsilon)\), a sufficient requirement is proposal-level error \(O(\epsilon a_0)\); a stepwise implementation must budget this across its \(O(M)\) random choices. Exact-law claims for unspecified real parameters require an additional access model.

### Degree prescription and spectral recurrence

Neither (MAXIMUM) nor the sampler proof needs a spectral-gap estimate.

For interpreting the supplied REG inequality, the stated native recurrence is consistent: outside the span of a \(j\)-subset, two different successful extensions would contradict independence of \(j+2\le k\) Vandermonde rows. This gives \(p_{k-1}\le(k-1)/m\), with equality for an evaluation row, and hence
\[
r=\frac{m-k+1}{m}\ge1-R.
\]
Conditional on the displayed REG prescription and on \(\gamma=1/4\),
\[
sM\le
\frac{4\log(1/(1-\eta))}{1-R}+1.
\]
This is constant at fixed \(R<1\) and fixed \(\eta<1\), not uniformly as \(R\to1\) or \(\eta\to1\). It supplies no log-Sobolev or optimization-hitting conclusion.

The excerpts do not independently establish that a particular source routine satisfies REG, implements precisely this filter, or has the asserted \(S\subseteq T_\eta\subseteq T\) geometry. Those remain source-level proof obligations.

### Unattained upper bounds

With a known upper bound \(\bar g\), actual maximum \(g_*\), and slack \(\Delta=\bar g-g_*\),
\[
1+b\bar g\le E+s+b\Delta,
\]
so
\[
A\le \exp\!\left(\frac{M(s+b\Delta)}E\right)
\le \exp[M(s+b\Delta)].
\]
The total exponent must be charged.

Conditional on the supplied interval assertion, \(b\le1\), and \(M\le M_{\max}\), the additional exponent would satisfy
\[
Mb\Delta\le
\frac{M_{\max}}{2n^2(M_{\max}+1)^2}.
\]
That algebra is valid; the claimed source interval guarantee is not independently verified here, and it cannot be extended to clipped trials without proof.

## Final scope

**No repair to (MAXIMUM) is needed.** The necessary repair is to overstrong algorithmic wording:

> With probability at least \(1-\min(1,2^m/q^k)\) over the specified native tables, the explicit score has attained maximum \(1\). On that event, the stated uniform positive filter has the exact stationary-output sampler and the \(S\subseteq T\) unnormalized-amplitude bound, uniformly over admissible parameters, subject to paid normalizer, access, precision, degree, and initial-conditioning costs.

This is neither a per-instance maximum certificate nor a perfect-codeword search algorithm, and it establishes no general hardness or quantum-speedup conclusion.