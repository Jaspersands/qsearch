# Local transport/offset audit

## Verdict

**The single local operation is not closed by this report.** There is an exact falsifier of **independent Jordan/BONG-component matching followed by lifting an arbitrary residue isometry**. There is also a polynomial-cost finite verification and spinor-extraction procedure once a sufficiently accurate seed exists.

These conclusions do **not** falsify every possible coupled, cross-scale matching algorithm. The packet does not specify such an algorithm, and I cannot supply its missing uniform construction. Claiming either a completed native algorithm or a general impossibility would therefore overstate the evidence.

All calculations below are deductions from the supplied data and displayed identities. No external source or executable control was consulted.

## 1. Exact dyadic falsifier: matching components independently is wrong

Work over \(\mathbf Q_2\). For \(m\ge2\), set
\[
 A_m=\operatorname{diag}(1,4,-25\,2^{2m}),\qquad
 B_m=\operatorname{diag}(5,20,-2^{2m}),
\]
and
\[
 U=\begin{pmatrix}
 1&-4&0\\
 1&1&0\\
 0&0&1/5
 \end{pmatrix}.
\]
Direct multiplication gives
\[
 U^TA_mU=B_m,\qquad \det U=1.
\]
Thus \(U\in\mathrm{SL}_3(\mathbf Z_2)\) is an exact proper integral local isometry. The forms are integral, nonsingular, indefinite over \(\mathbf R\), and have equal determinant
\[
 \det A_m=\det B_m=-100\,2^{2m}.
\]

Their displayed orthogonal decompositions are good BONGs, with valuation sequence
\[
 (0,2,2m).
\]
The unit squareclasses of the three Jordan lines are respectively
\[
 (1,1,-1),\qquad(5,5,-1).
\]
Since \(5\notin\mathbf Q_2^{*2}\), the first two rank-one components cannot be matched independently by scalar square roots. Nevertheless, the lattices are isometric: the necessary operation mixes the scale-\(1\) and scale-\(4\) lines.

Consequently:

* Unequal squareclasses in independently obtained good BONGs are **not** a valid NO certificate.
* Even distinct-scale rank-one Jordan components cannot simply be matched independently at dyadic places.
* This is not merely ambiguity inside a repeated-scale block.

### An apparently valid residue seed can be completely unliftable

The identity satisfies
\[
 A_m\equiv B_m\pmod4.
\]
But **no** exact isometry \(Y\equiv I\pmod2\) exists.

Indeed, its first column would have the form \((x,y,z)^T\), with \(x\) odd and \(y,z\) even. Then
\[
 x^2+4y^2-25\,2^{2m}z^2\equiv1\pmod8,
\]
whereas the required first-column norm is \(5\pmod8\).

Thus an irreversible lift starting from the identity residue class fails, although an exact transporter exists. Higher precision cannot repair that residue-class choice. The successful \(U\) has \(u_{21}\equiv1\pmod2\): information invisible in the original Gram congruence modulo \(2\) must determine a cross-scale residue entry.

For \(X=I\),
\[
 B_m^{-1}(X^TA_mX-B_m)
 =\operatorname{diag}(-4/5,-4/5,24),
\]
whose minimum valuation is \(2=2v_2(2)\). The strict square-root convergence hypothesis is not met. The correction lemma does not find the missing branch.

### The supplied rational identification need not reveal the answer

To defeat the preliminary shortcut “the supplied identification is already integral,” put \(a=5\,2^m\) and
\[
 R=\begin{pmatrix}
 5/4&0&3a/4\\
 0&1&0\\
 3/(4a)&0&5/4
 \end{pmatrix},\qquad F=RU.
\]
Then
\[
 R^TA_mR=A_m,\quad \det R=1,\quad F^TA_mF=B_m,
\]
but \(F\) is not \(2\)-integral. All displayed inputs have \(O(m)\) coefficient bits.

This is a cheap exact falsifier of the specified independent-matching/greedy-lifting implementation—not evidence of hardness. A coupled matcher can potentially handle it.

## 2. Finite certification: what a seed must actually certify

Let \(v(\pi)=1\), \(e=v(2)\), and choose
\[
 s_B\ge0,\qquad v((B^{-1})_{ij})\ge-s_B.
\]
Because \(B\) is integral, \(s_B=v(\det B)\) is always a safe, possibly wasteful choice.

