# Independent review: separated heat scales in a native conductivity moment

Date: 2026-11-12. Local mathematical review; no numerical sweep, Git,
network, or API action. Input convention is the one in
`PERIODIC_CONDUCTIVITY_NATIVE_ADMISSION.md`. The proposed counterfamily is
valid. The proof below controls the **absolute value** of the restricted
sum, without assuming that this sum is positive.

**Disposition.** For every sequence of nonnegative integer widths
`w=w(n)=o(n)`, the explicit circuit family below satisfies

\[
 T_2\longrightarrow\frac14,
 \qquad |T_2^{(w)}|
 =O\left(\frac{n2^w}{2^n}+\frac{n}{2^{n/2}}\right)
 \longrightarrow0.
\]

Here `T_2^(w)` retains exactly the triples of heat-band indices whose
maximum minus minimum is at most `w`. This refutes a uniform approximation
of the individual Neumann moments by this restriction. It does not refute
arbitrary correlated estimators, establish classical hardness, or by
itself rule out cancellations in a different approximation to the complete
conductivity series.

## 1. Operators and the explicit input

Let `L=2^n`, `n>=2`, and `N=L^2`. Use the ordinary counting inner product
on the two directed-edge components of the two-dimensional periodic grid.
Let `D` be the forward gradient, `K_0=D*D`, and
`Pi=D K_0^+ D*`. Write `K_e` for the componentwise scalar grid Laplacian
on edge fields. It commutes with `Pi`, has spectrum in `[0,8]`, and its
smallest positive eigenvalue is

\[
 \lambda_* =4\sin^2(\pi/L)\ge 16/L^2.
\]

Put

\[
 h(x)={\bf1}_{x<L/2},\quad
 \sigma(x,y)=h(x)(-1)^x+(1-h(x))(-1)^y,
 \quad \eta=e_1/L.
\]

Let `S` multiply both edge components by the same `sigma`. Thus
`S=S*=S^{-1}`. This is an allowed, uniformly succinct sign circuit:
one coordinate's high bit chooses which coordinate's parity bit is used.
For any fixed contrast, `c(I+zS)` gives the admitted two-valued positive
conductivity input.

Set

\[
 v=S\eta=v_A+v_B,
 \quad v_A=h(x)(-1)^x e_1/L,
 \quad v_B=(1-h(x))(-1)^y e_1/L.
\]

Both summands have squared norm `1/2`. Because `L/2` is even, `v_A` has
zero mean in `x`; a direction-1 field depending only on `x` with zero
mean is a periodic gradient. Consequently `Pi v_A=v_A`.

All Fourier modes of `v_B` have `k_y=L/2`, hence scalar Laplacian
eigenvalue `lambda_x+4`. The gradient projection's `(1,1)` symbol is
`lambda_x/(lambda_x+4)`. For `g(x)=1-h(x)`, one-dimensional Parseval gives

\[
 \|\Pi v_B\|^2
 =\frac1L\sum_{k_x}|\widehat g(k_x)|^2
       \frac{\lambda_x}{\lambda_x+4}
 \le\frac{\|D_xg\|^2}{4L}
 =\frac1{2L}.
\]

There are exactly two jumps of `g`. Let `q=S v_A=h e_1/L` and
`r=Pi q=(h-1/2)e_1/L`. Then `||r||=1/2` and

\[
 u=\Pi S\Pi v=r+\Pi S\Pi v_B,
 \qquad \|u-r\|\le(2L)^{-1/2}.
\]

The SERIES convention gives
`T_2=<v,Pi S Pi S Pi v>=||u||^2`. Therefore

\[
 \left|T_2-\frac14\right|
 \le\frac1{\sqrt{2L}}+\frac1{2L}.
 \tag{1}
\]

## 2. Outer heat bands concentrate at the eigenvalue 4

Define

\[
 A_{-1}=\int_0^1D e^{-tK_0}D^*\,dt,
 \qquad A_i=\int_{2^i}^{2^{i+1}}D e^{-tK_0}D^*\,dt\quad(i\ge0).
\]

Equivalently `A_i=Pi a_i(K_e)`, where
`a_-1(lambda)=1-exp(-lambda)` and
`a_i(lambda)=exp(-2^i lambda)-exp(-2^(i+1) lambda)` for `i>=0`.
The `A_i` are positive, commute, and sum to `Pi`. Put `c_i=a_i(4)`;
then `c_i>=0` and `sum_i c_i=1`.

For `f=h(-1)^x`, the identity
`(K_x-4)f=-(-1)^x K_xh` has four nonzero boundary entries, each of
absolute value one. Including the edge normalization gives

\[
 \|(K_e-4)v_A\|=2/\sqrt L,
 \qquad \|{\bf1}_{[0,2)}(K_e)v_A\|\le1/\sqrt L.
 \tag{2}
\]

Every `a_i` takes values in `[0,1]`. On `[2,8]` it is Lipschitz with
constant at most one, uniformly in `i`: this is immediate for `i=-1`;
for `i>=0`, writing `t=2^i>=1`,

