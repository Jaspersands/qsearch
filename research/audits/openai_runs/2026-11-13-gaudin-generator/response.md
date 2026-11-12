## Result: a general four-site obstruction, not a paid full-path generator

I do **not** obtain a complete paid \(K(g)\). I do obtain an analytic falsifier stronger than an \(N=4\) feasibility test:

> **For every \(N\ge4\), \(2\le M\le N-2\), and distinct real sites, no generator consisting only of at-most-three-site operators can satisfy the joint transport equations throughout any interval \([0,G]\) with \(G>0\).**  
> Genuine double-excitation currents are required already in the coefficient of \(g^2\).

This also rules out **single-exchange currents dressed by arbitrary diagonal occupation functions**, not just one spectator \(Z_c\). It does **not** rule out compact higher-body commutator/intertwiner representations or efficient endpoint preparation by another route.

Everything below is an algebraic deduction. I have not run the parent’s feasibility calculation or evaluated its outcome at \(g=1/3\).

## 1. The first two coefficients are explicitly constructible

Write
\[
d_{ab}=\epsilon_a-\epsilon_b,\qquad
T_{ab}=\sigma_a^+\sigma_b^-+\sigma_a^-\sigma_b^+,
\]
with the question’s convention
\[
C_{ab}=\sigma_a^+\sigma_b^--\sigma_a^-\sigma_b^+.
\]

Near \(g=0\), the joint computational-basis projectors are distinct. Consequently, the continuously transported real joint basis has a unique real antisymmetric generator. Expand it as
\[
K(g)=K_0+gK_1+g^2K_2+O(g^3),
\]
where these are Taylor coefficients, without factorials.

The first two coefficients are
\[
\boxed{
K_0=-\frac12\sum_{a<b}\frac{C_{ab}}{d_{ab}}
}
\]
and
\[
\boxed{
K_1=\frac14\sum_{a<b}\sum_{c\ne a,b}
\frac{1}{d_{ab}}
\left(\frac1{d_{ac}}+\frac1{d_{bc}}\right)Z_cC_{ab}.
}
\]

Thus currents suffice at \(g=0\); adding all spectator currents supplies the next coefficient. These formulas require only native site arithmetic—no target roots, eigenvalues, or spectral denominators.

They do **not** close the expansion.

## 2. Explicit, general higher-body necessity

Let \(a,b,c,d\) be four distinct sites, and let \(R\) be any set of \(M-2\) occupied sites outside that quartet. Denote the corresponding occupation states by
\[
|Rab\rangle=|R\cup\{a,b\}\rangle,\qquad
|Rcd\rangle=|R\cup\{c,d\}\rangle .
\]

The required generator obeys
\[
\boxed{
\langle Rab|K(g)|Rcd\rangle
=
-\frac{3g^2}{4}\,
\frac{\epsilon_a+\epsilon_b-\epsilon_c-\epsilon_d}
{d_{ac}d_{ad}d_{bc}d_{bd}}
+O(g^3).
}
\tag{1}
\]

The coefficient is independent of the occupations in \(R\).

Every at-most-three-site operator has zero matrix element between these states: they differ on four sites. So does every diagonally dressed single-transfer operator. Whenever the numerator in (1) is nonzero, those ansätze cannot be exact.

For **any** four distinct real sites, order them so that
\[
\epsilon_a<\epsilon_b<\epsilon_c<\epsilon_d.
\]
Then the numerator is strictly negative and the denominator is nonzero. A suitable \(R\) exists exactly in the stated range \(2\le M\le N-2\). This establishes the all-input, bulk-sector obstruction—not an extrapolation from a finite example.

An explicit operator carrying the forced matrix element is
\[
J_{ab;cd}
=
\sigma_a^+\sigma_b^+\sigma_c^-\sigma_d^-
-
\sigma_a^-\sigma_b^-\sigma_c^+\sigma_d^+ .
\]
Its coefficient in the double-transfer part of \(K_2\) is the rational expression in (1).

