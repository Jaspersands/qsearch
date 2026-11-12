## Verdict

**There is a classical randomized polynomial-BIT algorithm for the stated quadratic interface.** It does not need a fundamental unit, a complete \(S\)-unit basis, auxiliary class-generating primes, or principal-ideal generators.

The useful extra information in the supplied Bosma–Stevenhagen source is **not merely the output of represented 2-class generators**. Its §§5–6 give a matrix-producing construction of a square represented by a principal-genus form. That supplies small rational-norm solutions. After primitive normalization, their numerators are automatically in \(K(S,2)\), without factoring their additional support.

The distinction is important: the returned elements are generally **virtual \(S\)-units**, not actual \(S\)-units. Their valuations outside \(S\) are even, rather than necessarily zero. That is exactly the interface requested here.

---

## 1. Precise statement

Write
\[
K=\mathbf Q(\sqrt d),\qquad
D=\operatorname{disc}(K),
\]
where \(d\) is squarefree. Let \(P\) be an explicitly listed set of rational primes containing every prime dividing \(2D\), and let \(S\) contain **all** primes of \(K\) above \(P\). Put \(m=|P|\).

Assume:

* a native presentation of \(K\) and its maximal order;
* the complete factorization of \(D\);
* the prime list \(P\).

Let \(L\) be the total input bit length.

**Theorem.** Using the polynomial-time quadratic-form routines stated in the supplied Bosma–Stevenhagen §§2, 5 and 6, one can compute, in unconditional Las Vegas expected time \(L^{O(1)}\):

1. a complete \(\mathbf F_2\)-basis of \(K(S,2)\);
2. representatives of that basis in ordinary, polynomial-bit native coordinates;
3. explicit localization matrices at every prime in \(S\), and at every archimedean place, in explicitly constructed local squareclass frames;
4. the rational norm-squareclass matrix.

There are at most \(2m+1\) basis elements. No newly occurring integer needs to be factored.

If the “rational set” is instead supplied as composite support integers, rather than a prime list, factoring those integers is a **separate integer-factoring-oracle preprocessing step**. GRH is unnecessary for the randomized theorem.

The proof and algorithm follow.

---

## 2. The quadratic norm gives the right exact sequence

Let
\[
V_P=\mathbf Q(P,2)
  =\langle -1,\ p:p\in P\rangle
  \subset \mathbf Q^\times/\mathbf Q^{\times2}.
\]

### 2.1 Kernel of the norm

For every quadratic extension,
\[
\ker\!\left(
N:K^\times/K^{\times2}\longrightarrow
\mathbf Q^\times/\mathbf Q^{\times2}
\right)
=\operatorname{image}(\mathbf Q^\times).
\]

Here is the elementary argument, so no norm-solving operation is hidden. If \(N\alpha=r^2\), then \(\gamma=\alpha/r\) has norm one. Write
\[
\gamma=\beta/\bar\beta.
\]
One can take \(\beta=1+\gamma\) unless \(\gamma=-1\), in which case take \(\beta=\sqrt d\). Consequently
\[
[\alpha]=[r/N\beta]
\]
is a rational squareclass.

For a rational class lying in \(K(S,2)\), its valuation at every rational prime outside \(P\) must be even: those primes are unramified, so their ramification indices are one. Thus the kernel on \(K(S,2)\) is precisely the image of \(V_P\).

The only rational squareclasses becoming squares in \(K\) are \(1\) and \(d\). Therefore
\[
\ker(N|_{K(S,2)})\cong V_P/\langle d\rangle,
\qquad
\dim_{\mathbf F_2}\ker N=m.                     \tag{1}
\]

This kernel already incorporates the relevant torsion phenomena. For example, in \(\mathbf Q(i)\), one must not simply append \(-1\); instead
\[
[i]=[2],\qquad (1+i)^2=2i,
\]
and the rational-kernel construction includes that class.

### 2.2 Possible norm classes

For \(\alpha\in K(S,2)\), the rational norm has even valuations outside \(P\). Moreover:

* an inert prime has residue degree two, so its norm valuation is always even;
* an imaginary quadratic norm is positive;
* a real quadratic norm can have either sign.

Define the rational squareclass space
\[
A=
\begin{cases}
\langle p\in P:\ p\text{ split or ramified}\rangle,&D<0,\\[2mm]
\langle -1,\ p\in P:\ p\text{ split or ramified}\rangle,&D>0.
\end{cases}                                                    \tag{2}
\]

The remaining task is to compute the norm image inside \(A\), with explicit lifts. Genus characters and the **constructive proof** of Bosma–Stevenhagen 3.4 do this.