A sufficient finite certificate is
\[
 X\in\mathrm{GL}_3(\mathcal O/\mathfrak p^M),\qquad
 X^TAX\equiv B\pmod{\mathfrak p^M},
 \qquad M=s_B+2e+3.
\]
Take integral representatives and write
\[
 T=B^{-1}(X^TAX-B).
\]
Then \(v(T)\ge2e+3\). The series
\[
 C=(I+T)^{-1/2}
\]
converges integrally, with
\[
 v(C-I)\ge v(T)-e.
\]
For example,
\[
 \binom{-1/2}{j}=(-1)^j\binom{2j}{j}/4^j
\]
gives the required valuation growth. Moreover, \(T\) is \(B\)-self-adjoint, so
\[
 (XC)^TA(XC)=B.
\]
This proves that the finite certificate represents an actual local isometry, not merely a truncated solution. Replace \(XC\) by its negative if necessary to make
\[
 g=(XC)F^{-1}
\]
proper.

Conversely, any integral local isometry supplies such a certificate by reduction. Thus this is an exact finite existence criterion—but **not an efficient search algorithm**. Failure of a particular seed, including the identity in §1, never certifies NO.

Different certified proper transporters give the same coset: their quotient is a proper integral stabilizer element.

## 3. Spinor extraction has a paid finite-precision formula

This stage does not require a full exact matrix over the completion.

Choose an expanded rational diagonalization
\[
 D=W^TAW=\operatorname{diag}(a_1,a_2,a_3),
 \qquad h=W^{-1}gW.
\]
Use the four proper diagonal sign changes
\[
 S_0=I,\quad
 S_1=\operatorname{diag}(1,-1,-1),\quad
 S_2=\operatorname{diag}(-1,1,-1),\quad
 S_3=\operatorname{diag}(-1,-1,1).
\]
Set \(t_j=1+\operatorname{tr}(S_jh)\). Since \(\sum_j S_j=0\),
\[
 \sum_jt_j=4.
\]
Hence some \(j\) satisfies \(v(t_j)\le2e\), and in particular \(t_j\ne0\). For that chart,
\[
 \boxed{\ \theta(g)=\theta(S_j)t_j
       \quad\bmod K_{\mathfrak p}^{*2}\ },
\]
where
\[
 \theta(S_0)=1,\quad
 \theta(S_1)=a_2a_3,\quad
 \theta(S_2)=a_1a_3,\quad
 \theta(S_3)=a_1a_2.
\]

Here is the algebra behind the formula. For reflections \(r_u,r_v\),
\[
 1+\operatorname{tr}(r_ur_v)
 =\frac{4\,b(u,v)^2}{q(u)q(v)}.
\]
Whenever this is nonzero, its squareclass is
\(\theta(r_ur_v)=q(u)q(v)\). An elementary rank-three reflection reduction writes a proper isometry as two reflections: one first fixes an anisotropic vector, and the remaining improper action on its binary orthogonal complement is a reflection. This is an algebraic identity, not an imported constructive complexity theorem.

The four charts avoid the false assumption that \(1+\operatorname{tr}(g)\) is always nonzero.

### Explicit precision

Suppose an approximation to \(Y=XC\) is known modulo \(\mathfrak p^N\). Define
\[
 \beta=
 \max(0,-\min v(W^{-1}_{ij}))
 +\max(0,-\min v((F^{-1})_{ij}))
 +\max(0,-\min v(W_{ij})).
\]
Then
\[
 N=\beta+4e+1
\]
suffices to know every \(t_j\) to absolute precision \(4e+1\). For a selected chart with \(v(t_j)\le2e\), this gives relative precision at least \(2e+1\), sufficient for its squareclass under the supplied local squareclass contract.

Finally reduce \(\theta(S_j)t_j\) modulo the supplied stabilizer spinor subgroup. Properness can also be checked at finite precision: the determinant ratio is exactly \(\pm1\), distinguishable modulo \(\mathfrak p^{e+1}\).

This completes a **finite verifier and offset extractor**, not the missing seed constructor.

## 4. Required exact \(p=17\) neighbor check

