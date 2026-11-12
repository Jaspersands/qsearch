## Verdict

**The proposed determinant division is correct under the stated hypotheses.** It eliminates explicit parabolic-subspace computation—and therefore the repaired Kummer specialization/filter interface—**when the desired output is only the characteristic polynomial**.

There is one notational correction: on the dual of nodal cohomology, the local operator is
\[
q^{2}F_{\mathrm{node}}^{-\mathsf t},
\]
not literally \(q^{2}F_{\mathrm{node}}^{-1}\) in the original basis. Their characteristic polynomials agree, so **the proposed factor \(B_z(T)\) is unchanged**.

This is a conditional post-processing theorem. It does **not** construct the genuine arithmetic matrix \(F_W\), improve its reconstruction cost, or close the native classical comparator.

---

## 1. The finite-coefficient boundary sequence is valid

All cohomology in this section is geometric, with its residual Frobenius action. Put
\[
V=L'=R^1f_*\mathbf F_\ell,\qquad
K_\ell=H^1(\mathbf P^1_{\overline{\mathbf F}_p},j_*V),\qquad
E_\ell=H^1(U_{\overline{\mathbf F}_p},V).
\]

### The \(j_!/j_*\) comparison

There is an exact sequence of ordinary constructible sheaves
\[
0\longrightarrow j_!V\longrightarrow j_*V
 \longrightarrow
 \bigoplus_{\bar z\in Z(\overline{\mathbf F}_p)}
 i_{\bar z,*}V^{I_{\bar z}}
 \longrightarrow0.                                      \tag{1}
\]

This is checked on geometric stalks: it is the identity on \(U\), while at a puncture the stalks are \(0\), \(V^{I_{\bar z}}\), and \(V^{I_{\bar z}}\).

The skyscraper sheaves in (1) have no positive-degree cohomology **over the algebraically closed geometric base**. Consequently,
\[
H^2(\mathbf P^1,j_*V)\simeq H^2_c(U,V).
\]
Finite-coefficient Poincaré duality gives
\[
H^2_c(U,V)\simeq H^0(U,V^\vee)^\vee(-1).
\]
Full geometric \(\operatorname{Sp}_{62}(\mathbf F_\ell)\) monodromy implies
\(H^0(U,V^\vee)=0\). Indeed, its central element \(-I\) already excludes invariants because \(\ell\) is odd. No averaging over the order of the symplectic group is involved. Thus
\[
H^2(\mathbf P^1,j_*V)=0.                                 \tag{2}
\]

### Leray for the open immersion

The stalk of \(R^1j_*V\) at \(\bar z\) is \(H^1(I_{\bar z},V)\). In this tame situation, inertia has \(\ell\)-cohomological dimension one. Hence Leray, together with (2), gives the Frobenius-equivariant short exact sequence
\[
\boxed{
0\longrightarrow K_\ell\longrightarrow E_\ell
 \longrightarrow
 \bigoplus_{\bar z}H^1(I_{\bar z},V)
 \longrightarrow0.
}                                                        \tag{3}
\]

Moreover, (1) shows that \(H^1_c(U,V)\to K_\ell\) is surjective. Thus \(K_\ell\) is precisely the usual parabolic image inside \(H^1(U,V)\).

This proves the needed sequence in finite coefficients; it does not identify ordinary open cohomology with parabolic cohomology.

---

## 2. The two local Tate factors

Fix a closed critical value \(z\) of degree \(f\), put \(q=p^f\), and choose one geometric point above it.

### Procyclic inertia, not a finite cyclic quotient

Although a local transvection on \(V\) has finite order \(\ell\), its cohomology must be computed using actual inertia. Wild inertia contributes no higher \(\ell\)-cohomology and acts trivially here. The relevant tame factor is
\[
\mathbf Z_\ell(1),
\]
whose \(\ell\)-cohomological dimension is one.

Choosing a tame generator \(\tau\), continuous cohomology gives
\[
H^1(I_z,V)\simeq V/(\tau-1)V
\]
as vector spaces. Its Frobenius action contains a Tate factor.