---

## 3. Compute the norm image using genus characters

### 3.1 Forms attached to the generators of \(A\)

For each positive generator \(p\) of \(A\), construct a primitive form
\[
Q_p=(p,b,c),\qquad b^2-4pc=D.
\]

For odd \(p\), choose \(b\) with the appropriate parity and
\[
b^2\equiv D\pmod p.
\]
A root exists because \(p\) is split or ramified. If \(p\mid D\), use the zero root modulo \(p\). Fundamental-discriminant valuations ensure primitivity at ramified odd primes.

The prime \(2\) requires explicit treatment. Suitable forms are:

\[
\begin{array}{c|c}
\text{case}&Q_2\\ \hline
D\text{ odd},\ D\equiv1\pmod8
 &(2,1,(1-D)/8)\\
D=4d,\ d\equiv2\pmod4
 &(2,0,-d/2)\\
D=4d,\ d\equiv3\pmod4
 &(2,2,(1-d)/2).
\end{array}
\]

If \(D\) is odd and \(D\equiv5\pmod8\), then \(2\) is inert and is omitted from \(A\), **not** from the rational kernel (1).

For \(D>0\), also construct the form with first coefficient \(-1\):
\[
Q_{-1}=(-1,b,(D-b^2)/4),
\]
with \(b=0\) for even \(D\), and \(b=1\) for odd \(D\).

This is the real sign/orientation class. It is **not declared principal**. The source’s example \((-1,0,d)\), on p. 286, is exactly the warning against doing that.

### 3.2 The genus-character matrix

Factor the fundamental discriminant into prime discriminants
\[
D=\prod_i \delta_i.
\]
Use all characters
\[
\chi_i(n)=\left(\frac{\delta_i}{n}\right).
\]
Keeping the one redundant character is harmless.

For a primitive form \(Q\), evaluate \(\chi_i([Q])\) on an integer represented by \(Q\) and coprime to \(2D\). This implements the definition on p. 291 without reconstructing the missing OCR display (3.3):

* for each prime \(\ell\mid2D\), one of
  \[
  Q(1,0),\quad Q(0,1),\quad Q(1,1)
  \]
  is nonzero modulo \(\ell\);
* choose the corresponding pair modulo \(\ell\);
* combine these pairs by CRT;
* evaluate \(Q\) on the resulting pair.

All coordinates and the represented integer have \(O(L)\) bits. Character evaluation needs no factorization of that represented integer.

Let \(G\) have one column for each generator of \(A\), containing these genus-character values, encoded in \(\mathbf F_2\). Compute
\[
W=\ker G.                                                     \tag{3}
\]

### 3.3 Why every norm lies in \(W\), including the real sign

This is a strict-class calculation, not a Pell decision.

For a positive prime generator, \(Q_p\) represents the class of a prime ideal above \(p\), up to inversion; inversion is immaterial modulo \(2\operatorname{Cl}^+(K)\).

For \(D>0\), let
\[
\delta=[(\sqrt d)]\in\operatorname{Cl}^+(K).
\]
The class of a principal ideal \((\alpha)\) is zero if \(N\alpha>0\), and is \(\delta\) if \(N\alpha<0\). This follows by dividing by \(\sqrt d\) in the second case and changing an overall sign if necessary. The form \(Q_{-1}\) carries this orientation class.

Suppose
\[
N\alpha=q\,r^2,\qquad
q=(-1)^{e_-}\prod p^{e_p}\in A.
\]
At split primes, conjugate ideal classes are negatives of each other; at inert primes, the prime ideal is rational principal; and at ramified primes, the prime ideal squares to \((p)\). Factoring \((\alpha)\) **for this proof only** consequently gives
\[
\sum_p e_p[Q_p]+e_-[Q_{-1}]
       \in 2\operatorname{Cl}^+(K).
\]
All genus characters vanish, so the norm vector belongs to \(W\).

No factorization of an algorithmically produced ideal is performed here.

The converse requires an explicit lift. That is where the source’s ternary matrices matter.

---

## 4. Lift a genus-kernel vector without Pell or principalization

Take a basis vector of \(W\), represented by the squarefree signed integer
\[
q=(-1)^{e_-}\prod p^{e_p}.
\]

Construct a primitive form
\[
Q=(q,b,c),\qquad b^2-4qc=D,
\]
using the corresponding CRT congruences. Its genus character vector is the sum of the selected columns, hence zero. This can also be recomputed as an exact check before proceeding.

### 4.1 What is used from Bosma–Stevenhagen

