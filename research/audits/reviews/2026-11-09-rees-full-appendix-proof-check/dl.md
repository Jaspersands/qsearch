# Proof check `dl`: Dixmier-Lister central scalars (`prop:dl-central-scalars`) and the sentences citing it

Checker id `dl`, 9 Nov 2026. This is an independent pass. I read the earlier reports only after my own pass was complete (see the last section).

**Scope.**
- `T/main.tex` lines 446-492: the bracket table, the derivation paragraph, `prop:dl-central-scalars` with its proof, and the finite-check paragraphs.
- The sentences that cite the proposition: the abstract (l.88), the intro item (1) (l.116) and Contributions (1) (l.254). For terminology I also read the intro item (2) (l.117) and the related-work paragraph (l.120).
- `T/appendix-provenance.tex` items `prov:cover-dl` and `prov:dl-central-scalars` (l.21-26).
- The macros `\Dl*` in `T/numbers.tex`.

**Files and shasums.**
- `main.tex` `0ed1a1f82b13fef77fc94a48e35efc93f8d23ee4`
- `appendix-provenance.tex` `2545e44aeb3ff7f97a204932c46f20ac8c77ec62`
- `numbers.tex` `c7e587fbc60d3c4a24b95db17c69f8537aefef92`

**Verdict: MINOR ONLY.** The proposition is true as stated and its proof is complete, apart from two clauses that should be written out (finding 2). One sentence that cites the proposition, Contributions (1) at l.254, is false under the paper's own meaning of "central scalars" (finding 1, ERROR). That sentence states no result, and no stated result depends on it.

## Findings

### 1. ERROR: main.tex:254, Contributions (1), citing `prop:dl-central-scalars`

The sentence reads: "for the Dixmier--Lister algebra no automorphism of $G$ supplies central scalars beyond $\pm1$".

The paper's own usage, in intro item (2) at l.117, is that character alignment uses automorphisms that "act on a central subgroup by known scalars". In that sense the sentence is false whenever $p \equiv 1 \pmod 3$.

**Counterexample.** Let $\omega$ be a primitive cube root of unity. The diagonal map
- $e_1, e_4 \mapsto \omega^2\cdot$,
- $e_2, e_3 \mapsto \omega\cdot$,
- $e_5, e_6$ fixed,
- $e_7 \mapsto \omega e_7$, $e_8 \mapsto \omega^2 e_8$

preserves all ten brackets. It is a $\mathbb{Z}/3$-grading of $\mathcal{L}_{\mathrm{DL}}$, checked over $\mathbb{Z}[\omega]$ in `dl/dl_symbolic.py`.

So for $p \equiv 1 \pmod 3$ it is an automorphism of $G = \exp(\mathcal{L}_{\mathrm{DL}} \otimes \Fp)$. It acts on the central subgroup $\exp(\Fp e_7)$ by $z \mapsto z^\omega$. Composed with the paper's sign automorphism it acts by $z^{-\omega^2}$, where $-\omega^2$ is a primitive sixth root of unity.

At $p = 7$ the map $e_1, e_4 \mapsto 4\cdot$, $e_2, e_3 \mapsto 2\cdot$, $e_7 \mapsto 2e_7$, $e_8 \mapsto 4e_8$ acts on $\exp(\mathbb{F}_7 e_7)$ by $z \mapsto z^2$, and its composite with the sign map by $z \mapsto z^5$.

My own $\mathbb{F}_7$-rational computation of the image on the centre (`dl/rat_p7.out`) contains $\mathrm{diag}(2,4)$, $\mathrm{diag}(4,2)$, $\mathrm{diag}(3,5)$ and $\mathrm{diag}(5,3)$. The provenance item calls this image $D_{12}$. It is the dihedral group of order 12, and its rotations of order 3 and 6 have these eigenvalues.

Over $\bar{\mathbb{F}}_p$ the eigenvalues of automorphisms on the centre are exactly the sixth roots of unity for $p = 5, 7, 11, 13, 32003$ (finite computation, `dl/g_p*.out`). So only finitely many scalars occur on central lines, and the family $\theta^3$ remains unavailable. The narrative conclusion survives; the sentence as written does not.

Read literally as "acts on the centre by a scalar", the sentence is just the proposition. The abstract (l.88) and the intro (l.116) do say exactly that and are correct.

**Fix.** Replace the sentence with: "and for the Dixmier--Lister algebra no automorphism of $G$ acts on the centre of $G$ by a scalar other than $\pm1$ (Proposition~\ref{prop:dl-central-scalars})."

