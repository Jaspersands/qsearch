# Rees paper: the chart-cost lemma for prop:black-box (iv)

Date: 2026-11-03/04. AI session (Claude). Nothing here has been reviewed by a human.
Scope: Proposition `prop:black-box` item (iv) ("Chart cost") of
`docs/papers/rees-hsp/main.tex` and the paragraph "Chart arithmetic at cost linear
in $d$" (argued) in route (R2) of `docs/papers/rees-hsp/appendix-torsion-blackbox.tex`
(about line 815), as requested by Referee 2, Section 2.4
(`research/audits/reviews/2026-11-03-rees-referee-2.md`).

Files read: `main.tex` (lines 740-790: the paragraph before the proposition,
`prop:black-box`, `thm:bb-envelope`), `appendix-torsion-blackbox.tex` (the header
comments, "Free objects", the Setting and (M1)-(M3) of `app:tb-ring`, `lem:tb-words`,
`lem:tb-evaluation`, the proof of (i), `lem:tb-kernel`, the proof of (ii) with routes
(R1)-(R2)), `research/audits/reviews/2026-11-02-rees-bb-envelope.md` Section 2.4
(the source of item (iv)), `research/STATE.md` and `research/TRAPS.md` (skimmed).
Script and output: `research/audits/reviews/2026-11-03-rees-chart-lemma/check_chart_lemma.py`
(run with `/opt/anaconda3/bin/python`; prints `ALL PASSED`).

Labels used below: proved = a complete argument is given here; exact computation =
checked by the script on the stated cases; argued = plausible, no complete argument.

## 1. Verdict in one paragraph

The argued paragraph is correct as mathematics and becomes a lemma with a complete
proof (Section 5 below, proposed LaTeX in Section 9). The count $O_c(dk^2 + k^4)$
ring operations modulo $M = p^e$ is proved, with every operation named. No step
needs an extra hypothesis and no counterexample exists to the operation count. Four
defects of wording were found, none of which is a refutation: (G1) the $\ell$-only
form $O_c(s^c\ell^3 + \ell^4)$ in `prop:black-box`(iv) drops the $\eps$-dependence of
$k$ and holds only when $\log_2(8\ell/\eps) \le \ell$, or more generally when
$k = O(\ell)$; (G2) the paragraph counts the Howell membership tests ($O(k^2)$ each)
but not the Howell-form updates after each kept column ($O(k^3)$ each, at most $n$ of
them, absorbed in $k^4$); (G3) the sentence "By (M1) with $S = F$ and the ideal
$\ker\pi$, present $\mathcal{L}_G$" in (R2) describes a $\poly(d)$ step (a $d\times d$
Smith form), which contradicts "linear in $d$"; the lemma replaces it; (G4) the table
lookups and word-dictionary operations are not ring operations and must be counted
separately ($O_c(d + k^2)$ of them, each $O(c\log s)$ bit operations). The sharper
bound $O_c(s^c\ell^2 + \ell^4)$ holds under the hypothesis of (G1).

## 2. The claim as stated

`prop:black-box`(iv): with $k = \lfloor\ell/\log_2 p\rfloor + \lceil\log_p(8\ell/\eps)\rceil$
samples, "Howell and Smith normal forms over $\mathbb{Z}/M\mathbb{Z}$ then give the
explicit chart $F_{s,c}/\ker\pi \cong \log G$, with structure constants, in
$O_c(s^c\ell^3 + \ell^4)$ ring operations (argued in Appendix D, route (R2), at
$O_c(dk^2 + k^4)$)."

The appendix paragraph asserts: (P1) in a Lyndon basis the expansion of $[w_a,w_b]$
lies in the span of the at most $c!$ basis elements of multidegree
$\mu(a)+\mu(b)$ and is read from a table depending only on $c$; (P2) $u \mapsto Yu$
induces $F/\ker\pi \cong A = YF$; (P3) a column scan against a Howell form, $O(k^2)$
per test, keeps at most $n = \log_p|G|$ columns which generate $A$, and the mod-$p$
test is not enough ($C_9\times C_3$); (P4) a Smith form of the $k\times n$ matrix of
kept columns presents $\mathcal{L}_G$ with a basis supported on kept indices; (P5) the
structure constants come from $O_c(n^2)$ products $Y[w_a,w_b]$ and two contractions;
(P6) the images $\Phi(\varepsilon_i)$ cost $n(2b_e + m_+ + 2b_eq_+)$ multiplications
each; (P7) the total is $O_c(dk^2 + k^4)$ ring operations and
$n^2(2b_e + m_+ + 2b_eq_+)$ multiplications.

## 3. Cost model (proved)

**Definition.** A *ring operation modulo $M = p^e$* ($p$ known) is one of: addition,
subtraction or multiplication of residues; computing the $p$-adic valuation
$v_p(a) \in \{0,\dots,e\}$ of a residue together with its unit part $a/p^{v_p(a)}$;
exact division $a \mapsto a/p^v$ for $p^v \mid a$ (the result is defined modulo
$p^{e-v}$; any lift to $\mathbb{Z}/M$ is accepted, see Section 5.3 for why this is
harmless); inversion of a unit.

**Claim.** Each ring operation costs $O(b_e^2)$ bit operations, $b_e = \lceil\log_2(p^e+1)\rceil$.
*Proof.* Schoolbook arithmetic for $+,-,\times$ and reduction modulo $M$; the
extended Euclidean algorithm on $b_e$-bit integers for a unit inverse; at most $e$
trial divisions by $p$ for the valuation, each $O(b_e\log_2 p)$ bit operations, and
$e\log_2 p \le b_e$. (proved)

The envelope note states "each $O(b_M^2)$ bit operations" for the same model, so the
bit-operation line of `thm:bb-envelope`(iii) is unaffected (Section 7).

## 4. Preliminaries checked

### 4.1 The Lyndon basis (proved; exact computation for $c \le 5$, $s \le 5$ as listed)