The bare statement “return \(P\) with \(2[P]=[Q]\)” would not by itself provide the required field element.

The supplied source gives more:

* §5, ending on p. 305, constructs and retains a unimodular matrix reducing an indefinite determinant-\(-1\) ternary form to
  \[
  \Phi(X,Y,Z)=Y^2-2XZ,
  \]
  with the stated polynomial-time bound;
* §6.1 completes a principal-genus binary form to such a ternary form using modular square roots at the **known factors of the discriminant**;
* Theorem 6.6 and the discussion on pp. 307–308 provide the proper representation of the binary form by \(\Phi\).

Thus retain the matrix already computed by this algorithm. No missing formula for the halved binary form is needed.

### 4.2 Extract a represented square

For an even discriminant, the retained matrix gives linear forms \(L_1,L_2,L_3\) such that
\[
Q(u,v)=L_2(u,v)^2-2L_1(u,v)L_3(u,v).
\]
Write
\[
L_1(u,v)=a_1u+b_1v.
\]
Set
\[
(u,v)=(b_1,-a_1),\qquad w=L_2(u,v).
\]
Then
\[
Q(u,v)=w^2.                                                  \tag{4}
\]

The vector is nonzero: otherwise the restriction would have rank at most one. Also \(w\ne0\), since a nonzero rational isotropic vector for \(Q\) would make its discriminant a square.

All quantities have polynomial bit length because the source computes the transformation matrix in polynomial time.

For odd \(D\), first make the leading coefficient odd by a small recorded unimodular substitution, and replace
\[
(a,b,c)\quad\text{by}\quad(a,2b,4c).
\]
This is a primitive form of discriminant \(4D\). Its genus characters are the same conductor-two lift described at the start of §6; no additional dyadic character is introduced in this case. Apply the even-discriminant procedure, then undo the recorded substitutions. The factorization of \(4D\) is already available.

### 4.3 Turn the represented square into a small norm solution

From (4), form an integral solution
\[
x^2-dy^2=qz^2
\]
as follows:

\[
\begin{array}{c|ccc}
 &x&y&z\\ \hline
D=d\text{ odd}&2qu+bv&v&2w\\
D=4d&qu+(b/2)v&v&w .
\end{array}
\]

Divide \(x,y,z\) by their common gcd. Then output
\[
\alpha_q=x+y\sqrt d.                                         \tag{5}
\]
It satisfies
\[
N\alpha_q=qz^2,\qquad \gcd(x,y,z)=1.                          \tag{6}
\]

This norm equation was **computed and charged**, not supplied as an oracle.

### 4.4 Why primitive normalization eliminates the support problem

Let \(\ell\notin P\). Then
\[
\ell\nmid 2dq.
\]

If \(\ell\) is inert and divides \(\alpha_q\), reduction in
\(\mathbf F_{\ell^2}\) forces \(\ell\mid x,y\). Equation (6) then forces
\(\ell\mid z\), contradicting primitivity.

If \(\ell\) splits, the two prime ideals above \(\ell\) cannot both divide \(\alpha_q\): that would again force \(\ell\mid x,y,z\). Their valuation sum is
\[
v_\ell(N\alpha_q)=2v_\ell(z).
\]
Since at most one valuation is nonzero, each is even.

Therefore
\[
[\alpha_q]\in K(S,2).
\]

**No factorization of \(z\), \(N\alpha_q\), or any new prime support is needed.** Additional primes in the representative occur only to even valuation.

This proves the reverse inclusion in (3):
\[
N(K(S,2))=W.                                                 \tag{7}
\]

---

## 5. Return a complete basis

Choose a basis of \(V_P/\langle d\rangle\) by omitting one standard generator whose coordinate in \([d]\) is nonzero. This gives \(m\) rational representatives.

Append one element \(\alpha_q\) from (5) for every basis vector of \(W\).

The resulting list is a basis:

* its rational part is independent by (1);
* the appended elements have independent norm classes;
* any class in \(K(S,2)\) can first have its norm cancelled using the appended elements, after which it lies in the rational kernel.

In particular,
\[
\boxed{\displaystyle
\dim_{\mathbf F_2}K(S,2)=m+\dim_{\mathbf F_2}\ker G.}           \tag{8}
\]

This proves completeness without a unit-rank heuristic or a finite-index-unit assertion.

### What this does—and does not—say about units

Every unit squareclass is in the returned span. However, the algorithm does **not** select a basis for the actual subgroup \(O_{K,S}^{\times}/O_{K,S}^{\times2}\).