### Derivation using the actual transport equation

Take the native linear combination
\[
\sum_i\epsilon_iQ_i(g)
=
D+gV-\frac g2M(N-M)I,
\]
where
\[
D=\sum_i\epsilon_i n_i,\qquad
V=\frac12\sum_{a<b}T_{ab}.
\]
The scalar term is irrelevant to commutators.

Any solution of the joint equations necessarily satisfies
\[
[D+gV,\;V-[K,D+gV]]=0,
\]
or equivalently
\[
\operatorname{ad}_{D+gV}^{\,2}K=-[D,V].
\tag{2}
\]

First derive on the open dense set of sites where \(D\) has distinct fixed-\(M\) subset sums. Put \(B=[V,K_0]\). Expanding (2) gives
\[
[D,K_0]=-V,\qquad
[D,K_1]=-B_{\rm off},
\]
and
\[
[D,[D,K_2]]
=
-[D,[V,K_1]]-[V,B_{\rm diag}].
\tag{3}
\]
The first two equations yield the displayed \(K_0,K_1\).

For \(x=Rab\), \(y=Rcd\), one has \(V_{xy}=0\), so the last term of (3) contributes zero. Set
\[
\Delta=E_x-E_y=\epsilon_a+\epsilon_b-\epsilon_c-\epsilon_d.
\]
For \(\Delta\ne0\),
\[
(K_2)_{xy}=-\frac{[V,K_1]_{xy}}{\Delta}.
\]

There are exactly four intermediate configurations:
\[
Rac,\quad Rad,\quad Rbc,\quad Rbd.
\]
Substitution of \(K_1\) gives
\[
[V,K_1]_{Rab,Rcd}
=
\frac34
\left(\frac1{d_{ac}}+\frac1{d_{bd}}\right)
\left(\frac1{d_{ad}}+\frac1{d_{bc}}\right)
=
\frac34\frac{\Delta^2}{d_{ac}d_{ad}d_{bc}d_{bd}}.
\]
Contributions from spectators outside the quartet cancel. Equation (1) follows.

There is no residual subset-sum denominator: it cancels.

Finally, these Taylor identities extend to all pairwise-distinct sites, including accidental degeneracies of \(D\). The joint problem at \(g=0\) remains nondegenerate. Explicitly, for distinct occupation states \(x,y\),
\[
[n_j,[K,n_i]]_{xy}
=
-\bigl(n_j(x)-n_j(y)\bigr)
 \bigl(n_i(x)-n_i(y)\bigr)K_{xy}.
\]
This map is injective on real antisymmetric matrices. Hence the unique joint Taylor coefficients vary continuously with the native coefficients; the identities derived on the dense set extend across scalar subset-sum coincidences.

The local existence/uniqueness argument is a proof device, **not** an exponentially sized construction being counted as an algorithm.

## 3. Exact diagnostic for the parent fixture

For
\[
N=4,\quad M=2,\quad
(\epsilon_1,\epsilon_2,\epsilon_3,\epsilon_4)=(0,1,3,7),
\]
equation (1) gives
\[
\boxed{
[g^2]\,\langle12|K(g)|34\rangle
=
-\frac34\frac{-9}{(-3)(-7)(-2)(-6)}
=
\frac3{112}.
}
\]

Two further complementary-pair checks, with the same occupation convention, are
\[
[g^2]K_{13,24}=-\frac{15}{224},
\qquad
[g^2]K_{14,23}=-\frac1{32}.
\]

Structurally, in this six-dimensional sector:

* currents plus spectator currents span the 12 antisymmetric single-transfer edges;
* the full antisymmetric space has dimension 15;
* the three missing directions connect complementary occupation pairs.

The required generator enters those missing directions at order \(g^2\).

**Interpretation of the pending control:** this disproves an exact three-site generator on the entire path \(0\le g\le1/3\). It does **not**, by itself, determine feasibility at the isolated point \(g=1/3\). No such endpoint result is asserted here.