Let $X = \{X_1 < \dots < X_s\}$. A word $w$ over $X$ is Lyndon if it is strictly
smaller, in lexicographic order, than each of its proper suffixes. Every Lyndon word
$w$ of length at least two has a standard factorisation $w = uv$ with $v$ its longest
proper Lyndon suffix; then $u$ is Lyndon, and the standard bracketing is
$b(w) = [b(u),b(v)]$, $b(X_i) = X_i$. The bracketings $b(w)$ of the Lyndon words of
length at most $c$ form a $\mathbb{Z}$-basis of the free nilpotent Lie ring of class
$c$ (Reutenauer, *Free Lie Algebras*, Chapter 5; the Lyndon words form a Hall set, so
this is the Hall-basis statement the appendix already uses). Ordered by length and
then lexicographically, the basis begins $w_1 = X_1,\dots,w_s = X_s$ and each
$w_j = [w_{j'},w_{j''}]$ with $j',j'' < j$, as the proof of part (i) requires.

(L1) *Multihomogeneity.* The free Lie ring is graded by $\mathbb{N}^s$ (the content
$\mu(w)$, counting letters), the bracket is additive on contents, and each $b(w)$ is
homogeneous of content $\mu(w)$. Hence $[b(u),b(v)]$ is homogeneous of content
$\mu(u)+\mu(v)$ and lies in the span of the basis elements of that content, or is
$0$ in $F_{s,c}$ when $|\mu(u)|+|\mu(v)| > c$. (proved)

(L2) *At most $(m-1)!$ basis elements per content.* Fix a content $\alpha$ with
$|\alpha| = m \le c$. A Lyndon word is primitive, its $m$ rotations are distinct
words of content $\alpha$, and each rotation class of a primitive word contains
exactly one Lyndon word (its minimum). So the number of Lyndon words of content
$\alpha$ is at most $\binom{m}{\alpha}/m \le m!/m = (m-1)!$, with equality at
$\alpha = (1,\dots,1)$. The paper's "$c!$" is therefore true and $(c-1)!$ is the
exact maximum over contents of length at most $c$. (proved; exact computation: the
counts are $1,1,2,6$ at $c = 1,2,3,4$ with $s \ge c$ letters, attained at content
$(1,\dots,1)$; the bracket of two basis elements touched at most $3$ basis elements
in every case computed, $c \le 5$.)

(L3) *One table for all $s$.* Let $T_c$ be the table whose entry at a pair $(u,v)$
of Lyndon words over the alphabet $\{1 < \dots < c\}$ with $|u|+|v| \le c$ is the
Lyndon-basis expansion of $[b(u),b(v)]$ in the free nilpotent Lie ring of class $c$
on $c$ generators, an integer vector with at most $(c-1)!$ entries. $T_c$ is finite
and depends only on $c$. For basis elements $w_a, w_b$ of $F_{s,c}$ with
$|w_a|+|w_b| \le c$, let $X' \subseteq X$ be the set of letters occurring in them,
$t = |X'| \le c$, and $\rho : X' \to \{1,\dots,t\}$ the order-preserving bijection.
Whether a word is Lyndon, and its standard factorisation, depend only on the relative
order of its letters, so $\rho$ maps the Lyndon words over $X'$ bijectively onto the
Lyndon words over $\{1,\dots,t\}$ and commutes with $b$. The Lie ring map
$\rho_* : \Lambda(X') \to \Lambda(\{1,\dots,c\})$ induced by $\rho$ is an isomorphism
onto the free Lie ring on $\{1,\dots,t\}$, and the inclusion
$\Lambda(X') \subseteq \Lambda(X)$ maps the Lyndon basis of $\Lambda(X')$ onto the
basis elements of $\Lambda(X)$ whose letters lie in $X'$ (the same words). Applying
$\rho_*^{-1}$ and then the inclusion to the identity recorded in $T_c$ gives
$[w_a,w_b] = \sum_w T_c(\rho w_a,\rho w_b)_w\, b(\rho^{-1}w)$ in $F_{s,c}$. (proved;
exact computation: for $c \le 4$ and $s \le 3$ every bracket expansion in $F_{s,c}$
agrees with the relabelled entry of $T_c$, with integer coefficients.)

Computing $T_c$ once costs $O_c(1)$ integer operations (expand the standard
bracketings in the truncated free associative algebra on $c$ letters and extract the
Lyndon coordinates triangularly: $b(w) = w + $ words larger than $w$, Reutenauer
Theorem 5.1); reducing it modulo $M$ costs $O_c(1)$ ring operations.

### 4.2 Duality in $(\mathbb{Z}/M)^d$ (proved)

For a subgroup $B \le (\mathbb{Z}/M)^d$, with
$B^\perp = \{a : a\cdot u \equiv 0 \ \forall u \in B\}$, one has $B^{\perp\perp} = B$:
the pairing $a \mapsto (u \mapsto \zeta_M^{a\cdot u})$ identifies $(\mathbb{Z}/M)^d$
with its character group, under which $B^\perp$ is the annihilator of $B$, that is,
the character group of $(\mathbb{Z}/M)^d/B$, of order $M^d/|B|$. So
$|B^{\perp\perp}| = |B|$ and $B \subseteq B^{\perp\perp}$. Consequently, if the rows
$a_1,\dots,a_k$ of $Y$ generate $(\ker\pi)^\perp$, then
$\ker Y = \{u : a_i\cdot u = 0\ \forall i\} = (\ker\pi)^{\perp\perp} = \ker\pi$.

## 5. The steps, checked

Throughout, assume the success event of `lem:tb-kernel`: the rows of $Y \in (\mathbb{Z}/M)^{k\times d}$
generate $(\ker\pi)^\perp$. Write $n = \log_p|G|$ and note $n \le \lfloor\ell/\log_2 p\rfloor \le k$
because the encodings are unique.

### 5.1 $F/\ker\pi \cong A$ (P2: proved)

By 4.2, $\ker Y = \ker\pi$, so $u \mapsto Yu$ induces an additive isomorphism
$F/\ker\pi \to A \coloneqq YF$, the column module of $Y$ in $(\mathbb{Z}/M)^k$. Since
$\ker\pi$ is an ideal, $[Yu,Yv] \coloneqq Y[u,v]$ is well defined and makes this a
Lie ring isomorphism. In particular $|A| = |F/\ker\pi| = |\pi(F)| = |G| = p^n$.

### 5.2 Howell forms over $\mathbb{Z}/p^e$ (P3, the test: proved; exact computation)

**Definition.** A sequence $r_1,\dots,r_m$ of nonzero vectors in $(\mathbb{Z}/M)^k$ is
in *Howell form* if (H1) the leading positions $j_1 < \dots < j_m$ are strictly
increasing and the leading entries are $p^{a_1},\dots,p^{a_m}$ with $0 \le a_t < e$;
(H2) for every $t$, $p^{e-a_t}r_t \in \langle r_{t+1},\dots,r_m\rangle$. Then $m \le k$.

**Membership test.** Given $v$, for $j = 1,\dots,k$: if $v_j \ne 0$ then, if $j = j_t$
for some $t$ and $p^{a_t} \mid v_j$, replace $v$ by $v - (v_j/p^{a_t})r_t$; otherwise
report $v \notin S$. At the end report $v \in S$ iff $v = 0$. Cost: at most $m \le k$
reductions, each one exact division and $k$ multiplications and subtractions, so at
most $k(2k+1) = O(k^2)$ ring operations.

*Correctness.* Reductions preserve the coset $v + S$, so "accept" implies $v \in S$.
Conversely let $S_t = \langle r_t,\dots,r_m\rangle$ and suppose $v \in S_t$ when the
scan reaches position $j_t$ (true at $t = 1$ with $S_1 = S$). Then $v$ vanishes
before $j_t$, and $v = \sum_{i\ge t}\lambda_ir_i$ gives $v_{j_t} = \lambda_tp^{a_t}$,
so $p^{a_t} \mid v_{j_t}$. Any lift $\lambda_t'$ of $v_{j_t}/p^{a_t}$ satisfies
$\lambda_t' \equiv \lambda_t \pmod{p^{e-a_t}}$, hence
$v - \lambda_t'r_t = \sum_{i>t}\lambda_ir_i + (\lambda_t-\lambda_t')r_t \in S_{t+1}$ by
(H2). If $v_{j_t} = 0$ the same holds with $\lambda_t' = 0$. Positions strictly
between pivots are zero on $S_{t}$, so the scan never rejects an element of $S$, and
at the end $v \in S_{m+1} = 0$.

**Construction.** Given generators $g_1,\dots,g_q$ of $S$: for $j = 1,\dots,k$, among
the remaining vectors pick one whose entry in position $j$ has minimal valuation
$a < e$ (if all are divisible by $p^e$, that is zero, continue); multiply it by the
inverse of the unit part so that its entry is $p^a$; call it the pivot row for $j$ and
remove it from the remaining set. Every other remaining vector $r$ has $p^a \mid r_j$;
replace it by $r - (r_j/p^a)\cdot\text{pivot}$. Finally append $p^{e-a}\cdot\text{pivot}$
to the remaining set. *Correctness:* the span of (pivot rows so far) $\cup$ (remaining)
is $S$ at all times, since every operation is an invertible row operation or the
appending of an element already in the span; at the end the remaining set is empty
and the pivot rows generate $S$. (H1) holds because remaining vectors are zero in all
earlier positions (zero columns stay zero under the operations used). (H2): with
$R_t$ the remaining set right after the pivot for $j_t$ is fixed, each later step
replaces $R$ by $R'$ with $\langle R\rangle = \langle r_{\text{new}}\rangle + \langle R'\rangle$,
so by induction $\langle R_t\rangle = \langle r_{t+1},\dots,r_m\rangle$, and
$p^{e-a_t}r_t \in R_t$. *Cost:* at most $k$ vectors are appended, so at most $q+k$
vectors are ever processed; per position, $O(q+k)$ valuations and $O((q+k)k)$
operations for elimination; in all $O((q+k)k^2)$ ring operations. With $q \le k+1$
generators this is $O(k^3)$.

(Exact computation: on 60 random modules in $(\mathbb{Z}/p^e)^k$, $p \in \{2,3,5\}$,
$e \le 3$, $k \le 3$, the computed form satisfies (H1), (H2), spans the input module,
and the membership test agrees with brute-force membership on every vector.)

Literature: Howell, *Linear and Multilinear Algebra* 1986; Storjohann and Mulders, ESA 1998, give
the general-$N$ theory and faster algorithms; the proof above is self-contained for
$N = p^e$ and is all the lemma needs.

### 5.3 The column scan (P3: proved; exact computation)

Scan $j = 1,\dots,d$; keep $j$ iff $Yw_j \notin \langle Yw_i : i \text{ kept}, i < j\rangle$,
decided by the membership test against the current Howell form; after keeping $j$,
recompute the Howell form of the kept columns. Let $J$ be the kept set, $r = |J|$.

*Kept columns generate $A$:* by induction, $\langle Yw_i : i\in J, i \le j\rangle = \langle Yw_1,\dots,Yw_j\rangle$
for every $j$; at $j = d$ this is $A$. *At most $n$ kept:* each kept column strictly
enlarges a subgroup of the $p$-group $A$, multiplying its order by at least $p$, and
$|A| = p^n$; so $r \le n \le k$. *Cost:* $d$ membership tests at $O(k^2)$ and at most
$n \le k$ Howell constructions of at most $k+1$ generators at $O(k^3)$: in all
$O(dk^2 + k^4)$ ring operations. (G2) The paragraph states only the test cost; the
construction cost is what forces the $k^4$ term here, and it is within the claimed
total.

*Why not mod $p$:* for $A$ the image of $Z/9 \oplus Z/3$ the second column of every
sample is divisible by $3$ (exact computation: a sample run gave column
$(3,0,0,0,0,3)$), yet it is not in the $\mathbb{Z}/9$-span of the first column; the
kernel of reduction modulo $p$ of $A$ is not zero, so a mod-$p$ independence test
would discard a needed generator. The paper's remark is correct.

*Any lift of an exact quotient is harmless:* in both the test and the construction,
different lifts of $v_j/p^a$ differ by multiples of $p^{e-a}$, and $p^{e-a}\cdot\text{pivot}$
lies in the module in question; the cosets and spans computed do not depend on the lift.

### 5.4 Smith form of the kept columns (P4: proved; exact computation)

Let $C \in (\mathbb{Z}/M)^{k\times r}$ have the kept columns. *Algorithm:* for
$t = 1,2,\dots$: find an entry of minimal valuation $a_t$ in rows and columns $\ge t$
(stop if all are zero); permute it to $(t,t)$; scale row $t$ by the inverse of its
unit part so $C_{tt} = p^{a_t}$; all other entries in row $t$ and column $t$ are
multiples of $p^{a_t}$, so clear column $t$ by row operations and then row $t$ by
column operations (which now change only row $t$); record the row operations in
$P \in \mathrm{GL}_k(\mathbb{Z}/M)$ and the column operations in
$Q \in \mathrm{GL}_r(\mathbb{Z}/M)$. Result: $PCQ = D = \diag(p^{a_1},\dots,p^{a_r})$
padded with zeros, with $a_1 \le a_2 \le \dots$ (valuations of successive global
minima are non-decreasing, since elimination never lowers valuations below the
current minimum). Let $I = \{i \le r : a_i < e\}$ and $m = |I|$; for $i \notin I$ the
entry is $0$.

*Cost:* each of at most $r$ steps costs $O(kr)$ valuations, $O(kr)$ operations on $C$,
$O(k^2)$ on $P$ and $O(r^2)$ on $Q$; in all $O(k^2r) \le O(k^3)$ ring operations since
$r \le k$. (Exact computation: on 60 random $k\times r$ matrices, $k,r \le 4$, the
output satisfies $PCQ = D$ exactly with $P, Q$ unimodular and the divisibility chain.)

*Chart basis.* Put $\varepsilon_i = CQe_i \in A$ and
$\tilde\varepsilon_i = \sum_{a=1}^r Q_{ai}w_{\kappa_a} \in F$ for $i \in I$, where
$\kappa_1 < \dots < \kappa_r$ enumerate $J$; then $Y\tilde\varepsilon_i = \varepsilon_i$ and
$\tilde\varepsilon_i$ is supported on $J$. Since $P$ is an automorphism of
$(\mathbb{Z}/M)^k$ and $Q$ of $(\mathbb{Z}/M)^r$,
$PA = P\cdot\mathrm{col}(C) = \mathrm{col}(PCQ) = \bigoplus_{i\in I}p^{a_i}(\mathbb{Z}/M)e_i$,
a direct sum of cyclic groups of orders $p^{e-a_i}$. Pulling back by $P^{-1}$ and
using $P^{-1}p^{a_i}e_i = P^{-1}De_i = CQe_i = \varepsilon_i$,
$$A = \bigoplus_{i\in I}(\mathbb{Z}/p^{e_i})\varepsilon_i,\qquad e_i \coloneqq e - a_i \in \{1,\dots,e\},\qquad \textstyle\sum_{i\in I}e_i = \log_p|A| = n .$$
Computing the $\varepsilon_i$ costs $O(kr^2)$ ring operations (or read them off as the
nonzero columns of $CQ$). The number $m$ of cyclic factors may be smaller than $r$
(exact computation: $\mathbb{Z}/27$ generated by $3$ and $1$ keeps $2$ columns and
has $m = 1$).

*Coordinates.* For $v \in A$, $v = \sum_{i\in I}t_i\varepsilon_i$ iff
$Pv = \sum_{i\in I}t_ip^{a_i}e_i$, so $t_i = (Pv)_i/p^{a_i} \bmod p^{e_i}$, an exact
division; the rows of $Pv$ outside $I$ vanish on $A$. Cost: $O(k^2)$ ring operations
per vector.

### 5.5 Structure constants (P5: proved)

$[\varepsilon_i,\varepsilon_j]_A = Y[\tilde\varepsilon_i,\tilde\varepsilon_j]
= \sum_{a,b\le r}Q_{ai}Q_{bj}\,z_{ab}$ with $z_{ab} \coloneqq Y[w_{\kappa_a},w_{\kappa_b}]$.
By (L1)-(L3), $[w_{\kappa_a},w_{\kappa_b}]$ has at most $(c-1)!$ nonzero Lyndon
coordinates, read from $T_c$ after relabelling; so each $z_{ab}$ is a combination of
at most $(c-1)!$ columns of $Y$ and costs $O_c(k)$ ring operations and $O_c(1)$
dictionary lookups (the column index of a word of length at most $c$). All $r^2$ of
them: $O_c(r^2k)$. Then two contractions, $u_{ib} = \sum_aQ_{ai}z_{ab}$ and
$\sum_bQ_{bj}u_{ib}$, cost $O(r^3k)$ each, and the coordinates of the $m^2$ results
cost $O(m^2k^2)$ by 5.4. The structure constants $c_{ij}^{m}$ are the coordinates,
integers in $[0,p^{e_m})$. They satisfy antisymmetry and Jacobi because $A$ is a Lie
ring (5.1). In all $O_c(k^4)$ ring operations (using $r, m \le k$). (G4) The
$O_c(d + r^2)$ dictionary operations on words of length at most $c$ over $s$ letters
(building the word-to-index dictionary once, then the lookups) are not ring
operations; each is $O(c\log_2 s)$ bit operations.

(Exact computation: on five explicit Lazard rings with $p^e \in \{3^2, 3^3, 5^2\}$,
$s \in \{2,3\}$, $c \in \{2,3\}$, including a class-3 ring over $\mathbb{Z}/25$ with
orders $(2,2,2,1)$ and a redundant third generator, samples drawn uniformly from
$(\ker\pi)^\perp$ were fed to the algorithm as implemented in the script; in every
run ($5$ repeats each) the output basis had the right orders, $\varepsilon_i \mapsto \pi(\tilde\varepsilon_i)$
was an additive bijection, and every computed bracket matched the bracket of the
images. The operation counter recorded $170$-$1611$ ring operations per run.)

### 5.6 Images and the chart-to-group map (P6: proved)

$\tilde\varepsilon_i$ has at most $r \le n$ nonzero coordinates, so by the evaluation
formula of part (i), $\Phi(\tilde\varepsilon_i)$ costs at most
$r\cdot2b_e + (r-1)(m_+ + 2b_eq_+) \le n(2b_e + m_+ + 2b_eq_+)$ group multiplications
from the precomputed $h_j = \pi(w_j)$; all $m \le n$ images cost at most
$n^2(2b_e + m_+ + 2b_eq_+)$. By 5.1 and `cor:tb-correspondence`, $\bar\pi : \varepsilon_i \mapsto \pi(\tilde\varepsilon_i)$
is a Lie ring isomorphism $\mathcal{L}_G \to \log G$, and
$\exp\bar\pi(\sum_it_i\varepsilon_i) = \Phi(\sum_it_i\tilde\varepsilon_i)$ is the
$\Pi_+$-fold of the powers $\Phi(\tilde\varepsilon_i)^{t_i}$, which is the
chart-to-group map of item (iv); its per-use cost there is not re-derived here.

### 5.7 Totals (P7: proved) and the $\ell$-only form (G1)

Ring operations modulo $M$: $O(dk^2 + k^4)$ (scan) $+ O(k^3)$ (Smith) $+ O_c(k^4)$
(structure constants) $+ O_c(1)$ (table) $= O_c(dk^2 + k^4)$. Dictionary operations:
$O_c(d + k^2)$. Group multiplications: at most $n^2(2b_e + m_+ + 2b_eq_+)$. No
evaluation of $\Phi$ beyond the $k$ samples, no query to $f$.

With $d \le \sum_{i\le c}s^i \le 2s^c$ ($s \ge 2$) and
$k = \lfloor\ell/\log_2p\rfloor + \lceil\log_p(8\ell/\eps)\rceil \le \ell + \log_2(8\ell/\eps) + 1$:
if $\log_2(8\ell/\eps) \le \ell$ then $k \le 2\ell + 1$ and the count is
$O_c(s^c\ell^2 + \ell^4) \subseteq O_c(s^c\ell^3 + \ell^4)$. Without a bound on
$\log(1/\eps)$ in terms of $\ell$ the $\ell$-only form is false in the trivial sense
that $k^4$ grows with $\log^4(1/\eps)$; in the input size $N = s\ell + w + \log(1/\eps)$
of `thm:bb-envelope`, $k = O(N)$ always. This is a wording defect in
`prop:black-box`(iv), not in the appendix paragraph, which is stated in $d$ and $k$.

### 5.8 What is not computed: a generating set of $\ker\pi$ (G3)

The chart needs $\ker\pi$ only through $\ker Y$: membership $Yu = 0$ costs $dk$ ring
operations, and $\Phi^{-1}(\Omega_1(G)) = \{x : px \in \ker\pi\}$ (item (iii)) is
likewise $\{x : pYx = 0\}$. A generating set of $\ker\pi$ (lattice basis in
$\mathbb{Z}^d$, as `lem:tb-kernel`'s last sentence and (M1) with $S = F$ would use) is
a $d\times d$ normal-form computation, $\poly(d) = \poly(s^c)$ and not linear in $d$.
Route (R2) as written invokes "(M1) with $S = F$ and the ideal $\ker\pi$"; that
sentence should point to the lemma instead (both are correct; only the cost differs).

## 6. Exact computations (script `check_chart_lemma.py`)

| Check | Cases | Result |
|---|---|---|
| Witt numbers $d = \sum_{k\le c}W(s,k)$ equal the Lyndon-word count | $c\le4$, $s\le3$ | agree |
| (L1) bracket expansions multihomogeneous with integer coefficients | $c\le4$, $s\le3$; also $(s,c)=(4,4),(2,5),(5,4)$ | all |
| (L2) max Lyndon words per content vs $(c-1)!$ | $c\le4$, $s\le5$ | $1,1,2,6$; equality at content $(1,\dots,1)$ |
| max basis elements touched by one bracket | $c\le5$ as above | $3$ |
| (L3) relabelling invariance against $T_c$ | $c\le4$, $s\le3$ | all pairs agree |
| Howell form: (H1), (H2), span, membership vs brute force | 60 random, $p\in\{2,3,5\}$, $e\le3$, $k\le3$ | pass |
| Smith form: $PCQ = D$, $P,Q$ unimodular, chain | 60 random, $k,r\le4$ | pass |
| Full chart on explicit Lazard rings (orders, bijection, brackets) | 5 rings, 5 runs each | pass |
| $C_9\times C_3$: second column $\equiv 0 \bmod 3$ but not in the span | 1 run | as the paper says |

Finite checks falsify only; they do not prove the lemma. The proofs are in Section 5
and in the LaTeX below.

## 7. Consequences for other statements

- `thm:bb-envelope`(iii) "Classical time is $O_c(s^c\ell^5 + \ell^6)$ bit operations
  for the charts": with $O(b_M^2) \le O(\ell^2)$ bit operations per ring operation and
  $\sum_{p>c}b_{M_p} \le \ell + O(\ell/\log_2 c)$, the lemma gives
  $O_c(s^c\ell^4 + \ell^6)$ under $\log_2(8\ell/\eps) \le \ell$, which is within the
  stated bound. The statement's "argued in route (R2)" for the chart arithmetic can be
  dropped once the lemma is in; the summation and gate counts remain argued, as the
  theorem says.
- `prop:black-box`(ii), route (R2), and the sentence before the proposition in
  `main.tex` ("except that the linear-in-$d$ chart arithmetic ... is argued there,
  not proved") need the edits in Section 9.
- `lem:tb-kernel` is unchanged; its last sentence (Smith form for a generating set of
  $\ker\pi$) is correct and is simply not used by the chart.

## 8. Exact statement that now holds; what is missing; gates

**Statement (proved here, AI-checked, pending human review).** Let $G$, $F = F_{s,c}$,
$\pi$, $\Phi$, $d$, $M = p^e$, $b_e$, $m_+$, $q_+$ and the precomputed $h_j$ be as in
the proof of `prop:black-box`(i), with $F$ given in its Lyndon basis, and let
$n = \log_p|G|$. Let $Y \in (\mathbb{Z}/M)^{k\times d}$ be any matrix whose rows
generate $(\ker\pi)^\perp$ (so $k \ge n$). Then, with $O_c(dk^2 + k^4)$ ring
operations modulo $M$, $O_c(d + k^2)$ dictionary operations on words of length at
most $c$, no evaluation of $\Phi$ and no query to $f$, one computes a set $J$ of
$r \le n$ basis indices whose columns generate $A = YF \cong F/\ker\pi$, elements
$\varepsilon_1,\dots,\varepsilon_m$ ($m \le r$) with
$A = \bigoplus(\mathbb{Z}/p^{e_i})\varepsilon_i$, $\sum e_i = n$, lifts
$\tilde\varepsilon_i \in F$ supported on $J$ with $Y\tilde\varepsilon_i = \varepsilon_i$,
a coordinate map at $O(k^2)$ per vector, and integer structure constants making
$\mathcal{L}_G = \bigoplus(\mathbb{Z}/p^{e_i})\varepsilon_i$ an explicit Lie ring in
the setting of `app:tb-ring` with $b = n$, such that
$\varepsilon_i \mapsto \pi(\tilde\varepsilon_i)$ is a Lie ring isomorphism onto
$\log G$ and a group isomorphism $(\mathcal{L}_G,\ast) \to G$. The images
$\Phi(\tilde\varepsilon_i)$ cost at most $n^2(2b_e + m_+ + 2b_eq_+)$ group
multiplications in all. Combined with `lem:tb-kernel` (which supplies $Y$ with
failure probability at most $\delta$ from $t \le k$ samples), this is item (iv) with
the operation count $O_c(dk^2 + k^4)$; the $\ell$-only form
$O_c(s^c\ell^3 + \ell^4)$ (indeed $O_c(s^c\ell^2 + \ell^4)$) holds when
$\log_2(8\ell/\eps) \le \ell$.

**Still missing.**
1. Human review of the proof below and of the script.
2. The per-use cost $4n(2b_M + A_c)$ of the chart-to-group map in item (iv) was not
   re-derived here (it is the $\Pi_+$-fold of $n$ powers with Bennett cleanup, from the
   envelope note); only its precomputation cost is covered.
3. The lemma is deterministic given $Y$; the failure event of `lem:tb-kernel`
   ($\ker Y \supsetneq \ker\pi$) is charged there and is not detected by the chart
   computation. An optional Las Vegas check would need a generating set of $\ker Y$,
   at $\poly(d)$ cost, and is not proposed.
4. Constants in $O_c$ are not made explicit; $(c-1)!$ enters linearly through the
   $z_{ab}$ step, and $|T_c|$ enters only the one-time setup.

**Claim gates.** All Rees claim gates stay false. This note proves an operation
count for public classical post-processing; it does not change the conditional
status of `prop:black-box`(ii) (R1)/(R2) on `thm:ring-to-field`(iii) and `thm:main`,
and it is no evidence of a speedup, novelty or hardness.

## 9. Proposed paper text (AI-checked, pending human review)

All labels below exist in the current sources except the new `lem:tb-chart`. Macros
used (`\Fp`, `\rank`, `\diag`, `\coloneqq`, `\poly`, `\eps`, `\file`) are already used
in the appendix or `main.tex`.

### 9.1 `appendix-torsion-blackbox.tex`, proof of part (i): fix the basis

In the sentence "a free $\mathbb{Z}/p^e$-module with Hall basis $w_1 = X_1,\dots,w_s = X_s, w_{s+1},\dots,w_d$,"
replace "Hall basis" by

```latex
Hall basis $w_1 = X_1,\dots,w_s = X_s, w_{s+1},\dots,w_d$, which we take to be the
Lyndon basis (the standard bracketings $b(w)$ of the Lyndon words $w$ of length at
most $c$, ordered by length and then lexicographically; Reutenauer, \emph{Free Lie
Algebras}, Chapter~5),
```

(The rest of the sentence is unchanged; the Lyndon basis is a Hall basis, has
$w_j = [w_{j'},w_{j''}]$ with $j',j'' < j$ by the standard factorisation, and is
multihomogeneous, which Lemma~\ref{lem:tb-chart} uses.)

### 9.2 `appendix-torsion-blackbox.tex`, route (R2): two edits

Replace

```latex
  Lemma~\ref{lem:tb-kernel}. By (M1) with $S = F$ and the ideal $\ker\pi$, present
  $\mathcal{L}_G \coloneqq F/\ker\pi \cong \bigoplus_i \mathbb{Z}/p^{e_i}$ with explicit
  structure constants inherited from $F$ and section $\tilde\sigma$.
```

by

```latex
  Lemma~\ref{lem:tb-kernel}. By Lemma~\ref{lem:tb-chart} below, present
  $\mathcal{L}_G \coloneqq F/\ker\pi \cong \bigoplus_i \mathbb{Z}/p^{e_i}$ with explicit
  structure constants, lifts $\tilde\varepsilon_i \in F$ of the basis and the section
  $\tilde\sigma(\sum_i t_i\varepsilon_i) = \sum_i t_i\tilde\varepsilon_i$. ((M1) with
  $S = F$ and the ideal $\ker\pi$ gives the same presentation from a generating set of
  $\ker\pi$, at $\poly(d)$ cost; the lemma costs $O_c(dk^2 + k^4)$ ring operations and
  never computes such a generating set.)
```

Then delete the whole paragraph beginning "\emph{Chart arithmetic at cost linear in
$d$} (argued; AI-checked, pending human review)." and ending "with no query to $f$."
and insert, after the `\end{enumerate}` that closes (R1)-(R2), the following.

```latex
\paragraph{Ring operations.} A \emph{ring operation modulo $M = p^e$} ($p$ known) is an
addition, subtraction or multiplication of residues; the computation of the $p$-adic
valuation $v_p(a) \in \{0,\dots,e\}$ of a residue with its unit part $a/p^{v_p(a)}$; an
exact division $a \mapsto a/p^v$ with $p^v \mid a$, whose result is defined modulo
$p^{e-v}$ and may be lifted to $\mathbb{Z}/M$ arbitrarily; or the inversion of a unit.
Each costs $O(b_e^2)$ bit operations (schoolbook arithmetic, the extended Euclidean
algorithm, and at most $e$ trial divisions by $p$ at $O(b_e\log_2 p)$ each, with
$e\log_2 p \le b_e$).

\begin{lemma}[Chart from the sample matrix; AI-checked, pending human review]
\label{lem:tb-chart}
Let $G$, $F = F_{s,c}$ in its Lyndon basis $w_1,\dots,w_d$, $\pi$, $\Phi$, $M = p^e$,
$b_e$ and the precomputed $h_j = \pi(w_j)$ be as in the proof of part~(i), and let
$n = \log_p|G| \le \lfloor\ell/\log_2 p\rfloor$. Let $Y \in (\mathbb{Z}/M)^{k\times d}$
be a matrix whose rows generate $(\ker\pi)^\perp$, as the samples of
Lemma~\ref{lem:tb-kernel} do on its success event; then $k \ge n$. Then
$u \mapsto Yu$ induces a Lie ring isomorphism $F/\ker\pi \cong A \coloneqq YF \subseteq (\mathbb{Z}/M)^k$,
with $[Yu,Yv] \coloneqq Y[u,v]$, and with $O_c(dk^2 + k^4)$ ring operations modulo $M$,
$O_c(d + k^2)$ dictionary operations on words of length at most $c$ over $s$ letters,
no evaluation of $\Phi$ and no query to $f$, one computes:
\begin{enumerate}[label=(\alph*),leftmargin=2em]
  \item a set $J \subseteq \{1,\dots,d\}$ of $r \le n$ indices such that the columns
  $Yw_j$, $j \in J$, generate $A$;
  \item elements $\varepsilon_1,\dots,\varepsilon_m \in A$, $m \le r$, and integers
  $1 \le e_i \le e$ with $A = \bigoplus_{i=1}^m(\mathbb{Z}/p^{e_i})\varepsilon_i$ and
  $\sum_i e_i = n$, together with lifts $\tilde\varepsilon_i = \sum_{j\in J}\alpha_{ij}w_j \in F$
  satisfying $Y\tilde\varepsilon_i = \varepsilon_i$;
  \item the coordinate map $A \to \bigoplus_i\mathbb{Z}/p^{e_i}$, $v \mapsto (t_i)_i$ with
  $v = \sum_i t_i\varepsilon_i$, at $O(k^2)$ ring operations per vector;
  \item integers $c_{ij}^{m'}$ with $[\varepsilon_i,\varepsilon_j] = \sum_{m'}c_{ij}^{m'}\varepsilon_{m'}$.
\end{enumerate}
Consequently $\mathcal{L}_G \coloneqq \bigoplus_i(\mathbb{Z}/p^{e_i})\varepsilon_i$ with
the constants $c_{ij}^{m'}$ is an explicit Lie ring of class at most $c$ in the setting
of Section~\ref{app:tb-ring}, with $b = n$, and
$\bar\pi : \varepsilon_i \mapsto \pi(\tilde\varepsilon_i)$ is a Lie ring isomorphism
$\mathcal{L}_G \to \log G$, hence a group isomorphism $(\mathcal{L}_G,\ast) \to G$.
The images $\Phi(\tilde\varepsilon_i) = \exp\bar\pi(\varepsilon_i)$ cost at most
$n(2b_e + m_+ + 2b_eq_+)$ group multiplications each, at most
$n^2(2b_e + m_+ + 2b_eq_+)$ in all. Membership of $u \in F$ in $\ker\pi = \ker Y$ is
decided by $Yu = 0$ at $dk$ ring operations; no generating set of $\ker\pi$ is computed.
\end{lemma}

\begin{proof}
\emph{Step 0: the Lyndon basis.} Write $\mu(w) \in \mathbb{N}^s$ for the content of a
word $w$ (the number of occurrences of each letter). The free Lie ring is graded by
content, the bracket adds contents, and each $b(w)$ is homogeneous of content
$\mu(w)$; so $[w_a,w_b]$ is $0$ in $F$ if $|\mu(w_a)|+|\mu(w_b)| > c$ and otherwise
lies in the span of the basis elements of content $\mu(w_a)+\mu(w_b)$. For a content
$\alpha$ with $|\alpha| = m \le c$ there are at most $(m-1)! \le (c-1)!$ Lyndon words
of content $\alpha$: a Lyndon word is primitive, its $m$ rotations are distinct words
of content $\alpha$, and each rotation class of a primitive word contains exactly one
Lyndon word, so their number is at most $\binom{m}{\alpha}/m \le (m-1)!$. Let $T_c$ be
the table whose entry at a pair $(u,v)$ of Lyndon words over $\{1<\dots<c\}$ with
$|u|+|v| \le c$ is the Lyndon-basis expansion of $[b(u),b(v)]$ in the free nilpotent
Lie ring of class $c$ on $c$ generators, an integer vector with at most $(c-1)!$
entries; $T_c$ is finite and depends only on $c$, and reducing it modulo $M$ costs
$O_c(1)$ ring operations. Given $w_a, w_b$ with $|w_a|+|w_b| \le c$, let $X'$ be the
set of letters they use, $t = |X'| \le c$, and $\rho : X' \to \{1,\dots,t\}$ the
order-preserving bijection. Whether a word is Lyndon, and its standard factorisation,
depend only on the relative order of its letters, so $\rho$ maps Lyndon words over
$X'$ bijectively to Lyndon words over $\{1,\dots,t\}$ and commutes with $b$; the Lie
ring map induced by $\rho$ is an isomorphism of the free Lie ring on $X'$ onto the free
Lie ring on $\{1,\dots,t\}$, and the inclusion of the free Lie ring on $X'$ into that
on $X$ maps Lyndon basis to Lyndon basis (the same words). Hence
$[w_a,w_b] = \sum_w T_c(\rho w_a,\rho w_b)_w\,b(\rho^{-1}w)$ in $F$: every bracket of two
basis elements is read from $T_c$, with at most $(c-1)!$ terms, at $O_c(1)$
dictionary lookups of the indices of the words $\rho^{-1}w$ in the basis.

\emph{Step 1: $A$.} For a subgroup $B \le (\mathbb{Z}/M)^d$ one has $B^{\perp\perp} = B$:
the pairing $a \mapsto (u \mapsto \zeta_M^{a\cdot u})$ identifies $(\mathbb{Z}/M)^d$
with its character group, under which $B^\perp$ is the character group of
$(\mathbb{Z}/M)^d/B$, of order $M^d/|B|$; so $|B^{\perp\perp}| = |B|$ and
$B \subseteq B^{\perp\perp}$. Since the rows of $Y$ generate $(\ker\pi)^\perp$,
$\ker Y = (\ker\pi)^{\perp\perp} = \ker\pi$, and $u \mapsto Yu$ induces an additive
isomorphism $F/\ker\pi \to A$. As $\ker\pi$ is an ideal, $[Yu,Yv] \coloneqq Y[u,v]$ is
well defined and the isomorphism is one of Lie rings. In particular
$|A| = |\pi(F)| = |G| = p^n$, and $n \le \lfloor\ell/\log_2 p\rfloor \le k$ by unique
encodings and the definition of $k$ in Lemma~\ref{lem:tb-kernel}. Since
$\ker\pi = \ker Y$, membership of $u$ in $\ker\pi$ is the test $Yu = 0$, at $dk$ ring
operations, which is the last sentence of the lemma.

\emph{Step 2: Howell forms over $\mathbb{Z}/p^e$.} Call a sequence $r_1,\dots,r_q$ of
nonzero vectors of $(\mathbb{Z}/M)^k$ a \emph{Howell form} if (H1) its leading
positions $j_1 < \dots < j_q$ are strictly increasing and the leading entries are
$p^{a_1},\dots,p^{a_q}$ with $0 \le a_t < e$, and (H2) $p^{e-a_t}r_t \in \langle r_{t+1},\dots,r_q\rangle$
for every $t$; then $q \le k$. Let $S = \langle r_1,\dots,r_q\rangle$.

\emph{Membership test.} Given $v$, scan $j = 1,\dots,k$: if $v_j \ne 0$ and $j = j_t$
with $p^{a_t} \mid v_j$, replace $v$ by $v - (v_j/p^{a_t})r_t$; if $v_j \ne 0$ otherwise,
reject; at the end accept iff $v = 0$. This is at most $q \le k$ reductions of $O(k)$
ring operations, so $O(k^2)$. Reductions preserve the coset $v + S$, so acceptance
implies $v \in S$. Conversely, put $S_t = \langle r_t,\dots,r_q\rangle$ and suppose
$v \in S_t$ when the scan reaches $j_t$ (true for $t = 1$). Then $v$ vanishes before
$j_t$, and $v = \sum_{i\ge t}\lambda_ir_i$ gives $v_{j_t} = \lambda_tp^{a_t}$, so
$p^{a_t} \mid v_{j_t}$; any lift $\lambda_t'$ of $v_{j_t}/p^{a_t}$ is congruent to
$\lambda_t$ modulo $p^{e-a_t}$, so
$v - \lambda_t'r_t = \sum_{i>t}\lambda_ir_i + (\lambda_t-\lambda_t')r_t \in S_{t+1}$ by (H2).
Positions strictly between pivots vanish on $S_t$, so no element of $S$ is rejected,
and at the end $v \in S_{q+1} = 0$.

\emph{Construction.} Given generators $g_1,\dots,g_{q_0}$ of $S$, for $j = 1,\dots,k$:
among the remaining vectors choose one whose entry in position $j$ has minimal
valuation $a < e$ (if none, continue), multiply it by the inverse of the unit part of
that entry so the entry becomes $p^a$, declare it the pivot row for $j$ and remove it;
every other remaining vector $r$ has $p^a \mid r_j$, so replace it by
$r - (r_j/p^a)\cdot\mathrm{pivot}$; finally append $p^{e-a}\cdot\mathrm{pivot}$ to the
remaining set. The span of the pivot rows together with the remaining set stays $S$,
since each operation is an invertible row operation or appends an element of the
span; remaining vectors stay zero in all earlier positions; and with $R_t$ the
remaining set right after the $t$-th pivot is fixed, each later step replaces $R$ by
$R'$ with $\langle R\rangle = \langle r_{\mathrm{new}}\rangle + \langle R'\rangle$, so
$\langle R_t\rangle = \langle r_{t+1},\dots,r_q\rangle \ni p^{e-a_t}r_t$, which is (H2).
At most $k$ vectors are appended, so at most $q_0 + k$ are processed, at
$O((q_0+k)k)$ ring operations per position: $O((q_0+k)k^2)$ in all, which is $O(k^3)$
for $q_0 \le k+1$. Different lifts of an exact quotient $r_j/p^a$ differ by multiples
of $p^{e-a}$, and $p^{e-a}\cdot\mathrm{pivot}$ lies in the module in question, so no
computed span or coset depends on the lifts. (For general moduli see Howell,
\emph{Linear and Multilinear Algebra}\ 1986, and Storjohann and Mulders, ESA 1998.)

\emph{Step 3: the column scan, (a).} Scan $j = 1,\dots,d$ and keep $j$ exactly when
$Yw_j$ fails the membership test against the Howell form of the columns kept so far;
after keeping a column, rebuild the Howell form of the kept columns. By induction on
$j$, the kept columns with index at most $j$ span $\langle Yw_1,\dots,Yw_j\rangle$, so
the kept set $J$ spans $A$. Each kept column strictly enlarges a subgroup of the
$p$-group $A$ of order $p^n$, so $r = |J| \le n \le k$. The cost is $d$ tests at
$O(k^2)$ and at most $n$ constructions from at most $k+1$ generators at $O(k^3)$:
$O(dk^2 + k^4)$ ring operations. Testing the columns modulo $p$ instead is not enough:
for $G = C_9\times C_3$, $s = 2$, every sample lies in $\{(x,3y,0)\}$, so the second
column is divisible by $3$, yet it is not in the $\mathbb{Z}/9$-span of the first.

\emph{Step 4: Smith form, (b) and (c).} Let $C \in (\mathbb{Z}/M)^{k\times r}$ have the
kept columns, $\kappa_1 < \dots < \kappa_r$ their indices. For $t = 1,2,\dots$: choose
an entry of minimal valuation $a_t$ among rows and columns $\ge t$ (stop if all are
zero), permute it to $(t,t)$, scale row $t$ by the inverse of its unit part so that
$C_{tt} = p^{a_t}$; all other entries of row $t$ and column $t$ are multiples of
$p^{a_t}$, so clear column $t$ by row operations and then row $t$ by column
operations, which now change only row $t$; record the row operations in
$P \in \mathrm{GL}_k(\mathbb{Z}/M)$ and the column operations in
$Q \in \mathrm{GL}_r(\mathbb{Z}/M)$. Then $PCQ = D$ is diagonal with entries
$p^{a_1},\dots,p^{a_r}$ (an entry with $a_t = e$ is $0$). Each of the at most $r$ steps
costs $O(kr)$ valuations and operations on $C$, $O(k^2)$ on $P$ and $O(r^2)$ on $Q$, so
$O(k^2r) \le O(k^3)$ in all. Let $I = \{i : a_i < e\}$, $m = |I|$, $e_i = e - a_i$ for
$i \in I$, $\varepsilon_i = CQe_i$ and $\tilde\varepsilon_i = \sum_{a=1}^rQ_{ai}w_{\kappa_a}$;
then $Y\tilde\varepsilon_i = CQe_i = \varepsilon_i$ and $\tilde\varepsilon_i$ is supported
on $J$. Since $P$ and $Q$ are automorphisms,
$PA = \mathrm{col}(PCQ) = \bigoplus_{i\in I}p^{a_i}(\mathbb{Z}/M)e_i$, a direct sum of
cyclic groups of orders $p^{e_i}$, and $P^{-1}(p^{a_i}e_i) = P^{-1}De_i = CQe_i = \varepsilon_i$,
so $A = \bigoplus_{i\in I}(\mathbb{Z}/p^{e_i})\varepsilon_i$ and
$\sum_{i\in I}e_i = \log_p|A| = n$. For $v \in A$, $v = \sum_it_i\varepsilon_i$ iff
$Pv = \sum_it_ip^{a_i}e_i$, so $t_i = (Pv)_i/p^{a_i} \bmod p^{e_i}$ by exact division,
at $O(k^2)$ ring operations; this is (c).

\emph{Step 5: structure constants, (d).} By Step 1,
$[\varepsilon_i,\varepsilon_j] = Y[\tilde\varepsilon_i,\tilde\varepsilon_j] = \sum_{a,b\le r}Q_{ai}Q_{bj}z_{ab}$
with $z_{ab} \coloneqq Y[w_{\kappa_a},w_{\kappa_b}]$. By Step 0 each $z_{ab}$ is a
combination of at most $(c-1)!$ columns of $Y$, read from $T_c$, at $O_c(k)$ ring
operations and $O_c(1)$ dictionary lookups; all $r^2$ of them cost $O_c(r^2k)$. The two
contractions $u_{ib} = \sum_aQ_{ai}z_{ab}$ and $\sum_bQ_{bj}u_{ib}$ cost $O(r^3k)$ each,
and the coordinates of the $m^2$ results, by (c), $O(m^2k^2)$. The constants
$c_{ij}^{m'}$ are these coordinates; they are integers in $[0,p^{e_{m'}})$, and they
satisfy antisymmetry and the Jacobi identity because $A$ is a Lie ring. With
$r, m \le k$ this is $O_c(k^4)$ ring operations. The word-to-index dictionary is built
once at $O_c(d)$ dictionary operations.

\emph{Step 6: totals and the isomorphism.} Steps 0 and 3 to 5 cost
$O_c(1) + O(dk^2 + k^4) + O(k^3) + O_c(k^4) = O_c(dk^2 + k^4)$ ring operations and
$O_c(d + k^2)$ dictionary operations; no step evaluates $\Phi$ or queries $f$. The ring
$\mathcal{L}_G$ is $A$ in the basis $(\varepsilon_i)$, so it is a Lie ring of class at
most $c$ annihilated by $M$ with $b = \sum_ie_i = n$, as in Section~\ref{app:tb-ring},
and $\bar\pi(\varepsilon_i) = \pi(\tilde\varepsilon_i)$ is the composite of
$A \cong F/\ker\pi$ (Step 1) with the isomorphism $F/\ker\pi \cong \log G$ induced by
$\pi$; by Corollary~\ref{cor:tb-correspondence} it is a group isomorphism
$(\mathcal{L}_G,\ast) \to G$. Finally $\tilde\varepsilon_i$ has at most $r \le n$ nonzero
coordinates, so by the evaluation count of part~(i),
$\Phi(\tilde\varepsilon_i) = \exp\bar\pi(\varepsilon_i)$ costs at most
$n\cdot2b_e + (n-1)(m_+ + 2b_eq_+) \le n(2b_e + m_+ + 2b_eq_+)$ group multiplications
from the $h_j$.
\end{proof}

\noindent In the notation of Proposition~\ref{prop:black-box}(iv), with
$d \le \sum_{i\le c}s^i \le 2s^c$ for $s \ge 2$ and
$k = \lfloor\ell/\log_2 p\rfloor + \lceil\log_p(8\ell/\eps)\rceil \le \ell + \log_2(8\ell/\eps) + 1$,
the count $O_c(dk^2 + k^4)$ is $O_c(s^c\ell^2 + \ell^4) \subseteq O_c(s^c\ell^3 + \ell^4)$
whenever $\log_2(8\ell/\eps) \le \ell$; in the input size
$N = s\ell + w + \log(1/\eps)$ of Theorem~\ref{thm:bb-envelope} it is
$O_c(s^cN^2 + N^4)$ without that condition. Each ring operation is $O(b_e^2)$ bit
operations.
```

### 9.3 `main.tex`, `prop:black-box`(iv)

Replace

```latex
recovers $\ker\pi$ with error at most $\eps/(4\ell)$ and no query to $f$; here $k$ bounds the number of cyclic factors of $\log G$, which is not bounded by $s$. Howell and Smith normal forms over $\mathbb{Z}/M\mathbb{Z}$ then give the explicit chart $F_{s,c}/\ker\pi \cong \log G$, with structure constants, in $O_c(s^c\ell^3 + \ell^4)$ ring operations (argued in Appendix~\ref{app:torsion-blackbox}, route~(R2), at $O_c(dk^2 + k^4)$).
```

by

```latex
recovers $\ker\pi$, as the solution set of $k$ linear congruences, with error at most $\eps/(4\ell)$ and no query to $f$; here $k$ bounds the number of cyclic factors of $\log G$, which is not bounded by $s$. Howell and Smith normal forms over $\mathbb{Z}/M\mathbb{Z}$ then give the explicit chart $F_{s,c}/\ker\pi \cong \log G$, with structure constants, in $O_c(dk^2 + k^4)$ ring operations modulo $M$, each $O(b_M^2)$ bit operations (Lemma~\ref{lem:tb-chart} in Appendix~\ref{app:torsion-blackbox}, which never computes a generating set of $\ker\pi$); this is $O_c(s^c\ell^2 + \ell^4) \subseteq O_c(s^c\ell^3 + \ell^4)$ when $\log_2(8\ell/\eps) \le \ell$.
```

and, at the end of the same item, replace "This item is from \file{research/audits/reviews/2026-11-02-rees-bb-envelope.md} (AI-checked only); Lemma~\ref{lem:tb-kernel} proves the kernel step" by "The sample count is from \file{research/audits/reviews/2026-11-02-rees-bb-envelope.md} and the chart arithmetic from \file{research/audits/reviews/2026-11-03-rees-chart-lemma.md} (both AI-checked only); Lemma~\ref{lem:tb-kernel} proves the kernel step".

### 9.4 `main.tex`, the paragraph before the proposition

Replace "Appendix~\ref{app:torsion-blackbox} proves it, except that the linear-in-$d$ chart arithmetic behind the operation count $O_c(s^c\ell^3+\ell^4)$ of item~(iv) is argued there, not proved (AI-checked, pending human review)." by

```latex
Appendix~\ref{app:torsion-blackbox} proves it, including the linear-in-$d$ chart
arithmetic of item~(iv) (Lemma~\ref{lem:tb-chart}); as the rest of that appendix, the
proofs are AI-checked, pending human review.
```

(The replaced sentence is quoted exactly from the current `main.tex`.)

### 9.5 `main.tex`, `thm:bb-envelope`, proof-status sentence

In "The chart arithmetic in~(ii)--(iii) is argued in route~(R2) of Appendix~\ref{app:torsion-blackbox}, and the summation into~(i), the gate and time counts of~(iii) and the exponents above are \emph{argued} in the proof sketch below, not proved in this paper." replace the first clause by "The chart arithmetic in~(ii)--(iii) is Lemma~\ref{lem:tb-chart} of Appendix~\ref{app:torsion-blackbox}, under $\log_2(8\ell/\eps) \le \ell$ for its $\ell$-only form, and the summation ...".

### 9.6 Appendix header comment

Add to the "Works cited in the text without a key" list:

```latex
%   Howell1986       J. A. Howell, Spans in the module (Z_m)^s, Linear and
%                    Multilinear Algebra 19 (1986) 67-77
%   StorjohannMulders1998  A. Storjohann, T. Mulders, Fast algorithms for linear
%                    algebra modulo N, ESA 1998, LNCS 1461, 139-150
```

(I did not verify these bibliographic details against the sources; the integrator
should, or drop the parenthetical citation in Step 2, which the proof does not need.)