That stronger output is unnecessary here. In particular, a lift of the norm class \(-1\) need not be a norm-\(-1\) unit. Confusing those two statements would quietly reintroduce negative Pell. The unknown real ambiguous relation discussed on pp. 292–293 and recovered on p. 296 is never supplied for free or guessed.

---

## 6. Explicit local squareclass maps

These are field-squareclass localization maps, not a re-audit of the conditional Jacobian local-image routines.

All returned representatives have polynomial-bit ordinary coordinates. Subsequent changes of basis can be stored as binary matrices; no fundamental unit or large power is expanded.

### 6.1 Native coordinates and prime labels

Convert between the native quadratic presentation and the standard basis
\[
1,\sqrt d\quad\text{or}\quad1,(1+\sqrt d)/2.
\]
In degree two, these are exact polynomial-bit linear operations using the supplied maximal order and discriminant. Their input, arithmetic and output costs are included.

At split primes, choose and retain the two roots in the native presentation. These label the two prime ideals and the corresponding local components. No abstract local-field identification is left unpaid.

### 6.2 Odd primes: split, inert and ramified

For a prime ideal \(\mathfrak p\mid p\), \(p\) odd, use
\[
E^\times/E^{\times2}\cong
\langle[\pi]\rangle\oplus
\langle[\widetilde u]\rangle,
\qquad E=K_{\mathfrak p},
\]
where \(\pi\) is a uniformizer and \(u\) is a residue-field nonsquare.

Suitable uniformizers are:

* \(\pi=p\) at split and inert unramified primes;
* \(\pi=\sqrt d\) at odd ramified primes.

For \(\alpha\), output
\[
\left(
v_{\mathfrak p}(\alpha)\bmod2,\
\chi_{\mathbf F_{p^f}}
  \bigl(\overline{\alpha\pi^{-v_{\mathfrak p}(\alpha)}}\bigr)
\right).
\]

Here \(f=2\) at an inert prime and \(f=1\) otherwise. The quadratic character is computed by Euler powering; no discrete logarithm is used. A residue nonsquare is found by verified random sampling, with constant expected trials.

Inert primes were omitted only from the **norm-image candidate space** (2). Their rational-prime generators and their local maps remain present.

### 6.3 Dyadic places

For \(E/\mathbf Q_2\), let \(e=v_E(2)\). Since the global degree is two, \(e,f\le2\) and \(ef\le2\).

Use
\[
U_{2e+1}\subset E^{\times2}.
\]
Construct the finite unit group modulo \(\pi^{2e+1}\), enumerate its squares, and select an \(\mathbf F_2\)-basis of the quotient. Append the uniformizer bit.

This enumeration has **constant size**:
\[
|\mathcal O_E/\pi^{2e+1}|\le64.
\]
It supplies actual frame representatives and a complete lookup/evaluation map, not an abstract identification.

Uniformizers can be chosen explicitly:

* \(2\) in the split or unramified case;
* \(\sqrt d\) if \(d\) is even;
* \(1+\sqrt d\) if \(d\equiv3\pmod4\).

The resulting local dimensions are \(3\) for \(\mathbf Q_2\) and \(4\) for a quadratic extension of \(\mathbf Q_2\).

### 6.4 Precision and valuation costs

For every returned integral representative \(\alpha\),
\[
0\le v_{\mathfrak p}(\alpha)
 \le \left\lceil\log_2\!\bigl(2|N\alpha|\bigr)\right\rceil=:V_\alpha.
\]
Its norm has polynomial bit length, so \(V_\alpha\) is polynomial **numerically**, not merely binary-encoded.

Thus arithmetic through local precision \(V_\alpha+2e+1\), together with the charged native-coordinate conversion, suffices. At odd primes only residue precision is needed after normalization. Factoring the norm is unnecessary: valuations are computed at the already specified primes.

### 6.5 Real places, complex places and norm rows

For \(D>0\), compute both signs of
\[
x+y\sqrt d,\qquad x-y\sqrt d
\]
by exact integer comparisons, using \(x^2\) versus \(dy^2\) when required. No uncharged real approximation is needed.

Complex squareclass groups are trivial.

The norm matrix is already known:

* every rational-kernel column has trivial norm class;
* the column for \(\alpha_q\) is the vector of \(q\).

If norms are independently evaluated through valuations, the formula uses residue degrees:
\[
v_p(N\alpha)=\sum_{\mathfrak p\mid p}
                  f_{\mathfrak p}v_{\mathfrak p}(\alpha),
\]
not ramification indices.

The same local procedure also handles any additional explicitly supplied polynomial-bit prime. An infinite list of local maps is neither required nor claimed.

---

