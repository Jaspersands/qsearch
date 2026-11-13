## Verdict

**Yes, for a sufficiently large fixed signal constant.** A connected, degree-two subfamily of even covers gives a **log-free classical detection upper bound for the exact Bernoulli input in the contract**.

The proof below is not an application of the supplied fixed-\(l\) HCE theorem. It supplies a uniform growing-order count and accounts for the additional covariance caused by shared vertices.

The resulting algorithm has
\[
\beta\ge \frac{D^{1/2}}{n\sqrt l},
\qquad l\le \tfrac18\log n,
\]
for an absolute constant \(D\), and runs in
\[
\bigl(n^4+n^{2l}\exp(O(l\log l))\bigr)
        \operatorname{poly}(B,l,\log n)
\]
bit operations. Consequently, in the window
\[
\beta=\frac{C}{n\sqrt{\log n}},
\]
it detects for every sufficiently large fixed \(C\), using \(l=\Theta(\log n)\) and time \(\exp(O(\log^2 n))\). This is asymptotically smaller than \(n^{\ell/4}\) when \(\ell=\Theta(\log^2 n)\).

This is a stronger same-input classical upper bound—not a contradiction of the quantum upper bound, nor a hardness or optimality claim.

---

## 1. Statistic and theorem

Let \(\mathcal H_l\) consist of simple \(4\)-uniform hypergraphs \(H\) satisfying:

* \(H\) has exactly \(l\) distinct hyperedges;
* every used vertex has degree exactly two, hence \(H\) uses \(2l\) vertices;
* the incidence graph is connected.

Write \(N_l=|\mathcal H_l|\), and define
\[
X_H=\prod_{E\in H}A_E,\qquad
T_l=\sum_{H\in\mathcal H_l}X_H.
\]

These are squarefree products of the actual observations. No repeated samples or planted labels are used.

### Theorem

There are absolute constants \(l_0,K,n_0\) such that the following holds. Suppose \(n\ge n_0\), \(l\) is even,
\[
l_0\le l\le \frac{\log n}{8},\qquad
0<\beta\le1,\qquad
D:=\beta^2n^2l\ge 2^{15}.
\]
For the exact \(p=4,k=3,q=1/4\) model, declare planting when
\[
T_l>\frac12N_l\left(\frac{\beta}{18}\right)^l. \tag{1}
\]
Each error probability is at most
\[
K\left(2^{-l}+l^2n^{-5/8}\right). \tag{2}
\]

The planted error is with respect to the specified iid uniform labels and the conditional Bernoulli observations.

The constants are deliberately unoptimized. For example, taking
\[
l=2\left\lfloor\frac{\log n}{16}\right\rfloor
\]
makes the theorem apply, for all sufficiently large \(n\), to every fixed \(C\ge1024\) in the contract’s signal window.

---

## 2. The actual multiclass contraction is positive

The XOR identity \(\mathbb E X_H=\rho^l\) is not valid here. The following special identity for three colors replaces it.

Choose regular-triangle vectors \(\psi_1,\psi_2,\psi_3\in\mathbb R^2\) with
\[
\psi_a\cdot\psi_b=3\mathbf1[a=b]-1.
\]
For a uniform color \(x\),
\[
\mathbb E\psi_x=0,\qquad
\mathbb E[\psi_x\psi_x^\top]=I_2.
\]
Also,
\[
\mathbf1[x=c]-\frac13=\frac13\psi_c\cdot\psi_x.
\]

The triangle’s fourth-moment identity gives, exactly,
\[
f_x(\{i,j,r,s\})
 =\frac1{54}\left[
 (\psi_{x_i}\!\cdot\psi_{x_j})(\psi_{x_r}\!\cdot\psi_{x_s})
 +(\psi_{x_i}\!\cdot\psi_{x_r})(\psi_{x_j}\!\cdot\psi_{x_s})
 +(\psi_{x_i}\!\cdot\psi_{x_s})(\psi_{x_j}\!\cdot\psi_{x_r})
 \right]. \tag{3}
\]
In particular,
\[
|f_x(E)|\le b:=\frac29. \tag{4}
\]

