## Strongest result

**The repaired algebraic composition is consistent, conditionally: I find no remaining dimension, Tate-twist, or arithmetic-Frobenius contradiction. In particular, the actual subgroup \(U=\operatorname{ev}_{s_0}\operatorname{Hom}_\Gamma(S,J_{\mathrm{full}}[\ell])\), quotient-first reconstruction, and direct boundary division fit together.**

**The unconditional native \(\operatorname{poly}(\log p)\) theorem nevertheless remains OPEN on this packet.** The decisive proof gate is an **effective, uniform reconstruction-height bound**, including its particular cover-compatible-model and analytic inputs. The supplied height note gives a substantive assembly, but imports essential estimates from material not supplied here. Its “independently checked” labels do not establish those estimates. A bound stated as “polynomial” without an effective bound available to the reconstruction algorithm does not yet supply its certified precision.

There is also a concrete, repairable parameter interface: the numerical lift described with \(D_0=(2g+1)O\) cannot simply be reused after changing to \(D_0=A+gb\). Fresh RR spaces, evaluation data, and a correctly re-expressed point are required. Below I give a sufficient construction, including the claimed canonical-extraction step, rather than treating the Algorithm 7 citation as a proof.

These are **OPEN proof obligations, not counterexamples to the existence of the proposed algorithm**. Absence of a fatal counterexample is not an admission.

---

## 1. Parameter ledger: the fixed quantities and the growing quantities

The following distinctions are essential.

| Object | Correct parameter |
|---|---:|
| Original smooth pencil fibre | genus \(g_0=31\) |
| Natural representation | \(n=2g_0=62\) |
| Geometric singular fibres | \(r=220\) |
| Open multiplicity space \(W\), and subgroup \(U\) | \(m=(r-2)n=13516\) |
| Whole natural socle \(E\) | \(nm=837992\) |
| Connected frame component degree | \(D=|\operatorname{Sp}_{62}(\mathbf F_\ell)|\) |
| Full frame degree | \(d=(\ell-1)D=|\Gamma|\) |
| Connected frame component genus | \(g=g(C_0)\), growing with \(\ell\) |
| Number of points of \(U\) | \(\ell^m\), not \(m\) |
| Rank of reconstructed \(\mathbf Q[B_a\times U]\) | \(d\ell^m\) |
| Rank of descended \(\mathbf Q[U]\) | \(\ell^m\) |

For \(n=62\),
\[
D=\ell^{31^2}\prod_{i=1}^{31}(\ell^{2i}-1),
\qquad d<\ell^{1954}.
\]
Riemann–Hurwitz gives
\[
2g-2=D\left(-2+220\left(1-\frac1\ell\right)\right).
\]
Thus \(g=O(D)\), with a fixed constant. All RR, Wronskian, evaluation-count, and lifting bounds must use this \(g\), **not 31**.

The apparent enormous enumerations are not, by themselves, a complexity contradiction. Since \(m,n,r\) are fixed, \(\ell^m\), \(d\ell^m\), and fixed powers of these quantities are polynomial in numerical \(\ell\). This argument would cease to establish polynomial complexity if the surface degree, \(n\), or \(r\) grew with the input.

Two particularly important non-implications are:

* \(p>|\Gamma|\) does **not** imply \(p>\ell^m\), the rank of \(\mathbf Q[U]\).
* A polynomial field degree does **not** by itself imply polynomial coordinate bit lengths.

The proposed maximal-order procedure addresses the first. The second must be addressed by explicit presentations and height bounds, not by field-degree statements alone.

---

## 2. Native geometry and monodromy

### Geometry and dimensions

The numerical geometry checks.

For a \((5,3)\) complete-intersection curve,
\[
2g_0-2=(5+3-4)\cdot 15=60,
\]
so \(g_0=31\). Two cubic divisors on the quintic meet in
\[
(3H)^2=9H^2=45
\]
basepoints. The surface Euler characteristic is \(55\); after blowing up those points it is \(100\). Consequently,
\[
100=2(2-62)+r
\]
gives \(r=220\).