Optionally add after l.489: "The proposition concerns scalar action on the whole centre. On a central line more scalars occur: for $p\equiv1\pmod 3$ the $\mathbb{Z}/3$-grading ($e_1,e_4$ of weight $\omega^2$, $e_2,e_3$ of weight $\omega$, $e_5,e_6$ of weight $1$, $e_7$ of weight $\omega$, $e_8$ of weight $\omega^2$) is an automorphism acting on $\exp(\Fp e_7)$ by a primitive cube root of unity; in the finite computations only sixth roots of unity occur as eigenvalues on the centre, so the scalars $\theta^3$ are still unavailable."

### 2. MINOR: main.tex:480, proof of `prop:dl-central-scalars`, the rank-one step

The property "$([x,\mathcal{L}]+\gamma_3)/\gamma_3$ is one-dimensional" is stated for $x \in U$, but it is applied to $\phi(x) = Ax + b(x) + z(x) \notin U$. Two facts are used silently:

- **(a)** The dimension depends only on $x \bmod \gamma_2$, because $[\gamma_2,\mathcal{L}] \subseteq \gamma_3$.
- **(b)** "$A$ maps $U_+ \cup U_-$ into itself" implies "preserves or exchanges". This needs:
  - a subspace inside a union of two subspaces lies in one of them;
  - $A$ is injective, so $A(U_+) \ne A(U_-)$.

Both are true, and I checked them. The locus is exactly $P(U_+) \cup P(U_-)$ over $\mathbb{F}_9$ (characteristic 3), $\mathbb{F}_5$, $\mathbb{F}_{13}$ and $\mathbb{F}_{49}$, and adding $\gamma_2$-parts to $x$ never changes the rank (`dl/rank_one_locus.out`).

**Fix.** After "...$(U_+\cup U_-)\setminus\{0\}$;" insert: "since $[\gamma_2,\mathcal{L}_{\mathrm{DL}}]\subseteq\gamma_3$, the same holds for every $x\in\mathcal{L}_{\mathrm{DL}}$ with $x\bmod\gamma_2$ in place of $x$. This property is preserved by $\phi$, so $A$ maps $U_+\cup U_-$ into itself; a subspace contained in the union of two subspaces lies in one of them, and $A(U_+)\cap A(U_-)=0$, so $A$ preserves or exchanges $U_+$ and $U_-$."

### 3. MINOR: main.tex:88, abstract

The abstract says the algebra has "only nilpotent derivations and admit[s] no positive grading" with no field stated.

This is true over $\mathbb{Q}$ and over $\Fp$ for $p>3$. The first half fails in characteristic 3: $\dim\mathrm{Der}(\mathcal{L}_{\mathrm{DL}}\otimes\mathbb{F}_3)=16$, and 176 of 200 random derivations over $\mathbb{F}_3$ are not nilpotent (`dl/derivations.out`). So the non-grading argument does not apply there; I did not determine whether a positive grading exists in characteristic 3. Line 116 has the qualifier "over $\Fp$ for $p>3$". The context ($c=3<p$) arguably supplies it.

**Fix (optional).** Write "...admit no positive grading over $\Fp$ for $p>3$;".

### 4. MINOR: main.tex:489, "act on the top grade"

$G$ is not graded. The intended object is $\gamma_3(\mathcal{L}_{\mathrm{DL}}) = Z(\mathcal{L}_{\mathrm{DL}})$, which is $E_s(\A_3)$.

**Fix.** Replace with: "...no automorphism of $G$ can act on $\gamma_3(\mathcal{L}_{\mathrm{DL}})$ as a dilation $\delta_\theta$ acts on the top grade $\A_3$, by $\theta^3$, once $\theta^3\ne\pm1$". The qualifier "once $\theta^3\ne\pm1$" is correct and needed: the sign map acts as $\delta_{-1}$ would.

### 5. MINOR: main.tex:465 and 469, statement and first line of the proof

- In the statement, "its centre $\gamma_3(\mathcal{L}_{\mathrm{DL}})=\Span(e_7,e_8)$" should be $\Span_K(e_7,e_8)$.
- "The Lazard group $\exp(\mathcal{L}_{\mathrm{DL}})$ over $\Fp$" should be $\exp(\mathcal{L}_{\mathrm{DL}}\otimes\Fp)$.
- "$\zeta\ne\pm1$" should be "$\zeta\not\equiv\pm1 \pmod p$".
- "We may assume $K$ algebraically closed" deserves one clause: an automorphism over $K$ extends to $\bar K$ with the same action on the centre, which is $\Span(e_7,e_8)$ over every field; the converse maps are defined over $\mathbb{Z}$.