\[
 |a_i'(\lambda)|\le t e^{-2t}+2t e^{-4t}
 \le e^{-2}+2e^{-4}<1.
\]

Split (2) into the parts below and above `2`. The low part uses
`|a_i(lambda)-c_i|<=1`, and the high part uses the Lipschitz bound. Thus

\[
 \|A_i v_A-c_i v_A\|\le3/\sqrt L,
 \qquad \|A_i v_B\|\le\|\Pi v_B\|\le1/\sqrt{2L}.
 \tag{3}
\]

Write `A_i v=c_i v_A+e_i`, and put `E=sum_i ||e_i||`. To justify an
actual summable bound, rather than multiplying (3) by infinitely many
bands, take `J=3n`. The first `J+2` bands contribute at most
`4(J+2)/sqrt L`. For the remaining bands,

\[
 \sum_{i>J}\|A_i v\|
 \le\sum_{i>J}e^{-\lambda_*2^i}
 \le2e^{-32L},
 \qquad
 \sum_{i>J}c_i=e^{-4\,2^{J+1}}.
\]

The first inequality uses `||Pi v||<=1`; the second uses
`lambda_* 2^(J+1)>=32L` and `2^s>=s+1`. Therefore

\[
 E\le E_n:=\frac{4(3n+2)}{\sqrt L}+3e^{-32L}
 =O(n/\sqrt L).
 \tag{4}
\]

All series manipulations below are legitimate: for each finite `L`,
the band operator norms have an exponentially decaying tail. In
particular, the unrestricted triple expansion is absolutely convergent.

## 3. The restricted operator sum and its error

Define the restriction precisely by

\[
 T_2^{(w)}=
 \sum_{\substack{i,j,k\ge-1\\
          \max(i,j,k)-\min(i,j,k)\le w}}
 \langle A_i v,S A_j S A_k v\rangle.
\]

For each outer pair, let

\[
 M_{ik}=\sum_{\substack{j\ge-1\\
          \max(i,j,k)-\min(i,j,k)\le w}} A_j.
\]

If `|i-k|>w`, this is zero; otherwise it is the sum over the interval
`max(i,k)-w <= j <= min(i,k)+w`, intersected with `j>=-1`.
In all cases `0<=M_ik<=Pi<=I`, and `M_ik=M_ki`.
This makes `T_2^(w)` real, but positivity of the complete restricted
quadratic form is not needed or asserted.

After replacing the outer bands by `c_i v_A`, the resulting expression is

\[
 F_w=\sum_{i,k}c_i c_k\langle q,M_{ik}q\rangle\ge0.
\]

Using `||S||=||M_ik||<=1`, summing absolute errors over all outer pairs,
and using `sum c_i=1`, gives the width-independent estimate

\[
 |T_2^{(w)}-F_w|
 \le2\|v_A\| E+E^2=\sqrt2 E+E^2.
 \tag{5}
\]

There is no uncharged count of admissible middle or outer bands in (5).
The full allowed middle sum is a contraction before errors are bounded.

## 4. The remaining scalar sum vanishes

Let `a=ceil(log_2 n)` and `T=2^(a+w+1)`. If both outer indices are at
most `a`, every allowed middle index is at most `a+w`. Consequently

\[
 M_{ik}\le\sum_{j=-1}^{a+w} A_j
 =\Pi(1-e^{-T K_e}).
\]

The total coefficient weight of pairs with at least one outer index
above `a` is at most `2 tau`, where
`tau=sum_(i>a)c_i=exp(-4*2^(a+1))`. Each scalar quadratic form is at
most `||q||^2=1/2`. Hence

\[
 F_w\le\langle q,\Pi(1-e^{-T K_e})q\rangle+\tau
 \le T\langle q,K_e q\rangle+\tau
 =\frac{2T}{L}+\tau
 \le\frac{8n2^w}{L}+e^{-8n}.
 \tag{6}
\]

The second inequality uses commutation, `0<=Pi<=I`, and
`1-exp(-T lambda)<=T lambda`. The energy `2/L` again counts the two
vertical interfaces, with `L` edges at each interface and amplitude
`1/L`. Combining (4)--(6) supplies the fully explicit bound

\[
 |T_2^{(w)}|
 \le\frac{8n2^w}{L}+e^{-8n}+\sqrt2 E_n+E_n^2.
 \tag{7}
\]

Since `n/sqrt(2^n)` is bounded, this implies the asymptotic bound stated
at the start. In particular, for every `w=o(n)`, (1) and (7) give
`T_2-T_2^(w) -> 1/4`.

## Scope and next gate

The mechanism is explicit: the two outer projections see essentially
the microscopic eigenvalue `4`; multiplication by the sign field turns
that part into the macroscopic half-grid step `h`, whose projection
requires much longer heat times. A single narrow scale window cannot
capture this three-projection interaction.

A prospective correlated classical algorithm must therefore pay or
represent widely separated scales; it cannot justify the omission of
all such triples by a uniform small-error bound on `T_2`. The result
places no lower bound on the cost of representing those interactions.
General polynomial-work correlated estimators, analytic resummations,
and other native classical algorithms remain open at the existing scope.