The irreducibility argument also works in the stated one-node setting. A reducible connected fibre with only one ordinary node would have a decomposition
\[
A+B=3H,\qquad A\cdot B=1.
\]
Choosing \(a=H\cdot A\le7\) gives
\[
A^2=3a-1,\qquad A^2\le a^2/5,
\]
which is impossible for \(1\le a\le7\).

The native pencil search therefore has the right target geometry. Its complexity still requires a uniform bounded-degree description of the bad parameter locus and exact nodality/transversality tests. Fixed degree and a fixed number of variables make such elimination bounds appropriate; no growing-dimensional elimination is being licensed here.

### Mod-\(\ell\) monodromy

Rational Zariski density is insufficient. The needed argument is stronger:

1. Over \(\mathbf C\), the blown-up quintic has \(H_1=0\).
2. A Lefschetz fibration with a geometric section presents the fibre’s first homology modulo its vanishing cycles as the total space’s first homology. Here geometric sections exist from the blown-up basepoints.
3. Thus the vanishing cycles span **integrally**, and hence modulo every \(\ell\).
4. The cycles are conjugate under the pencil monodromy.
5. The irreducibility argument using the symplectic pairing and Picard–Lefschetz transvections then applies.
6. The transvection theorem must be used with its actual hypotheses, including generation by the relevant transvections—not merely “contains a transvection and is rationally dense.”

This gives the necessary route to a uniform full-\(\operatorname{Sp}\) statement for this family. It avoids relying on a broad assertion that torsion-free integral cohomology automatically makes every hard-Lefschetz map invertible modulo every prime.

The supplied geometry excerpt supports the transvection/conjugacy route. The integral spanning step is indispensable: otherwise an input-dependent exceptional \(\ell\) could invalidate both the dimension \(m\) and the CRT supply of primes.

For transfer to the target characteristic, \(p>|\Gamma|\) is a sufficient safe prime-to-\(p\) regime, provided the verified pencil gives a smooth pair with finite-étale branch divisor over \(\mathbf Z_p\). Failure of that numerical regime can be handled by the stated direct-count branch. It must not be replaced by an uncharged promise about \(p\).

---

## 3. Native cover, auxiliary prime, and complete module

### Cover construction

The cover construction has the correct interface **if its stated algorithmic contracts hold**:

* the original Jacobian atlas is genuinely the Jacobian, with radical ideals and complete addition charts;
* the ordered torsion basis is evaluated in that actual Jacobian;
* an actual Weil pairing fixes the normalization;
* the full frame retains the cyclotomic coordinate and its right \(\Gamma\)-action.

These requirements are substantive. An abstract cover with the same geometric group, or an alternating form known only up to an unlinked scalar, would not supply the arithmetic coefficient system needed downstream.

The supplied native-atlas derivation addresses the previously missing rational-point input using closed fibres and fixed-format constructions. Its fixed genus is important: this does not authorize fixed-variable elimination on the growing-genus auxiliary Jacobian.

The height theorem must subsequently be applied **componentwise** to the geometrically connected \(\operatorname{Sp}\)-cover. The full \(\Gamma\)-cover has \(\ell-1\) geometric components and is not a geometrically connected curve to which that theorem can simply be applied unchanged. Using \(d\) as a larger numerical bound is harmless; confusing the connected genus or RR problem is not.

### Auxiliary prime

The small-prime argument is valid in principle:

* an explicit integer \(M\) of polynomial bit length has at most \(O(\log |M|)\) distinct prime divisors;
* a polynomial numerical threshold and polynomially many excluded primes permit a polynomial-size prime search;
* testing divisibility does not require factoring \(M\).

But the construction order must be explicit. It is circular to select \(P\) using an \(M\) that already contains witnesses depending on a later \(P\)-dependent choice of \(a,b\), or canonical divisor.

A sufficient organization is:

1. Construct \(M_0\) for the fixed cover, normalization, deck maps, and fixed coordinate data.
2. Choose \(P\) avoiding \(M_0\ell|\Gamma|p\), above all predetermined degree and bad-parameter bounds.
3. Choose \(a,b\) and certify the new residue ranks and unit pivots directly.
4. Use fixed-rank/base-change arguments to justify those new integral RR computations.