## 4. What is paid, and what remains unpaid

Let
\[
\delta=\min_{a\ne b}|\epsilon_a-\epsilon_b|>0.
\]

The displayed coefficients are inexpensive to construct:

| Displayed part | Number of terms | Bound per coefficient |
|---|---:|---:|
| \(K_0\) | \(O(N^2)\) | \(1/(2\delta)\) |
| \(K_1\) | \(O(N^3)\) | \(1/(2\delta^2)\) |
| Forced double-transfer part of \(K_2\) | \(O(N^4)\) | \(3/(2\delta^3)\) |

For the last bound, use
\[
\frac{\Delta}{d_{ac}d_{ad}d_{bc}d_{bd}}
=
\frac1{d_{ad}d_{bc}d_{bd}}
+
\frac1{d_{ac}d_{ad}d_{bc}}.
\]

Reading the explicit rational input and branch label costs at least their written size. Enumerating these coefficients takes \(O(N^4)\) rational operations with polynomial bitlength; evaluating them to \(p\) bits likewise has polynomial cost in native bitlength, \(N\), and \(p\). Each displayed operator has a constant-size Pauli expansion.

For example, the trial generator \(K_0+gK_1\) has the paid simulation normalization bound
\[
\int_0^G
\|i(K_0+gK_1)\|_{\mathrm{Pauli},1}\,dg
=
O\!\left(
\frac{GN^2}{\delta}
+
\frac{G^2N^3}{\delta^2}
\right).
\]
Its coefficient evaluation, variation, and ordinary product-formula implementation can therefore be paid under the native conditioning contract.

**But this pays implementation of the trial generator, not its correctness.** No bound has been established here on
\[
\int_0^G
\left\|K(g)-\sum_{r=0}^{r_{\max}}g^rK_r\right\|\,dg.
\]
Nor has the complete \(K_2\), a closed hierarchy, or a controlled resummation been supplied.

The obstruction is therefore **algebraic closure at three sites**, not prohibitive cost at fourth order. Adding the forced \(O(N^4)\) terms is itself polynomial.

## 5. Admission tests for a successor mechanism

A higher-body commutator or rational-intertwiner proposal remains viable, but must meet these concrete tests:

1. **Actual transport identity.** Verify all joint equations, or prove that a paid orthogonal \(U(g)\) makes every \(U(g)^TQ_i(g)U(g)\) diagonal in the initial bit basis. Its \(K=U'U^T\) must reproduce (1). Flatness alone is insufficient.

2. **Evaluation and simulation access.** Supply polynomial-cost coefficient evaluation or a block encoding, including its normalization, precision, and control variation. A short formal inverse or nonunitary intertwiner does not pay inversion, normalization, or success probability.

3. **Truncation or target-branch error.** For an approximation \(\widetilde K\), a sufficient direct certificate is
   \[
   \int_0^G
   \|(\partial_g-\widetilde K(g))|\psi_b(g)\rangle\|\,dg
   \le \epsilon_{\rm path},
   \]
   in a fixed phase gauge, with a bound computable from native input rather than target-state advice. Duhamel’s formula then controls state-vector—and hence trace-distance—error. Finite coefficient matching is not such a certificate.

4. **End-to-end costs.** Charge reading the input, \(O(N)\) preparation of \(|b\rangle\), coefficient rounding, time discretization, simulation error, and delivery of the \(N\)-qubit output state. No state-preparation algorithm is claimed by the present calculation.

### Cheapest disproof

For any proposed complete current/spectator closure, ask for the single coefficient
\[
[g^2]\langle12|K(g)|34\rangle.
\]
That ansatz necessarily returns zero; native transport requires \(3/112\).

This is a concrete mechanism-specific falsifier. It establishes neither exponential representation size nor hardness, and does not exclude low-body gates synthesizing higher-body effective transport or a different preparation path.