Let \(\Phi_z\) be geometric \(q\)-Frobenius. Then
\[
\Phi_z^{-1}\tau\Phi_z=\tau^q.
\]
For a cocycle \(c\), modulo \((\tau-1)V\),
\[
(\Phi_z c)(\tau)
 =\Phi_z c(\tau^q)
 \equiv q\,\Phi_z c(\tau).
\]
Therefore, equivariantly,
\[
\boxed{H^1(I_z,V)\simeq V_{I_z}(-1).}                     \tag{4}
\]

Using \(C_\ell\) instead of procyclic inertia would introduce generally nonzero higher group cohomology and would not justify this Leray argument.

### Invariant–coinvariant duality

The smooth-fibre cup-product pairing is perfect:
\[
V\times V\longrightarrow\mathbf F_\ell(-1).
\]
It induces a perfect pairing between coinvariants and invariants, hence
\[
V_{I_z}\simeq (V^{I_z})^\vee(-1).                         \tag{5}
\]
This follows directly by taking annihilators of \((I_z-1)V\). It does not require a semisimple inertia representation, or a nondegenerate restriction of the pairing to \(V^{I_z}\).

Combining (4) and (5),
\[
\boxed{
H^1(I_z,V)\simeq (V^{I_z})^\vee(-2).
}                                                        \tag{6}
\]

Thus the two factors of \(q\) have different origins:

1. \(q\) from invariant–coinvariant duality through the cup-product target \(\mathbf F_\ell(-1)\);
2. \(q\) from the tame-inertia cohomology twist.

### Finite-coefficient invariant cycles

Under the charged invariant-cycle hypothesis,
\[
V^{I_z}\simeq H^1(C_{z,\overline{\mathbf F}_q},\mathbf F_\ell).
\]

For a genuine regular one-node Lefschetz degeneration, this is not merely a rational-coefficient assertion. Étale-locally the degeneration has the semistable model \(xy=t\). The integral vanishing-cycle quotient is free of rank one, and Picard–Lefschetz monodromy is a primitive transvection. Specialization remains injective after reduction modulo \(\ell\), and both its image and the inertia-invariant space have dimension \(61\).

This qualification matters: a model \(xy=t^a\) with \(\ell\mid a\) could have trivial reduced monodromy and invalidate the claimed invariant dimension. The regular Lefschetz hypothesis excludes that failure.

Consequently,
\[
\boxed{
H^1(I_z,V)
 \simeq H^1(C_{z,\overline{\mathbf F}_q},\mathbf F_\ell)^\vee(-2),
}
                                                               \tag{7}
\]
so its geometric local Frobenius is
\[
q^2F_{\mathrm{node}}^{-\mathsf t}.
\]

---

## 3. Nodal cohomology gives exactly the proposed local factor

Let \(\nu:\widetilde C_z\to C_z\) be the normalization. Since the fibre has exactly one geometric singular point, that node is rational over \(\mathbf F_q\). Its two branches are either both rational over \(\mathbf F_q\), or conjugate over its quadratic extension.

The normalization sequence gives
\[
0\longrightarrow E_z
 \longrightarrow H^1(C_z,\mathbf F_\ell)
 \longrightarrow H^1(\widetilde C_z,\mathbf F_\ell)
 \longrightarrow0,                                      \tag{8}
\]
where \(E_z\) is the one-dimensional graph contribution.

Explicitly, \(E_z\) is the quotient of the permutation module on the two branches by its diagonal line. Frobenius therefore acts on it by
\[
\epsilon_z=
\begin{cases}
+1,&\text{split branches},\\
-1,&\text{nonsplit branches}.
\end{cases}
\]
There is **no Tate twist** on this graph contribution to untwisted \(H^1(C_z,\mathbf F_\ell)\). Hence
\[
P_{\mathrm{node},z}(S)
 =(1-\epsilon_zS)P_{\widetilde C_z}(S).                   \tag{9}
\]

In the supplied generalized-Jacobian language, the torus has arithmetic Frobenius \(\epsilon_z q\) on its \(\ell\)-torsion. Passing from \(H^1(C_z,\mu_\ell)\) to untwisted \(H^1(C_z,\mathbf F_\ell)\) removes that cyclotomic factor, leaving \(\epsilon_z\). This agrees with (8).

### Dualizing the normalization contribution