This avoids requiring every later witness to have been included in an earlier integer.

In particular, choose \(P>2g-1\) when invoking the stated ordinary-Wronskian avoidance argument. The relevant genus is the growing cover genus.

### Complete module, not an observed subgroup

The module extraction has the right safeguards:

* compute the smooth-model zeta numerator at the **small numerical characteristic \(P\)**;
* include every irreducible Frobenius factor of degree at most \(m\), with full primary multiplicity;
* use
  \[
  H=\ell^{\lceil\log_\ell\max(1,2g)\rceil}
       \prod_{j=1}^{m}(\ell^j-1);
  \]
* certify the whole selected primary space by a Weil-pairing rank test.

The factor involving \(2g\), rather than \(m\), pays for ambient nilpotent blocks. The product over \(j\le m\) pays for the semisimple orders. Its numerical value is polynomial in \(\ell,g\) only because \(m\) is fixed.

The algorithm must retain the distinction between:

* computing generators and linear coordinates in a space of dimension at most \(2g\); and
* enumerating all points of that space.

The former is polynomial here. Enumerating ambient torsion would not be justified. Only the fixed-rank \(U\) is subsequently enumerated.

The auxiliary field is also charged correctly only if its representation has bit size proportional to its degree times \(\log P\), and extension zeta coefficients are charged at their actual \(O(g\,bH\log q)\) sizes. Treating these as unit-cost field operations would not prove the requested bit bound.

### Why the new \(U\) is the right object

The repair
\[
U=\operatorname{ev}_{s_0}\operatorname{Hom}_\Gamma(S,J_{\mathrm{full}}[\ell])
\]
is sound.

If \(\phi(s_0)=0\) for nonzero \(s_0\), the kernel of the intertwiner \(\phi\) is a nonzero \(\Gamma\)-submodule of the simple natural dual \(S\). Hence \(\phi=0\). Evaluation is therefore injective.

Because \(S,s_0\), and the full right deck action are constant, evaluation is Galois-equivariant. Thus \(U\) is an actual Galois-stable subgroup of rank \(m\), and its arithmetic Frobenius is the action on \(W\).

No \(\Gamma\)-stability of \(U\) follows or is needed. In particular:

* do not descend deck maps as endomorphisms of \(U\);
* do not concatenate \(\ell-1\) independent multiplicity spaces;
* do not perform a final natural-isotypic extraction after reconstructing \(U\).

The component formula supplied in the packet is consistent with the stated right-pushforward convention and constructs the full intertwiner from the one-component Hom space.

---

## 4. Canonical numerical extraction: a usable construction

This is the most important repairable interface mismatch.

The numerical-lift note starts with \(D_0=(2g+1)O\). The proposed canonical extraction uses
\[
D_0=A+gb.
\]
These are different KM models. Merely changing the symbol does not transport either the point representation or its evaluation coordinates.

For example, if \(A\) has degree at least \(3g-1\), then the new \(D_0\) has degree at least \(4g-1\). An old evaluation set sized just above \(5(2g+1)\) need not even inject the new \(L(4D_0)\). This is a genuine dimensional failure of literal reuse, not a height issue.

### Sufficient reinitialization

Work on one connected component. Choose \(A\), before choosing the canonical divisors, as a sufficiently large known pole divisor, with:

* support avoided by every canonical divisor;
* \(\deg A=a\ge3g+2\);
* the plane coordinates \(x,y\) contained in \(L(A)\).

After making the plane generator integral over the base affine line, a sufficiently large multiple of the pole divisor of the base map is a suitable choice.

For each chosen \(b\):

1. Construct exact generic RR spaces for \(A+gb\) and the required bounded multiples.
2. Choose fresh integral evaluation data large enough for this new degree.
3. Re-express the residue class \(x=-t\) in this KM model using the supplied closed divisor class.
4. Lift in this model, rather than silently reinterpreting an old KM matrix.

The two-chart normalization data provide a route to the new RR systems: multiply by powers of \(x-a\), bound coefficient degrees using the Laurent transitions, and impose the closed fibre-idempotent constraints at the other points above \(a\). The required constant field for these exact RR spaces is the explicit basepoint field, not the unknown global torsion field.