The reduction itself is correct; the conclusion is a condition on $\zeta$, so it descends trivially.

### 6. MINOR (suggested improvement; the current text is correct): main.tex:454 and 461, derivation rank

The $224\times64$ integer system has rank 52 over $\mathbb{Q}$, and its nonzero elementary divisors are exactly $\{1,3,6\}$ (`dl/derivations.out`). So it has rank 52 modulo every prime $p>3$, and $\mathrm{Der}(\mathcal{L}_{\mathrm{DL}}\otimes\Fp)$ is the reduction of the paper's 12-parameter family. That family spans a saturated lattice: each parameter has its own $\pm1$ pivot entry.

This proves the "every $p>3$" claim directly, without the row certificates in the JSON (which I did not read). It also shows that the finite range $5\le p\le23$ is not needed.

**Fix (optional).** Replace "has rank $52=64-12$ modulo every prime $5\le p\le23$ (a finite computation; the row certificates cover every $p>\DlBaseClass$)" with "has nonzero elementary divisors $1$, $3$ and $6$, hence rank $52=64-12$ modulo every prime $p>\DlBaseClass$".

## Checked and correct

- **Bracket table.**
  - Jacobi holds over $\mathbb{Z}$ on all 56 basis triples.
  - $\dim(\gamma_2,\gamma_3,\gamma_4,Z)=(4,2,0,2)$ over $\mathbb{Q}$ and over $\mathbb{F}_p$ for $p=3,5,7,11,13$.
  - $\gamma_2=\Span(e_5..e_8)$, $\gamma_3=Z=\Span(e_7,e_8)$ and $[\gamma_2,\gamma_2]=0$, in every characteristic.
  - Script: `dl/dl_symbolic.py`.
- **Derivation paragraph** (l.454-461).
  - The system has 224 equations in 64 variables (138 nonzero rows) and rank 52 over $\mathbb{Q}$.
  - The paper's 12-parameter family satisfies the system and equals the full kernel over $\mathbb{Q}$.
  - The rank is 52 modulo all 15 primes $5\le p\le59$; the dimension of $\mathrm{Der}$ is 14 at $p=2$ and 16 at $p=3$.
  - $D(\mathcal{L})\subseteq\gamma_2$ implies $D^3=0$; checked by hand.
  - The grading argument (dividing the degrees by their gcd gives a non-nilpotent degree derivation) is correct; checked by hand.
  - Script: `dl/derivations.sage`.
- **Proposition proof, line by line, by hand and by machine.**
  - Centre: correct.
  - Change of basis: determinant $8i$, invertible exactly when $2\ne0$.
  - New-basis table: all 28 brackets in the new basis recomputed over $\mathbb{Z}[i]$ agree with the proof, including every zero bracket and $[v_+,v_-]=0$. The 15 displayed identities also hold in $\mathbb{F}_p[i]$ for $p=3,5,7,11,13$.
  - Shape of $\phi$: $[\phi x,\phi v]=[Ax,Mv]$ and $[\phi x,\phi y]\equiv[Ax,Ay]$; correct, with the complement handled by $b$ and $z$.
  - $\psi_\pm$ matrices and the two maps of determinant $-1$: correct.
  - Keep case: $Mv_+=\det(P)v_+$, $P=\mu\,\mathrm{id}$ with $\mu^3=\zeta$, the $e_7$-coefficient (the corrections lie in $Ke_8$ because $[u_1,v_-]=[u_3,v_+]=0$), and $\zeta=\mu\nu$ forcing $\zeta=1$: correct.
  - Swap case: $\alpha^3=\beta^3=-\zeta$ and $\zeta=-\alpha\beta$ forcing $\zeta=-1$: correct.
  - Sign automorphism: correct.
  - Lazard transfer for $p>3$: correct.
  - Characteristic 3: nothing in the proof divides by 3, and the Gröbner check at $p=3$ also gives scalars $\{\pm1\}$.
- **Finite-check paragraph** (l.489). My counts are independent of GAP:
  - The gauge-fixed component variety has 4 $\mathbb{F}_5$-points and 12 $\mathbb{F}_7$-points.
  - With the free 12-dimensional unipotent fibre (4 gauge parameters $\lambda,\mu,\nu,\rho$ plus 8 central coordinates), this gives $|\mathrm{Aut}|=4\cdot5^{12}$ and $12\cdot7^{12}$.
  - The $\mathbb{F}_p$-rational image on the centre has order 4 ($\{\pm I,\pm\tau\}$, with $\tau$ swapping $e_7\leftrightarrow-e_8$) and order 12.
  - The only scalars in each image are $\pm1$.
  - Scripts: `dl/rat_p5.out`, `dl/rat_p7.out`.