For a degree-two cover, expand one of the three pairings in (3) at every hyperedge. Averaging over labels joins the two incidences at each original vertex using
\(\mathbb E\psi_x\psi_x^\top=I_2\). The resulting closed index circuits each contribute a factor two. Thus
\[
t(H):=\mathbb E_x\prod_{E\in H}f_x(E)
 =54^{-l}\sum_{\sigma\in\{1,2,3\}^l}2^{c(H,\sigma)}, \tag{5}
\]
where \(c(H,\sigma)\) is the number of resulting circuits.

This is the centered-color tensor-network contraction. It depends on the cover; it is not a universal Boolean parity coefficient. Nevertheless, every summand is positive, so
\[
t(H)\ge 18^{-l}=:a^l. \tag{6}
\]

Conditional independence of the observations now yields
\[
\mathbb E_1T_l
 =\beta^l\sum_{H\in\mathcal H_l}t(H)
 \ge N_l(a\beta)^l=:\mu_* . \tag{7}
\]

The special \(p=4,k=3\) identity is doing substantive work here.

---

## 3. Exact count and growing-order control

Represent a degree-two cover by its dual multigraph:

* its \(l\) nodes are the hyperedges;
* each original vertex becomes an edge joining its two incident hyperedges.

The dual is a loopless, connected, \(4\)-regular multigraph. Parallel edges are allowed. For \(l\ge3\), connectedness excludes two nodes joined by four parallel edges, so the original hyperedges are distinct.

Let \(P_l\) be the number of pairings of \(4l\) labeled slots, grouped into \(l\) labeled boxes of size four, whose box multigraph is loopless and connected. Then the exact count is
\[
N_l=\frac{(n)_{2l}P_l}{l!(4!)^l}. \tag{8}
\]
Each cover is represented exactly \(l!(4!)^l\) times.

Put
\[
g_l=\frac{(4l-1)!!}{l!24^l},\qquad g_0=1.
\]

The pairing calculation underlying the supplied count gives
\[
\Pr(\text{no within-box pair})\longrightarrow e^{-3/2}.
\]
For completeness, the number of within-box pairs has factorial moments tending to \((3/2)^r\); Bonferroni bounds then give this zero-event limit.

Connectedness costs only \(o(1)\). Indeed, the probability that some set of \(s\le l/2\) boxes has no outgoing pair is at most
\[
\sum_{s=1}^{\lfloor l/2\rfloor}
 \binom ls
 \frac{(4s-1)!!(4l-4s-1)!!}{(4l-1)!!}
 =
\sum_{s=1}^{\lfloor l/2\rfloor}
 \frac{\binom ls\binom{2l}{2s}}{\binom{4l}{4s}}
 =O(l^{-1}). \tag{9}
\]
The last estimate follows uniformly from factorial bounds: its \(s\)-th summand is at most
\[
\frac{K}{\sqrt s}\exp[-l\,h(s/l)]
 \le \frac{K}{\sqrt s}(s/l)^s,
\]
where \(h\) is binary entropy.

Consequently, for an absolute \(c_*>0\), uniformly for sufficiently large \(l\) and \(l\le(\log n)/8\),
\[
c_*g_ln^{2l}\le N_l\le g_ln^{2l}. \tag{10}
\]
One may take \(c_*=e^{-3/2}/4\) after increasing the lower cutoffs.

This avoids exchanging the source’s fixed-\(l\) and large-\(n\) limits: (8) is exact, and \((n)_{2l}/n^{2l}=1-O(l^2/n)\) uniformly in this range.

We will use the elementary recurrence
\[
\frac{g_j}{g_{j-1}}
 =\frac{(4j-1)(4j-3)}{24j}
 \ge \frac j8.
\]
It implies
\[
g_l\ge \frac{l!}{8^l}\ge \left(\frac{l}{8e}\right)^l,
\qquad
\binom ls\frac{g_{l-s}}{g_l}\le\frac{8^s}{s!}. \tag{11}
\]

The familiar \(l^l\) cover-count enhancement is present: more precisely,
\(g_l\sim(\pi l)^{-1/2}[(2/(3e))l]^l\). The proof below needs only (10)–(11).

---

## 4. Exact covariance, including shared vertices

For the native Bernoulli variable,
\[
A_E=\frac{4Y_E-1}{\sqrt3},\qquad
\mathbb E[A_E\mid x]=\beta f_x(E),
\]
and
\[
\mathbb E[A_E^2\mid x]
 =1+\kappa\beta f_x(E),\qquad
\kappa=\frac2{\sqrt3}. \tag{12}
\]