### Derivation of the Algorithm 7 prefix

Let \(D\) be the effective degree-\(d_0\) divisor representing \(x=-t\), where
\[
D_0=A+gb,\qquad d_0=a+g,\qquad [D-D_0]=-t.
\]
The input KM space is
\[
W_D=L(2D_0-D).
\]

Compute
\[
W_1=W_D\cap L(2D_0-A)
    =L(2D_0-D-A).
\]
This line bundle has degree \(g\) and class \(t+gb\). The residue condition \(h^0(t+gb)=1\) therefore makes \(W_1\) a line, with \(H^1=0\). A primitive generator \(u\) satisfies
\[
\operatorname{div}(u)=D+A+D_t-2D_0.
\]

Now compute, using all linear constraints,
\[
W_+=\{h\in L(2D_0):hW_D\subset uL(2D_0)\}.
\]
Since \(2D_0-D\) has degree \(d_0\ge2g+1\), its line bundle is globally generated. The containment is therefore equivalent to the divisor inequality defining
\[
W_+=L(D-\operatorname{div}(u))
    =L(2D_0-A-D_t)
    =L(A+2gb-D_t).
\]

This supplies the required prefix independently of an uninspected line-number citation.

### The second colon is correct

Because \(\mathcal O(2gb)\) is globally generated,
\[
L(A-D_t)
=
\{f\in L(A):fL(2gb)\subset L(A+2gb-D_t)\}.
\]
Global generation is exactly what prevents an unwanted common zero from weakening the vanishing conditions at \(D_t\).

With \(V=L(A)\) and \(W=L(A-D_t)\), the degree choice gives \(H^1(A-D_t)=0\). Since \(A\) avoids \(D_t\), restriction yields
\[
V/W\simeq H^0(D_t,\mathcal O_{D_t}),
\qquad \dim(V/W)=g.
\]

Multiplication can be computed using \(L(2A)/L(2A-D_t)\), whose restriction is the same length-\(g\) algebra. The latter kernel can be obtained by the same containment method. Thus multiplication by \(x,y\), the characteristic polynomial of \(z=x+cy\), and the closed \(A_t,B_t,C_t\) encoding are obtainable by RR and linear algebra.

This construction handles nonsplit and nonreduced support. It needs no support splitting and no inverse-Abel oracle.

For precision preservation, generic equalities alone are insufficient. The implementation must verify the relevant residue ranks, choose unit pivots, and use the known flat ranks. Those are the conditions that make the argument valid over the truncated local ring without losing \(P\)-adic digits.

**Disposition:** the colon repair is mathematically sound. Fresh KM initialization and its integral RR output must be made explicit, but the supplied normalization interface provides a polynomial route.

---

## 5. Global encoding, descent, and the unresolved precision theorem

### A globally equivariant encoding exists

There is a clean way to avoid accidentally treating \(U\) as \(\Gamma\)-stable.

For \((b,t)\in B_a\times U\), retain \(b\), its cyclotomic component coordinate, and, for every fixed deck index \(g\in\Gamma\), the canonical divisor representing
\[
t_{\operatorname{component}(bg)}+g_C(bg),
\]
where \(g_C\) is the connected cover genus and \(t_j\) is the actual component of the already constructed full tuple \(t\).

Here the class is the appropriate component of \(t\), **not an asserted deck translate inside \(U\)**.

This encoding is:

* Galois-equivariant, because Galois commutes with the constant deck maps;
* closed over the class/basepoint field, by uniqueness;
* injective, because \(b\) is retained and the component divisor classes recover the full tuple \(t\).

The number of required canonical divisors is bounded by a fixed polynomial in \(d,\ell^m,g\). Every avoidance and separator count must include these redundant entries, not merely \(\ell^m\).

The splitting-field bound
\[
[B_a,U:\mathbf Q]\le d\,|\operatorname{GL}_m(\mathbf F_\ell)|
\]
is then legitimate. It does not justify splitting every divisor support, and no such splitting is needed.

### Rational algebra and equalizer