- **Arithmetic of l.491.** $\binom{14}{2}=91$, $3\cdot91=273$, $\binom{56}{2}\cdot3=4620$, $4\cdot8=32$, $4\cdot14=56$. I did not rerun the replay itself; it checks an identity proved in `thm:rees-cover`.
- **Citing sentences.** Abstract l.88 and intro l.116 match the proposition exactly. For Contributions l.254, see finding 1.

**Independent finite evidence** (my own Singular elimination; `dl/gen_gauge_ideal.py`). The setup:
- A block form of $\phi$ on $V\oplus W\oplus Z$, with the induced maps on $W$ and $Z$ and the $Z$-parts substituted.
- The gauge $Be_1=Be_2=0$. It is valid because $\exp(D)=1+D+D^2/2$ is an automorphism for every $D$ in the paper's $(\lambda,\mu,\nu,\rho)$ family in characteristic $\ne2$.

Results over $\bar{\mathbb{F}}_p$:

| p | component variety | image on the centre | scalars | eigenvalues on the centre |
|---|---|---|---|---|
| 3 | dim 2 | positive-dimensional (preserves $K(e_7-e_8)$) | $\pm1$ | all of $\bar{\mathbb{F}}_3^\times$ |
| 5, 7, 11, 13, 32003 | 36 reduced points | 12 points (dihedral) | $\pm1$ | exactly the sixth roots of unity |

## Not checked / UNKNOWN

- Characteristic 0 elimination timed out (217 s CPU): UNKNOWN. Only the proof and the $p=32003$ proxy cover it.
- Two earlier formulations at $p=5$ (eliminating all variables except $\zeta$; the block form without gauge) timed out: UNKNOWN.
- The rational count at $p=13$ timed out; $p=11$ was not run. My predictions from the structure, not computed: $12\cdot11^{12}$ and $36\cdot13^{12}$.
- I did not open the JSON row certificates (`research/reductions/rees_nongradable_control.json`); finding 6 replaces them.
- Compute used: about 18 core-minutes.

## For the human expert

- Check the bracket table against Dixmier-Lister (1957). From memory it matches the usual form, but this was not checked against the paper (no network).
- Is "acts on the centre by a scalar" the right barrier notion?
  - It is the exact analogue of $\delta_\theta$ on $\A_3$, and the proposition is sharp for it.
  - For alignment on a smaller central subgroup, automorphisms of $G$ do supply sixth roots of unity (finding 1), but apparently only finitely many scalars.
  - Whether any text should claim more than the whole-centre statement is an editorial choice.
- Characteristic 3 behaves differently, although the paper never uses $p=3$ for groups: there are non-nilpotent derivations and a positive-dimensional image on the centre. The proposition still holds there.

## Comparison with the earlier reports

**Referee report, DL part (`R/research/audits/reviews/2026-11-09-rees-dl-scalars-schedule2-referee.md`).**
- It rates the proposition CORRECT. I agree.
- Its gap W1 (missing "$\theta^3\ne\pm1$") is fixed in `main.tex` l.489, and in the core per `diffs/patch9nov-core_main-core.tex.diff`.
- Its gap W2 was applied as "supplies central scalars beyond $\pm1$". I consider that fix insufficient (finding 1). The referee's side remark anticipated the issue ("would need the image group ... and its eigenvalues"), but did not notice that the order-12 image at $p=7$ already has eigenvalues other than $\pm1$.
- Its scalar sets for $p=3,5,7,11$ agree with mine. I add $p=13$ and $p=32003$, the image and eigenvalue structure, and an independent recount of $4\cdot5^{12}$ and $12\cdot7^{12}$, which the referee could not obtain.
- The referee also used a gauge, setting the $e_5,e_6$-parts of $\phi(e_1),\phi(e_2)$ to zero. This is the same gauge as mine, found independently.

**Author's folder (`R/research/audits/reviews/2026-11-09-rees-dl-central-scalars/`), outputs only.**
- `split_check.out` and the GAP outputs at $p=5,7$ (orders, $C_2\times C_2$, the order-12 group) agree with my computations.
- `brute_p3.out` (12 central actions over $\mathbb{F}_3$, scalars $\pm1$) is consistent with my $\bar{\mathbb{F}}_3$ result.
- The GAP run at $p=11$ timed out, as recorded.