For \(H,H'\in\mathcal H_l\), let \(J=H\cap H'\) and \(s=|J|\). Exactly,
\[
\mathbb E[X_HX_{H'}\mid x]
 =
 \beta^{2l-2s}
 \prod_{E\in H\triangle H'}f_x(E)
 \prod_{E\in J}(1+\kappa\beta f_x(E)). \tag{13}
\]
Because \(\beta\le1\) and \(|f|\le2/9\),
\[
\left|\mathbb E_1[X_HX_{H'}]\right|
 \le \beta^{2l-2s}b^{2l-2s}2^s. \tag{14}
\]
The individual unconditional means are positive by (5), so (14) also upper-bounds the covariance.

### No shared edge does not mean zero covariance

For \(s=0\), conditional covariance is zero, but after averaging over labels,
\[
\operatorname{Cov}_1(X_H,X_{H'})
 =\beta^{2l}\bigl(t(H\cup H')-t(H)t(H')\bigr). \tag{15}
\]
This need not vanish when vertices are shared.

If the vertex sets are disjoint, the two statistics are independent even unconditionally. The number of ordered pairs with any shared vertex is at most
\[
N_l^2\frac{4l^2}{n}, \tag{16}
\]
since every cover uses \(2l\) vertices and its vertex set is uniform under vertex permutations. Hence the contribution from edge-disjoint, vertex-intersecting pairs is at most
\[
N_l^2\beta^{2l}b^{2l}\frac{4l^2}{n}. \tag{17}
\]

### Shared-edge count

Let \(N_s\) count ordered cover pairs sharing exactly \(s\) edges, where \(1\le s<l\).

Fix \(H\), choose \(J\subset H\) of size \(s\), and set \(r=l-s\). Let \(u\) be the number of vertices occurring once in \(J\). Since \(H\) is connected and \(J\) is a nonempty proper subset,
\[
u\ge2.
\]
Also \(u\) is even.

A degree-two completion of \(J\) by \(r\) edges must use:

* each of the \(u\) boundary vertices once;
* \(2r-u/2\) additional vertices twice.

Ignoring simplicity restrictions only increases the count. Slot counting therefore bounds the number of completions by
\[
\begin{aligned}
&\frac{(4r)_u(4r-u-1)!!}{r!24^r}\,
       n^{2r-u/2}\\
&\qquad\le
g_rn^{2r}\left(\frac{4r}{n}\right)^{u/2}
\le \frac{4l}{n}g_rn^{2r}. \tag{18}
\end{aligned}
\]
Thus (10)–(11) give the uniform overlap bound
\[
\frac{N_s}{N_l^2}
 \le
 \frac{4l}{c_*n}\binom ls\frac{g_{l-s}}{g_l}n^{-2s}
 \le
 \frac{4l}{c_*n}\frac{8^s}{s!\,n^{2s}}. \tag{19}
\]

Connectedness is useful precisely here: it rules out a proper shared subcover with \(u=0\).

---

## 5. Variance bound and detection

Under the null, distinct squarefree edge monomials are orthogonal. Therefore
\[
\mathbb E_0T_l=0,\qquad \operatorname{Var}_0(T_l)=N_l. \tag{20}
\]

Under planting, combine:

* (17) for no shared edge;
* (14) and (19) for \(1\le s<l\);
* \(\mathbb E X_H^2\le2^l\) for identical covers.

Using \(b/a=4\) gives
\[
\boxed{
\frac{\operatorname{Var}_1(T_l)}{\mu_*^2}
\le
16^l\left[
 \frac{4l^2}{n}
 +\frac{4l}{c_*n}
   \left(\exp\!\frac{324}{\beta^2n^2}-1\right)
\right]
+\frac1{c_*}
 \left(\frac{5184e}{D}\right)^l .
} \tag{21}
\]
This is an explicit growing-order bound in the **original** signal parameter \(\beta\).

For \(D\ge2^{15}\),
\[
\frac{5184e}{D}<\frac12,\qquad
16^l\exp\!\left(\frac{324l}{D}\right)\le e^{3l}.
\]
With \(l\le(\log n)/8\), (21) is at most
\[
K\left(l^2n^{-5/8}+2^{-l}\right). \tag{22}
\]

Likewise, (10)–(11) imply
\[
\frac{\operatorname{Var}_0(T_l)}{\mu_*^2}
\le
\frac1{c_*}\left(\frac{2592e}{D}\right)^l
\le \frac1{c_*}4^{-l}. \tag{23}
\]

Chebyshev’s inequality, together with \(\mathbb E_1T_l\ge\mu_*\), proves the theorem for threshold \(\mu_*/2\).

No concentration statement about an unknown empirical color histogram was assumed. The full iid-label randomness, including its shared-vertex covariance, is included in (21). Moreover, if the unconditional planted error is \(\delta_n\), Markov’s inequality gives conditional error at most \(\sqrt{\delta_n}\) for a \(1-\sqrt{\delta_n}\) fraction of iid label assignments.

---

## 6. Concrete implementation and paid costs

A direct exact implementation suffices:

1. Read and store all \(\binom n4=\Theta(n^4)\) input bits.
2. Enumerate pairings of \(4l\) slots; retain loopless connected box graphs.
3. For each retained pairing, enumerate injective assignments of \(2l\) vertex labels.
4. Read the \(l\) corresponding input bits and accumulate their product.

The number of pairing patterns is at most
\[
(4l-1)!!=\exp(O(l\log l)),
\]
and there are at most \(n^{2l}\) injective assignments per pattern. Connectivity checks, indexing, input reads, multiplication, and accumulation are all charged. Thus
\[
T_{\mathrm{classical}}
\le
\bigl(n^4+n^{2l}\exp(O(l\log l))\bigr)
 \operatorname{poly}(B,l,\log n). \tag{24}
\]
Patterns and assignments can be streamed. Storage is
\[
O(n^4)+\operatorname{poly}(B,l,\log n)
\]
bits, rather than an exponentially large meet-in-the-middle table.

For comparison, substituting the native dense input size \(m=\Theta(n^4)\) into an \(m^{l/2}\) MITM cost gives \(n^{2l}\), **not** the source’s \(n^l\) specialization at \(m=\Theta(n^2)\). The construction above also avoids importing XOR overlap corrections that rely on \(b_E^2=1\).

### Exact arithmetic

For even \(l\), no irrational observation arithmetic is required. Accumulate
\[
W_l=\sum_{\text{enumerated configurations}}
       \prod_{E}(4Y_E-1).
\]
Let \(d_l=l!24^l\) and \(N_{\rm conf}=d_lN_l\). Then
\[
W_l=d_l3^{l/2}T_l,
\]
and test (1) becomes
\[
W_l>\frac12N_{\rm conf}\left(\frac{2\epsilon}{9}\right)^l. \tag{25}
\]

The accumulator has \(O(l\log n+l\log l)\) bits. For \(B\)-bit rational \(\epsilon\), denominator clearing makes the comparison exact with polynomial arithmetic overhead. For a certified real-valued specification, relative precision \(O(1/l)\) in \(\epsilon\) suffices after slightly widening the threshold constants; in the target window this requires \(B=O(\log n+\log\log n)\) absolute binary precision. Output is one bit.

There is no label oracle, repeated observation, free input access, or latent-state preparation.

---

## 7. Consequence and remaining scope

For fixed \(C\ge1024\), take
\[
\beta=\frac{C}{n\sqrt{\log n}},
\qquad
l=2\left\lfloor\frac{\log n}{16}\right\rfloor.
\]
Then \(D=\beta^2n^2l\ge2^{15}\) eventually, the errors vanish, and
\[
\log T_{\mathrm{classical}}=O(\log^2 n).
\]
Meanwhile, for the quoted quantum level \(\ell=\Theta(\log^2 n)\),
\[
\log\!\left(n^{\ell/4}\right)=\Theta(\log^3 n).
\]

**Established:** a log-free, same-input classical upper bound, with a fully specified statistic and growing-order proof.

**Not established:** sharp constants, success for every fixed \(C>0\), uniform success for arbitrary adversarial fixed labels, or an extension of this proof to \(l\asymp\log^2 n\). The explicit limitation is the \(16^l/n\)-type shared-vertex bound in (21). Improving that range requires sharper contraction-relative covariance bounds; its failure outside the stated range is not evidence of statistical failure or hardness.

Thus the supplied fixed-level HCE theorem cannot simply be transferred, but **a restricted HCE detector can be proved directly and already supplies the requested stronger classical counter-baseline.**