## 7. Bit clock and randomness ledger

Let \(t\) be the number of prime-discriminant factors of \(D\).

### Charged work

* Reading and native-coordinate conversion: polynomial in \(L\).
* Splitting tests and initial forms: \(O(m)\) modular square-root problems with \(O(L)\)-bit moduli.
* Genus matrix: at most \(t(m+1)\) character entries, with polynomial-bit CRT and Jacobi/Kronecker arithmetic.
* Binary kernel computation: \(O((m+t+1)^3)\) elementary binary operations using ordinary elimination.
* Lifts: at most \(m+1\) matrix-producing principal-genus representation calls.
* All input forms for those calls have \(O(L)\)-bit coefficients.
* Each lift uses modular square roots only at the supplied factors of \(D\), or \(4D\).
* There are \(O(m^2)\) basis-element/place localization evaluations.
* There are \(O(m)\) field representatives and \(O(m^2)\) localization-matrix bits to output.

Let \(T_{\rm rep}(h)\) be the polynomial bit bound for the matrix-producing binary/ternary routines cited above, and let \(H(L)=L^{O(1)}\) bound their returned matrix entries and the coordinates in (5). A charged clock is
\[
\mathbf E[T]
 \le (m+1)T_{\rm rep}(O(L))
       +\operatorname{poly}(L,m,t,H(L)).
\]
The local arithmetic in the second term has degree at most two and precision at most \(O(H(L)+L)\) local digits. Hence the displayed clock is polynomial in the original bit input.

The supplied scan does not state a sharp Lagarias exponent; I do not invent one. The polynomial bound comes from the source’s matrix-producing algorithm, **not** from its §7 timing table.

Randomness is confined to verified finite-field nonresidue/square-root preparation. These are Las Vegas operations. Capping each nonresidue search after
\[
O(\log(L/\eta))
\]
trials gives a fixed polynomial clock with abort probability at most \(\eta\). A completed output remains exact.

All data are ordinary bit strings. There is no quantum state preparation, coherent input access, QRAM, or compact-unit recovery cost being omitted.

---

## 8. Unconditional, factoring-oracle and GRH status

| Input regime | Supported conclusion |
|---|---|
| Factored \(D\), maximal order native, explicit prime list \(P\) | **Unconditional randomized polynomial-BIT algorithm.** No additional integer factoring. |
| Additional support supplied only as composite integers | **Polynomial-time relative to ordinary integer factoring** for that preprocessing; the rest is the preceding algorithm. |
| Deterministic version with the factorizations available | The GRH nonresidue derandomization stated on p. 307 can be used; **GRH is not a class-generation assumption here**. |
| Unfactored general native discriminant/support | No unconditional classical polynomial factoring claim is made. |

For completeness, degree-two residue-field frame construction does not introduce a new GRH promise: at an inert odd prime, \(d\) is already a known nonsquare in \(\mathbf F_p\). Square roots in \(\mathbf F_{p^2}\) reduce to prime-field square roots, and successive square roots of \(-1\) yield a residue nonsquare in \(O(\log p)\) steps. Dyadic frame construction is constant-size enumeration.

GRH does not make arbitrary integer factorization free.

---

## 9. Audit checks and falsifiers

The substantive proof obligations are explicit:

1. **Retain the ternary transformation matrix.** Returning only the halved form is insufficient. The required matrix is the one constructed on pp. 305–308. An implementation that discards it cannot replace it by an uncharged Pell/principalization call.
2. **Verify every lift exactly:**
   \[
   Q(u,v)=w^2,\qquad
   x^2-dy^2=qz^2,\qquad
   \gcd(x,y,z)=1.
   \]
3. **Preserve strict signs.** The \(-1\) column is the orientation class, not an assumed identity.
4. **Verify local frames in the same native components.** In particular, split-prime labels and dyadic quotient tables must accompany their binary vectors.

A concrete falsifier of the support lemma would be a verified primitive triple in (6), together with a prime \(\ell\nmid2Dq\), for which \(x+y\sqrt d\) has odd valuation at a prime above \(\ell\). The split/inert argument above rules this out; it is not an inference from finite experiments.

### Consequence for the proposed comparator

For this quadratic, Galois-stable-\(S\) interface, the compact-\(T\)-unit route is unnecessary. **The supplied quadratic-form machinery already gives a classical polynomial-BIT replacement, with explicit local maps, once the stated factorizations are available.**

This does not compute a fundamental unit, does not establish classical polynomial-time integer factoring, and does not extend to arbitrary-degree field factors. It also supplies no necessity, hardness, separation, or general quantum-speedup claim.