Write \(G_z\) for geometric \(q\)-Frobenius on
\(H^1(\widetilde C_z,\mathbf F_\ell)\). Its perfect alternating pairing satisfies
\[
G_z^{\mathsf t}JG_z=qJ.
\]
Therefore
\[
qG_z^{-\mathsf t}=JG_zJ^{-1},
\]
and consequently
\[
\det(1-Sq^2G_z^{-\mathsf t})
 =\det(1-SqG_z)
 =P_{\widetilde C_z}(qS)\pmod\ell.                        \tag{10}
\]
This is a matrix identity in finite coefficients, not an argument requiring distinct eigenvalues.

Dualizing (8), twisting by \((-2)\), and taking determinants now gives
\[
\det\!\left(1-S\Phi_z\mid H^1(I_z,V)\right)
 =(1-\epsilon_zq^2S)P_{\widetilde C_z}(qS)\pmod\ell.        \tag{11}
\]

In particular, replacing the first factor by \(1-\epsilon_zqS\) would be wrong.

### Closed-point induction

The \(f\) geometric punctures above \(z\) form one Frobenius cycle. If the return map is \(A\), the cyclic block-matrix identity is
\[
\det(1-TF)=\det(1-T^fA).
\]
It holds in every characteristic, including when \(\ell\mid f\); no averaging or diagonalization of that permutation is needed.

Applying it to (11) proves
\[
\boxed{
B_z(T)=
(1-\epsilon_zq^2T^f)\,
P_{\widetilde C_z}(qT^f)\pmod\ell,
\qquad q=p^f.
}                                                        \tag{12}
\]

Thus all three delicate features in the proposal are correct:

- \(q^2\) on the graph term;
- \(q\) inside the normalization numerator;
- \(T^f\) for a degree-\(f\) closed critical value.

---

## 4. Global determinant division