Write \(s=17^4=83521\). The packet’s forms are
\[
 A=\operatorname{diag}(1,289,-83521),\qquad
 B=\begin{pmatrix}9&0&1\\0&289&0\\1&0&-9280\end{pmatrix},
 \qquad B=P^TAP.
\]

At the place \(3\), take
\[
 v=(1,0,4),\qquad
 d=q_A(v)=1-16s=-1336335=-3\cdot445445,
\]
and let
\[
 g=r_vr_{e_2}.
\]
The vectors are orthogonal, so \(g\) is a proper involution. Its spinor norm is
\[
 \theta(g)=d\cdot289\equiv d\pmod{\mathbf Q_3^{*2}}.
\]
Since
\[
 d/3=-445445\equiv1\pmod3,
\]
this is precisely the squareclass of \(3\).

The actual local transporter certificate is \(X=gP\):
\[
 gP=
 \begin{pmatrix}
 3(d-2)/d&0&(-1-8s)/(3d)\\
 0&-1&0\\
 -24/d&0&(16s-7)/(3d)
 \end{pmatrix}.
\]
Here \(v_3(d)=1\), while the last-column numerators are
\[
 -668169,\qquad1336329,
\]
both divisible by \(9\). Thus \(gP\) is \(3\)-integral. Its determinant is \(1\), so it lies in \(\mathrm{SL}_3(\mathbf Z_3)\), and
\[
 (gP)^TA(gP)=B.
\]

The chart formula also passes exactly. With
\(S_3=\operatorname{diag}(-1,-1,1)\),
\[
 \theta(S_3)=289,\qquad
 1+\operatorname{tr}(S_3g)=4/d,
\]
giving squareclass \(d\), hence \(3\). By contrast,
\(1+\operatorname{tr}(g)=0\): the unqualified single-trace formula fails this control.

At every finite place other than \(3\), \(P\) and \(P^{-1}\) are integral. Choose \(X=P\), giving \(g=I\) and offset \(1\).

**In particular, the offset at the place \(17\) is \(1\), not \(3\).** The neighbor idele has its nontrivial component at \(3\). The packet’s character evaluates it as
\[
 (3/17)=-1.
\]
This reproduces the supplied spinor obstruction; replacing the ray-class quotient by the ordinary class group would miss it.

## 5. Costs, cheapest attacks, and outstanding obligation

Let \(q=p^f\), \(r_{\mathfrak p}=v(p)\), and \(n=[K:\mathbf Q]\). Then
\[
 [K_{\mathfrak p}:\mathbf Q_p]=r_{\mathfrak p}f\le n.
\]
Here \(e=r_{\mathfrak p}\) at dyadic places and \(e=0\) otherwise.

For the verifier:

* Expanded input access and order-table arithmetic are charged.
* Exact valuations of nonzero expanded elements are bounded using their field-norm heights after clearing denominators.
* Consequently \(s_B,\beta,M,N\) have polynomial native-bit bounds.
* Precision-\(M\) residues carry \(M\log q\) information bits; their expanded coordinate representation and ideal arithmetic must also be charged.
* The series needs only polynomially many fixed-size matrix operations at the stated precision.
* The seed certificate and squareclass/coset output have polynomial size. No quantum state preparation is used by these classical deductions.

These bounds do **not** pay for finding \(X\).

The cheapest classical attacks on a proposed implementation are therefore:

1. Check whether the supplied \(F\) is already integral with integral inverse.
2. Run the family in §1. Any componentwise squareclass rejection or irreversible identity-residue lift is incorrect.
3. Audit cross-scale seed selection for dependence polynomial in **\(\log q\)**, ramification, and valuations—not enumeration of residue candidates.
4. Run the exact neighbor calculation in §4, including the location of the nontrivial idele component and the trace-chart degeneracy.

The remaining proof obligation is a concrete, uniformly bounded **coupled dyadic seed algorithm**, with a valid negative branch when genus differs. It must select residue classes using the higher-order constraints exposed in §1; listing Jordan/BONG invariants or invoking classification is not that construction.

**Final status:** the restricted independent-matching/greedy-lifting realization is falsified. Finite certification and spinor extraction are accounted for. A general coupled transporter or coset-only constructor is neither supplied nor disproved here; no hardness or speedup follows.