Choose separating coefficients in \(\mathbf F_P\), lifted to integers—not arbitrary coefficients in the larger working residue field. A bounded integer grid suffices once \(P\) exceeds the bad-pair count.

If the resulting values are \(\gamma_s\), then
\[
F(Z)=\prod_{s\in B_a\times U}(Z-\gamma_s)
\]
has rational coefficients by global Galois equivariance. Distinct residues make it separable and make the local interpolation denominators units.

The relation
\[
r(s,t)=1\quad\Longleftrightarrow\quad
\text{the two points have the same }U\text{-label}
\]
is also globally invariant. Local labels suffice because prime-to-\(P\) torsion lifting preserves equality and group operations, and the complete residue module lifts to the complete intrinsic module.

Over \(\overline{\mathbf Q}\), the equalizer
\[
C=\ker\!\left[f\mapsto r(f\otimes1-1\otimes f)\right]
\]
consists exactly of functions constant on each \(B_a\)-fibre. Hence
\[
C\simeq\mathbf Q[U],\qquad \dim_{\mathbf Q}C=\ell^m.
\]

Addition descends without choosing a rational basepoint: on the larger set use
\[
((b,t),(b',t'))\longmapsto(b,t+t'),
\]
then restrict its pullback to \(C\). Inversion and scalars are similar; the zero label gives the identity idempotent. No deck action on \(U\) is required.

These arguments close the global-descent interface, conditional on certified reconstruction of the rational coefficients.

### What precision actually requires

Let \(N_S=d\ell^m\), and suppose every encoding coordinate has an effective logarithmic height bound \(H\). Standard product and interpolation estimates give
\[
H_{\mathrm{rat}}\le
\operatorname{poly}(N_S)\bigl(H+\log N_S+1\bigr)
\]
for rational coefficients of the product polynomial and fixed-arity operation tables.

Consequently one may take an explicit numerator/denominator bound \(T\), and choose
\[
P^e>2T^2.
\]
The local arithmetic then has bit size polynomial in
\[
N_S,\quad [K_P:\mathbf Q_P],\quad e\log P,
\]
not merely in the number of field operations.

This does **not** require constructing a global splitting-field basis. The basepoint field has an explicit bounded presentation; torsion computations remain in the paid local field; rational coefficient heights control reconstruction directly.

### The decisive OPEN gate

The supplied height assembly depends on estimates including
\[
h_Z(b)\le C_r d^3S,\qquad
\Delta_{\mathrm{st}}\le C_r d^6(d+1+h_B),
\]
the stated theta and Faltings bounds, and the global Green-function lower bound with controlled \(\Lambda'\). The estimate for \(h_Z(b)\) must concern the **specific nonminimal cover-compatible model** used in the vertical-pole argument.

The packet explains why these estimates would imply the support bound and why intrinsic theta height alone is insufficient. It does not supply the derivations or effective constants for all those imported estimates. The referenced uniform-height material is not included.

Therefore:

* the finite/archimedean assembly is meaningful conditional evidence;
* the displayed support-height theorem is sufficient **as an assumption**;
* the packet does not yet independently establish the effective theorem needed to output certified \(e\).

The native branch-height input itself is not missing: it can be bounded from the fixed-format branch polynomial. The missing proof is the uniform arithmetic/analytic transfer from that input to the required canonical-coordinate bound.

Choose the quotient-first version with a small integer \(a\) if possible. If instead using \(a=a_0+pk\), retain \(\log(1+|a|)\) in every applicable bound. One cannot use the small-\(a\) formula unchanged.

---

## 6. Original-prime Frobenius: the quotient-first repair works

### Unramifiedness

The genuine intrinsic frame is finite étale over the smooth pencil locus over \(\mathbf Z_p\). After splitting the finite-étale branch divisor by an unramified extension, the local Kummer pullback kills the order-\(\ell\) inertia. Purity then gives the stated smooth local normalization.

This establishes good reduction of the compactified frame cover under the stated tame hypotheses. Its prime-to-\(p\) Jacobian torsion is unramified. Since \(U\) is an actual Galois-stable subgroup, \(U\) is unramified.

The argument would fail for an arbitrary ramified constant twist. The actual evaluation frame is therefore essential, not cosmetic.

Only \(C=\mathbf Q[U]\) needs this property. The larger algebra involving \(B_a\) can be ramified at \(p\). Thus descending first genuinely removes the need for target-regular \(B_a\).

### Known-prime maximalization

The specified order procedure does not require \(p>\operatorname{rank}C\). This matters because \(p>|\Gamma|\) is weaker.

There is a short correctness argument in the unramified case. Let \(A\) be the maximal local order and \(O\subset A\) the current order. Since \(A/pA\) is reduced, the radical preimage is
\[
I=O\cap pA.
\]
If \(O\ne A\), take the smallest \(k\ge1\) with \(p^kA\subset O\). Some
\(x\in p^{k-1}A\setminus O\) then satisfies
\[
xI\subset p^kA\subset O,\qquad xI\subset pA,
\]
so \(xI\subset I\). Hence \((I:I)\) strictly enlarges \(O\). A fixed point is therefore maximal at \(p\).

The discriminant-index identity bounds the number of strict enlargements. Original-order lattice coordinates are needed to bound intermediate bit lengths. No integer factorization follows from or is required by this argument.

The resulting unit discriminant at \(p\) is an exact consistency check. Direct reduction of the original numerical coordinates remains invalid; the supplied \(T(T-p)\) example correctly demonstrates that distinction.

### Arithmetic action

On the finite-étale reduction, \(a\mapsto a^p\) acts on geometric points by raising values to their \(p\)-th powers. This is **arithmetic Frobenius**.

For the determinant endpoint, an explicit point splitting field is optional. Using the descended group law and identity idempotent, one can compute the rank of the finite-étale kernel scheme of \(u(F)\). Its rank is
\[
\ell^{\dim_{\mathbf F_\ell}\ker u(F)}.
\]
Taking sufficiently high powers of irreducible \(u\) recovers primary multiplicities, including nonsemisimple blocks. All irreducibles of degree at most fixed \(m\) can be handled at polynomial numerical-\(\ell\) cost.

Thus the target-prime stage need neither invert Frobenius nor reconstruct a final Hom space.

---

## 7. Boundary division and the degree-53 output

The determinant calculation is internally consistent.

For the untwisted nearby-fibre module \(M\),
\[
H^1(I,M)=M_I(-1)
       \simeq(M^I)^\vee(-2).
\]
If \(F_{\mathrm{node}}\) denotes geometric Frobenius on nodal-fibre \(H^1\), the geometric open boundary is consequently
\[
q_z^2F_{\mathrm{node}}^{-T}.
\]

But the reconstructed module is arithmetic
\[
W=H^1(U,L')(2).
\]
On this boundary its arithmetic action is \(F_{\mathrm{node}}^T\). Therefore the direct factor is exactly
\[
B_{W,z}(T)
=(1-\epsilon_zT^{f_z})P_{\mathrm{norm},z}(T^{f_z}),
\]
with no additional \(p\)-scaling.

The boundary degree is
\[
220(1+60)=13420.
\]
Thus
\[
13516-13420=96.
\]

Parabolic duality identifies arithmetic action on the twist by \(2\) with the transpose-dual form of geometric action, giving equality of characteristic polynomials without semisimplicity. The supplied quotient is therefore the geometric parabolic polynomial.

The normalization interface has the right bounded parameters:

* unique node rational over the closed branch field;
* normalization genus \(30\);
* closed branch degree at most \(220\);
* blowup/Segre embedding in \(\mathbf P^{11}\) of degree \(28\).

The needed curve-counting theorem must indeed be uniform for these varying finite-field presentations. A fixed-number-field family theorem alone would not suffice. The packet states the stronger Pila2005 contract; I treat that as an explicit theorem assumption, not as independently checked source text.

Finally,
\[
P_{2,X}(T)=
\frac{(1-pT)^2P_{\mathrm{par}}(T)}
{\prod_b(1-p^{\deg b}T^{\deg b})}
\]
has degree
\[
96+2-45=53.
\]
This correctly retains nonsplit closed basepoints. Replacing the denominator by \((1-pT)^{45}\) would be wrong unless all basepoints were rational.

No rational section, eigenbasis, or explicit parabolic projector is needed. Exact multiplication-back tests certify the performed polynomial divisions, though finite successful tests do not prove the universal cohomological identities.

---

## 8. Bit complexity, fallback, and the narrow theorem

The Weil bound gives
\[
|[T^k]P_2|\le \binom{53}{k}p^k\le2^{53}p^{53}.
\]
Hence the stated CRT modulus \(>2^{54}p^{53}\) suffices. Suitable primes can have largest size \(O(B)\), where \(B=O(\log p)\).

If every native intermediate size and reconstruction precision is bounded by a fixed polynomial in \(\ell,B\), then:

* enumerated points and dense algebra tables have polynomial total size;
* field arithmetic is polynomial in presentation degree and coefficient bits;
* local arithmetic is polynomial in \(e\log P\), not unit cost;
* p-maximalization and powering use \(\log p\);
* the final output has \(O(B)\) bits because its degree is fixed.

For the fallback, a direct projective enumeration through extension degree \(53\) has a bound such as \(p^{159}\operatorname{poly}(B)\). If triggered only when \(p\le Q(\ell)\) for a fixed polynomial \(Q\), this is polynomial in \(\ell,B\), and hence in \(B\). An input-dependent condition such as \(p\mid M\) is **not** automatically covered by this argument; the intrinsic-model and maximal-order repairs are what avoid that condition.

All randomized calls need a polynomial bound on their number and a proved capped clock. Allocating total error \(\eta\) across that number adds \(O(\log B+\log(1/\eta))\) to the required repetition parameters. A failed certificate must return FAIL. Full input reading, intermediate table construction, and output writing are included in these bounds.

### Narrowest defensible theorem

The following conditional theorem is supported by the composition analysis:

> **Conditional native reconstruction theorem.**  
> For the fixed smooth-quintic family and \(n=62,r=220\), assume the stated uniform native cover/normalization contracts, certified small-characteristic module and lifting contracts, an effective uniform canonical-coordinate height theorem with the indicated model hypotheses, and the stated all-field fixed-presentation curve-counting theorem. Include the fresh KM initialization and globally equivariant encoding described above. Then there is a randomized algorithm taking only the binary prime and quintic coefficients, returning the exact degree-53 \(P_2\) or FAIL, with failure probability at most \(\eta\), in
> \[
> (B+\log(1/\eta)+2)^C
> \]
> bit operations for a fixed constant \(C\).

These are assumptions about **uniform algorithms and theorems**, not permission to supply their outputs as extra native-input advice.

### Indispensable closure work and falsifiers

The highest-priority remaining derivation is the effective height theorem: specify the particular model, prove its point-height and Green bounds, retain the base-value dependence, and produce an effective coefficient bound usable to choose \(e\).

Other indispensable checks are:

1. **Integral mod-\(\ell\) monodromy:** failure of vanishing-cycle spanning or of the transvection hypotheses invalidates the fixed \(m\).
2. **Fresh RR data:** changing \(D_0\) without rebuilding coordinates is invalid; a residue rank or unit-pivot failure must not be ignored.
3. **Global equivariance:** invariance only under auxiliary Frobenius does not prove rational reconstruction coefficients. The full Galois-equivariant encoding is required.
4. **Actual bit bounds:** low field degree does not excuse an exponentially large basis or recursively inflated coordinate heights.
5. **Target locality:** any remaining demand to directly reduce bad numerical coordinates, or to assume \(p>\ell^m\), introduces a new obligation.
6. **Boundary source scope and conventions:** the curve theorem must be all-field uniform, and the input matrix must be arithmetic on \(W(0)=H^1(U,L')(2)\), as used above.

**Final disposition: no fatal mathematical obstruction found in the repaired composition; conditional correctness and polynomial-size interfaces are substantially defensible. Full native classical matching remains OPEN until the effective height/source contracts and the explicit RR reinitialization output are established, rather than inferred from advisory acceptance labels.** No hardness, quantum speedup, or separation follows from this review.