The stipulated arithmetic identification is
\[
W\simeq H^1(U,L)(1)=H^1(U,L')(2).
\]
Arithmetic Frobenius on the double twist is multiplied by \(p^2\). Therefore geometric Frobenius on \(E_\ell\) is
\[
F_{E,\mathrm{geo}}=p^2F_W^{-1}.
\]

Taking determinants in (3) yields
\[
\boxed{
P_{\mathrm{par},\ell}(T)=
\frac{\det(1-Tp^2F_W^{-1})}
{\displaystyle\prod_{z\in |Z|}
 (1-\epsilon_zp^{2f_z}T^{f_z})
 P_{\widetilde C_z}(p^{f_z}T^{f_z})}
\quad\text{in }\mathbf F_\ell[T].
}                                                        \tag{13}
\]

The quotient is a polynomial, not merely a formal power series.

Since \(\widetilde C_z\) has genus \(30\), each local factor has degree \(61f_z\). Also
\[
\sum_z f_z=220.
\]
Thus
\[
\deg P_{\partial}=220\cdot61=13420,
\]
and
\[
\deg P_{\mathrm{par},\ell}
 =13516-13420=96.
\]

Multiplicativity here only uses a Frobenius-stable short exact sequence: an adapted basis makes the matrix block triangular. Boundary and parabolic eigenvalues may coincide modulo \(\ell\), and either action may have Jordan blocks. **Neither circumstance obstructs division.**

No parabolic basis, vanishing-cycle vector, specialization map on reconstructed torsion, or eigenvalue-separation filter is needed.

---

## 5. Surface assembly works without rational basepoints or a rational section

Let \(Y=\operatorname{Bl}_B X\), with its proper pencil \(\pi:Y\to\mathbf P^1\). Under the stated fibre hypotheses,
\[
R^0\pi_*\mathbf F_\ell=\mathbf F_\ell,\qquad
R^1\pi_*\mathbf F_\ell=j_*L',\qquad
R^2\pi_*\mathbf F_\ell=\mathbf F_\ell(-1).
\]
The last equality uses geometric irreducibility and multiplicity one of every fibre.

For total degree two, the Leray graded pieces are
\[
\mathbf F_\ell(-1),\qquad K_\ell,\qquad\mathbf F_\ell(-1).
\]
The only relevant possible \(d_2\)-maps have source
\(H^0(\mathbf P^1,j_*L')=0\) or target
\(H^2(\mathbf P^1,j_*L')=0\). Thus these pieces give a Frobenius-stable filtration of \(H^2(Y,\mathbf F_\ell)\), sufficient to conclude
\[
P_{2,Y,\ell}(T)=(1-pT)^2P_{\mathrm{par},\ell}(T).          \tag{14}
\]

No Frobenius-equivariant splitting and no rational section are required. Alternatively, the sum of the exceptional sections is a rational multisection of degree \(45\), invertible modulo every admitted \(\ell\), so the suggested section-sum repair is also available.

For the blowup, the Frobenius-equivariant formula is
\[
H^2(Y,\mathbf F_\ell)
 \simeq H^2(X,\mathbf F_\ell)
 \oplus H^0(B,\mathbf F_\ell)(-1).
\]
For nonrational basepoints,
\[
P_B(T)=\prod_{b\in|B|}(1-T^{\deg b}),
\]
and the exceptional factor is exactly \(P_B(pT)\). Therefore
\[
\boxed{
\overline{P_{2,X}}(T)\,P_B(pT)
 =(1-pT)^2P_{\mathrm{par},\ell}(T).
}                                                        \tag{15}
\]
The degrees check:
\[
53+45=2+96=98.
\]

Combining (13) and (15) computes \(P_{2,X}\bmod\ell\) directly from the stipulated whole-open \(F_W\).

---

## 6. Native cost of the replacement

The boundary calculation has a fixed-degree native implementation. It does not require point counting on the growing-genus frame cover.

### Geometry and residue fields

From the given surface and pencil, charge:

1. fixed-degree elimination to obtain the critical-value scheme;
2. factorization of its degree-\(220\) defining data;
3. construction of each residue field
   \[
   k_z=\mathbf F_{p^{f_z}},\qquad f_z\le220;
   \]
4. solving for the unique node over \(k_z\);
5. factoring its degree-two tangent cone to obtain \(\epsilon_z\);
6. constructing the normalization.

For an ordinary node, the strict transform in the blowup at that node is its normalization. The graph/blowup equations and a projective embedding have degrees and ambient dimension bounded solely by the original fixed format. Hence the normalization has a bounded-format smooth projective model over \(k_z\), independent of \(p\) and \(\ell\).

There are **at most \(220\)** such normalizations. They are processed over their individual residue fields; no common splitting field is required.

Fixed-degree elimination and standard randomized finite-field factorization give polynomial bit cost in \(\log p\). If a deterministic bound is demanded, the chosen finite-field factorization/construction implementation must be charged accordingly; deterministic polynomial time should not be silently inferred from randomized routines.

### Smooth fixed-genus Frobenius data

Only genus-\(30\) curves are counted.

There is an important source-interface qualification: **the quoted Pila statement requires explicit Jacobian equations and addition laws.** It does not, by itself, make those inputs free.

There are two legitimate implementations:

- construct and charge that bounded-format Jacobian presentation, then apply Pila; or
- use the supplied **curve-input, divisor-based torsion theorem** for the smooth normalization, avoiding Pila’s explicit-embedding interface.

For the second implementation, at a prime \(\lambda\ne p\), the torsion has rank \(60\). If an explicit torsion-splitting field is desired, its extension degree divides
\[
|\operatorname{GL}_{60}(\mathbf F_\lambda)|
 <\lambda^{3600}.
\]
This deliberately crude bound is polynomial in numerical \(\lambda\), since the dimension is fixed. Field construction, representation, Frobenius evaluation, divisor arithmetic, and coordinate recovery must all be charged; they remain polynomial in \((\lambda,\log q)\) under the supplied torsion primitive. Divisor supports may remain closed places.

Actual \(q\)-power Frobenius on these divisor representatives gives the arithmetic torsion matrix. Kummer and the smooth-curve pairing then give the untwisted geometric characteristic polynomial. Determinants should be computed by an arbitrary-characteristic algorithm, **not** by Newton identities dividing by possibly zero integers modulo \(\lambda\).

For (13), computing \(P_{\widetilde C_z}\bmod\ell\) directly is enough. This gives boundary cost
\[
\operatorname{poly}(\ell,\log p).
\]

Alternatively, reconstruct each integer normalization numerator once. Its degree is \(60\), and
\[
|a_i|\le \binom{60}{i}q^{i/2}\le 2^{60}q^{30}.
\]
A CRT modulus exceeding \(2^{61}q^{30}\), using auxiliary primes \(\lambda=O(\log q)\), suffices. The supplied fixed-genus torsion routine then gives polynomial cost in \(\log q=O(\log p)\). Those integer local numerators can be reused for all target primes.

This uses no uniform polynomial-time theorem in a growing genus.

### Matrix access, precision, and output

If \(F_W\) is supplied as an \(m\times m\) matrix, reading it costs
\[
\Omega(m^2\log\ell)\quad\text{bits},\qquad m=13516.
\]
Its inversion, characteristic polynomial, and the two exact polynomial divisions have polynomial bit cost in the explicit matrix size and \(\log\ell\). Here \(m\) is fixed, albeit very large.

All calculations are exact finite-field or integer calculations. No numerical precision oracle, prepared quantum state, coherent access assumption, or free matrix-query model is used. If \(F_W\) is supplied only as an operator, charge the evaluations needed to recover its matrix.

Thus, with \(F_W\) conditional,
\[
\boxed{
T_{\mathrm{post}}(p,\ell)
 =\operatorname{poly}(\ell,\log p)
}
\]
including the native boundary geometry and local curve computations. The upstream cost \(T_W(p,\ell)\) remains additional.

---

## 7. CRT and the small-characteristic fallback

Write
\[
P_{2,X}(T)=1+c_1T+\cdots+c_{53}T^{53}.
\]
Smooth proper purity gives
\[
|c_i|\le\binom{53}{i}p^i\le2^{53}p^{53}.
\]
The charged integral torsion-freeness ensures that (15) really supplies the reductions of this integer polynomial. Hence
\[
\prod_{\ell\in\Lambda}\ell>2^{54}p^{53}
\]
is sufficient for unique centered CRT reconstruction.

Primes larger than \(53\), excluding \(p\), with largest prime \(O(\log p)\) suffice. Their number is also \(O(\log p)\). Consequently, the total boundary/post-processing overhead for reconstruction is polynomial in \(\log p\), including CRT and writing the \(54\) coefficients, each of \(O(\log p)\) bits.

With the convention \(P_2(T)=\det(1-TF_{\mathrm{geo}})\),
\[
\boxed{\#X(\mathbf F_p)=1+p^2-[T]P_{2,X}(T).}
\]

For an explicit upstream guard \(p\le Q(\ell)\), direct counting over extensions of degrees \(1,\dots,53\) costs \(p^{O(1)}\), because all dimensions and extension degrees are fixed. Thus
\[
p^{O(1)}\le Q(\ell)^{O(1)},
\]
which is polynomial in numerical \(\ell\). Integer Newton identities then recover \(P_2\). This is a genuine uniform fallback once \(Q\) is explicit; it need not hide an unspecified finite threshold. The boundary argument does not itself establish an upstream reconstruction guard \(Q\).

---

## 8. Remaining obligations and falsifiers

The mathematical division theorem has no additional local Tate, closed-point, or modular-semisimplicity obstruction. Its essential obligations are:

- **Genuine arithmetic \(W\):** the stipulated identification with \(H^1(U,L')(2)\), not an abstract module with an unknown arithmetic twist.
- **Modular monodromy and invariant cycles:** full geometric \(\operatorname{Sp}_{62}(\mathbf F_\ell)\), tame primitive transvections, and the finite-coefficient invariant-cycle identification.
- **Actual local geometry:** exactly one geometric node, geometric irreducibility, correct normalization, and the correct split/nonsplit sign.
- **Paid smooth-curve arithmetic:** either the supplied curve-input torsion primitive or a constructed, charged Pila Jacobian presentation.
- **Native reconstruction cost:** still conditional and separate. A bound polynomial in numerical \(p\) is not upgraded to polynomial in \(\log p\) by this repair.

Useful exact falsifiers are:

1. a nonzero remainder in division (13), or quotient degree other than \(96\);
2. a nonzero remainder in (15), or quotient degree other than \(53\);
3. an invariant-cycle dimension other than \(61\) at a purported one-node Lefschetz fibre;
4. disagreement with an independently obtained exact point count.

Passing these checks does not certify the upstream arithmetic identification; wrong inputs can pass necessary determinant checks.

**Bottom line:** retain ordinary Hom as **OPEN** cohomology. Divide its characteristic polynomial by the explicitly computed boundary determinant. That replacement is proved under the stated hypotheses and removes the parabolic Kummer filter for the scalar endpoint, while leaving full native torsion reconstruction—and any end-to-end classical complexity claim—conditional.