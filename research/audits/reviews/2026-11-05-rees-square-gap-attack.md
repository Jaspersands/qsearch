# Two-level SDE threshold, round 10: the square gap attacked from the brief's new directions

AI-only report (2026-11-05), pending human review. No paper file was edited. Scripts and
outputs are in `2026-11-05-rees-square-gap-attack/` (two tiny Python checks, under one second
each, `/opt/anaconda3/bin/python -I`, `nice -n 19`).

Inputs read: `docs/papers/rees-hsp/appendix-schedule2.tex` (all of it), `main.tex` Remark
`rem:two-level-threshold-size`, the verdict and barrier sections of
`2026-11-05-rees-threshold-{6,7,8,9}.md` and their `-check` files, TH2 §§2-3, TH3 §§0,2,5-7, TH5
§§0,3-4, and the top of `research/STATE.md`. Abbreviations as in those reports: TH$n$ is round $n$.

## 0. Verdict

- **No unconditional threshold $T = o(\kappa^\kappa)$ is proved, and none of the brief's new
  routes can give one.** Every route listed in the brief (second moment or Janson over
  structured witness families, several coset generators at once, Katz-type sums over varieties,
  Stepanov, sum-product and additive energy of the cosets, Chevalley-Warning with restricted
  variables, Combinatorial Nullstellensatz) is shown below either to reduce to a certificate
  class already excluded by a rigorous barrier (O1, O2), or to be inapplicable outright. The
  square gap between the proved $T_A(\kappa) = \kappa^{\kappa+1-o(1)}$ and the observed
  $1.5\,\kappa^{(\kappa+1)/2}$ stays open, and so does the smaller question of any exponent below
  $\kappa$.
- **Proved here (rigorous, new in this form).**
  1. *Theorem 1.* The $(\kappa-1)$-wise independent law behind barrier O2 is written out
     explicitly, with a five-line proof. Consequence, now citation-free: for $p \le \kappa^\kappa/2$
     no certificate built from facts about at most $\kappa-1$ column counts at a time, each true
     under independence, can show $p \notin E_2(\kappa)$; and such a law with
     $\Pr[\text{all columns nonempty}] = 0$ exists exactly when $\Pr[n_0 > 0] \le 1/2$.
  2. *Theorem 2 (Chebotarev barrier).* No finite set of configurations defined over number
     fields (small integers, cyclotomic units, anything $p$-uniform) reduces to a two-level
     contraction at every large prime $p \equiv 1 \pmod\kappa$, $\kappa \ge 3$: a set of primes of
     positive density defeats all of them at once. This kills the Graham-Ringrose-type
     (Paley clique) route for an all-$p$ statement.
  3. *Proposition 3.* Exact structure of the character expansion: frequencies with a
     degree-one row or column vanish; frequencies with $\sum e \ne 0$ vanish; every 4-cycle
     frequency is an exact product of two Jacobi sums with $|S_e| = p^{2\kappa-2}(p-1)$. So the
     sizes TH3 measured are exact, cannot be improved by any estimate, and are harmless
     ($\le \kappa^7 p^{2\kappa-1}/4$ in total); the whole loss of the expansion sits in the
     $\kappa^{\kappa^2}(1-o(1))$ frequencies of dense support.
  4. *Proposition 4.* Chevalley-Warning, Ax-Katz and the Combinatorial Nullstellensatz are
     inapplicable to the contraction system for $\kappa \ge 4$ (degree count), and at $\kappa = 3$
     the Nullstellensatz coefficient is the count itself (tautology).
  5. *Lemma 5, Proposition 6.* Several generators at once change any moment threshold by a
     factor in $[\kappa^{-1/(2\kappa-2)}, 1]$; no Harris/FKG-type inequality for the column events
     holds with a $p$-independent constant, because $E_2(\kappa) \ne \emptyset$.
- **Heuristic, labelled as such (§4).** A square-root-cancellation certificate on any family with
  $v$ free parameters and $c$ coset conditions certifies only $p > \kappa^{2c/v}$, while the
  first moment is positive from $p > \kappa^{c/v}$; for the full problem $c/v = (\kappa+1)/2$, so
  $T_A$ already sits at the square-root limit. This is TH6 §6.2 restated; it is not a theorem
  (the "constant cell" loophole is explained in §4), and it is not used for any claim.
- **Consistency with data.** No new threshold is claimed, so no threshold can conflict with
  $3221 \in E_2(7)$ or $14281 \in E_2(8)$. The barrier values are above every known member:
  $\kappa^\kappa/2 = 4.1\cdot10^5$ at $\kappa = 7$, $8.4\cdot10^6$ at $\kappa = 8$ (§5).

## 1. Setting

$\kappa \ge 2$, $p \equiv 1 \pmod\kappa$ prime, $h = (p-1)/\kappa$, $Q_0 = (\mathbb{F}_p^\times)^\kappa$,
$Q_m = \xi^m Q_0$ for a coset generator $\xi$, $Q_m^\circ = Q_m \cup \{0\}$. By
`lem:app-s2-normal` a two-level contraction is a pair $(\alpha,\beta) \in \mathbb{F}_p^{2\kappa}$ with

$$\alpha_j + \beta_i \in Q^\circ_{-(i+j)} \ \ (i,j \in \mathbb{Z}_\kappa), \qquad \alpha_0 + \beta_0 \ne 0, \tag{R}$$

and $E_2(\kappa)$ is the set of primes with no such pair. Facts from the appendix used below:
(F1) in any solution of (R) the $\alpha_j$ are pairwise distinct and the $\beta_i$ are pairwise
distinct (`lem:app-s2-two-rows`); hence every row and column has at most one zero cell.
(F2) For $y = (0, y_1, \dots, y_{\kappa-1})$ uniform, $X_j(y) = \{x : x + y_i \in Q_{-(i+j)}\ \forall i\}$,
$n_j = |X_j(y)|$, $\mathbb{E}\, n_j = h^\kappa/p^{\kappa-1} =: \lambda < p/\kappa^\kappa$
(`lem:app-s2-moments`); $p \notin E_2(\kappa)$ iff some $y$ has every $X_j(y) \ne \emptyset$.
(F3) $\chi$ is a character of order $\kappa$ with $\chi(\xi) = \omega = e^{2\pi i/\kappa}$. Convention
for the expansion: $\chi^0 \equiv 1$ on all of $\mathbb{F}_p$ (including $0$) and $\chi^s(0) = 0$ for
$s \not\equiv 0$. Then $[u \in Q_m] = \kappa^{-1}\sum_{s} \omega^{-ms}\chi^s(u)$ for $u \ne 0$, and the
right side equals $1/\kappa$ at $u = 0$. For $e \in \mathbb{Z}_\kappa^{\kappa\times\kappa}$ put

$$S_e = \sum_{(\alpha,\beta) \in \mathbb{F}_p^{2\kappa}} \prod_{i,j} \chi^{e_{ij}}(\alpha_j + \beta_i),$$

so that $\kappa^{-\kappa^2}\sum_e \omega^{\langle e,\, i+j\rangle} S_e$ counts the solutions of the coset
conditions in (R) with a configuration having $z$ zero cells weighted $\kappa^{-z}$ (and with
the cell $(0,0)$ allowed to vanish). The barriers O1 (TH3 §2: term-by-term bounds cannot certify
$p \le 2^{-1/(\kappa-1)}\kappa^\kappa$) and O2 (TH3 §3) are cited as proved there.

## 2. Proved results

### Theorem 1 (the $(\kappa-1)$-wise independent law, explicitly) [proved]

Let $\kappa \ge 2$ and $0 < q \le 1/2$. Define $P$ on $\{0,1\}^\kappa$ by

$$P(x) = q^{|x|}(1-q)^{\kappa - |x|} - (-1)^{\kappa - |x|} q^\kappa, \qquad |x| = \textstyle\sum_i x_i .$$

(i) $P$ is a probability law, every marginal of $P$ on a proper subset $S \subsetneq [\kappa]$ of the
coordinates is the product Bernoulli$(q)^{\otimes S}$ law, and $P(1,\dots,1) = 0$.

(ii) Conversely, if $q > 1/2$, no law on $\{0,1\}^\kappa$ whose proper marginals are
Bernoulli$(q)$ products gives probability $0$ to $(1,\dots,1)$.

(iii) Let $\nu$ be any law on $\mathbb{N}$ with $\nu(\{n > 0\}) = q \le 1/2$. There is a law $\Lambda$ on
$\mathbb{N}^\kappa$ whose marginal on every set of at most $\kappa-1$ coordinates is $\nu^{\otimes(\kappa-1)}$
(restricted) and with $\Lambda(\text{all } n_j > 0) = 0$.

(iv) (Barrier O2, citation-free.) Let $\nu$ be the law of $n_0$ under uniform $y$ (F2). If
$p \le \kappa^\kappa/2$, then $\nu(\{n>0\}) \le \lambda < 1/2$, so $\Lambda$ of (iii) exists. Hence no
inequality that (a) involves only the joint law of at most $\kappa - 1$ of $n_0,\dots,n_{\kappa-1}$ at
a time and (b) holds for independent copies of $\nu$, can imply $\Pr[\text{all } n_j > 0] > 0$.
Facts of type (a)-(b) include every moment, factorial moment and tail bound of one $n_j$
(so $T_A$, TH2 Theorem 5, the union bound), and every joint factorial moment
$\mathbb{E}\binom{\sum_{j \in S} n_j}{m}$ with $m \le \kappa-2$ (TH9 Theorem 1, by Vandermonde).

*Proof.* (i) Write $\mathrm{ind}(x) = q^{|x|}(1-q)^{\kappa-|x|}$ for the product law and
$\chi_{\mathrm{top}}(x) = (-1)^{|x|}$ for the top Walsh character. Then $P = \mathrm{ind} - (-1)^\kappa q^\kappa \chi_{\mathrm{top}}$.
Summing $\chi_{\mathrm{top}}$ over any one coordinate gives $0$, so (1) $\sum_x P(x) = 1$, and (2) for a
proper subset $S$ the marginal of $\chi_{\mathrm{top}}$ on $S$ vanishes (sum out a coordinate outside
$S$), so the marginal of $P$ on $S$ equals that of $\mathrm{ind}$. At $x = (1,\dots,1)$:
$P = q^\kappa - (-1)^0 q^\kappa = 0$. Nonnegativity: if $\kappa - |x|$ is odd,
$P(x) = q^{|x|}(1-q)^{\kappa-|x|} + q^\kappa > 0$; if $\kappa - |x| = 2r \ge 2$,
$P(x) = q^{|x|}\bigl((1-q)^{2r} - q^{2r}\bigr) \ge 0$ because $q \le 1/2$.
(ii) A law with product proper marginals has all Walsh coefficients except the top one equal to
those of $\mathrm{ind}$, so it is $\mathrm{ind} + t\chi_{\mathrm{top}}$ for a real $t$. $P(1,\dots,1) = 0$ forces
$t = -(-1)^\kappa q^\kappa$, and then the atom $x$ with $|x| = \kappa - 2$ has
$P(x) = q^{\kappa-2}\bigl((1-q)^2 - q^2\bigr) < 0$ when $q > 1/2$ (for $\kappa \ge 2$).
(iii) Draw $B \sim P$; independently draw $m_j \sim \nu(\cdot \mid n > 0)$, and set $n_j = B_j m_j$.
On a proper subset $S$ the $B_j$ are i.i.d. Bernoulli$(q)$, so the $n_j$, $j \in S$, are i.i.d. with
law $(1-q)\delta_0 + q\,\nu(\cdot\mid n>0) = \nu$. All $n_j > 0$ iff $B = (1,\dots,1)$, of probability $0$.
(iv) $\nu(\{n>0\}) \le \mathbb{E}\, n_0 = \lambda = (p-1)^\kappa/(\kappa^\kappa p^{\kappa-1}) < p/\kappa^\kappa \le 1/2$.
A fact of type (a)-(b) holds for $\Lambda$ because it is determined by the $(\kappa-1)$-marginals,
which are those of $\nu^{\otimes\kappa}$; and $\Lambda(\text{all } n_j > 0) = 0$. For the joint factorial
moments: $\binom{M_S}{m} = \sum_{m_1 + \dots + m_r = m}\prod_{j \in S}\binom{n_j}{m_j}$ and each term with
$m \le \kappa - 2$ involves at most $\kappa-2$ coordinates. $\square$

*Remarks.* (1) This is the case needed of Benjamini-Gurel-Gurevich-Peled, Proposition 26, as
cited in `rem:two-level-threshold-size`; the paper can now state it without the citation. (2) The
law also shows that the $\kappa^\kappa/2$ figure is sharp for Bernoulli-type information: above it
($q > 1/2$) every $(\kappa-1)$-wise independent law has $P(\text{all}) \ge q^\kappa - \min_x \mathrm{ind}(x) > 0$,
which is why TH9's certificate can fire only above $\kappa^\kappa/2$. (3) Sanity check:
`square_gap_checks.py` part A verifies (i) in exact rationals for $\kappa = 3,\dots,6$ at
$q = 1/4, 1/2$ (nonnegative, total $1$, all proper marginals independent, $P(\text{all}) = 0$) and
finds a negative atom at $q = 2/3$, as (ii) predicts.

### Theorem 2 (no $p$-uniform algebraic construction; Chebotarev barrier) [proved]

Let $\kappa \ge 3$, let $K$ be a number field and $D \subseteq K^{2\kappa}$ a finite set of configurations
$(\alpha,\beta)$. Let $L$ be the compositum of $K(\zeta_\kappa)$ with the fields $K\bigl((\alpha_j+\beta_i)^{1/\kappa}\bigr)$
over all $(\alpha,\beta) \in D$ and all $(i,j)$ with $\alpha_j + \beta_i \ne 0$ (any choice of roots).
Let $\mathcal{P}$ be the set of primes $p$ that split completely in $L$ and divide no denominator of
any coordinate of any element of $D$. Then:

(i) every $p \in \mathcal{P}$ satisfies $p \equiv 1 \pmod\kappa$, and $\mathcal{P}$ has positive natural density,
namely $1/[\tilde L:\mathbb{Q}]$ for the Galois closure $\tilde L$ of $L$. If $K$ is Galois over $\mathbb{Q}$ and $D$ is
stable under $\mathrm{Gal}(K/\mathbb{Q})$ (arranged by enlarging $K$ to its Galois closure and $D$ to its
conjugates), then $L$ itself is Galois over $\mathbb{Q}$ and $[L:\mathbb{Q}] \le [K:\mathbb{Q}]\,\varphi(\kappa)\,\kappa^{|D|\kappa^2}$;

(ii) for $p \in \mathcal{P}$, every prime $\mathfrak{p}$ of $K$ above $p$ has residue field $\mathbb{F}_p$, and for every
$(\alpha,\beta) \in D$ the reduction $(\bar\alpha,\bar\beta) \in \mathbb{F}_p^{2\kappa}$ modulo $\mathfrak{p}$ is not a
two-level contraction at $(p,\kappa)$, for any coset generator; nor is any row or column
permutation of it.

Consequently, no finite family of configurations defined over number fields, used with any
rule for choosing among them and any rule for choosing $\xi$, gives $p \notin E_2(\kappa)$ for all
$p \equiv 1 \pmod\kappa$ above a threshold: the exceptions have relative density at least
$\varphi(\kappa)/[L:\mathbb{Q}]$ among primes $\equiv 1 \pmod\kappa$.

*Proof.* (i) $\mathbb{Q}(\zeta_\kappa) \subseteq L$, and a prime splits completely in $\mathbb{Q}(\zeta_\kappa)$ iff
$p \equiv 1 \pmod\kappa$. A prime splits completely in $L$ iff it splits completely in the Galois
closure $\tilde L$, and by the Chebotarev density theorem those primes have density
$1/[\tilde L:\mathbb{Q}]$; removing finitely many primes (denominators) changes nothing. If $K$ is Galois
and $D$ is Galois-stable, the set $U$ of nonzero cells is $\mathrm{Gal}(K/\mathbb{Q})$-stable, so
$F(X) = \prod_{u \in U}(X^\kappa - u)$ has coefficients in $\mathbb{Q}$, and $L$ is the compositum of the Galois
extension $K(\zeta_\kappa)$ with the splitting field of $F$, hence Galois. The degree bound is
$[K(\zeta_\kappa):K] \le \varphi(\kappa)$ and at most $\kappa$ for each of the at most $|D|\kappa^2$ Kummer generators.
(ii) Let $p \in \mathcal{P}$, $\mathfrak{p} \mid p$ in $K$, and $\mathfrak{P} \mid \mathfrak{p}$ in $L$. Complete splitting gives
$\mathcal{O}_L/\mathfrak{P} = \mathbb{F}_p$, hence also $\mathcal{O}_K/\mathfrak{p} = \mathbb{F}_p$, and $\mathcal{O}_K/\mathfrak{p} \hookrightarrow \mathcal{O}_L/\mathfrak{P}$ is the
identity of $\mathbb{F}_p$. Take a cell $u = \alpha_j + \beta_i \in K$. If $u \ne 0$ and $u$ is a $\mathfrak{p}$-unit, then
$u^{1/\kappa} \in L$ is a $\mathfrak{P}$-unit and $\bar u = (\overline{u^{1/\kappa}})^\kappa$ with $\overline{u^{1/\kappa}} \in \mathbb{F}_p^\times$,
so $\bar u \in Q_0$. If $\mathfrak{p} \mid u$ or $u = 0$, then $\bar u = 0$. So every cell of $(\bar\alpha,\bar\beta)$ lies in
$Q_0 \cup \{0\}$. Now suppose $(\bar\alpha,\bar\beta)$ satisfied (R) for some generator $\xi$, or more
generally $\bar\alpha_j + \bar\beta_i \in Q^\circ_{c_{ij}}$ for a pattern $c$ that is a Latin square (every row and
column of $c$ is a permutation of $\mathbb{Z}_\kappa$; the patterns $-(\sigma(i) + \tau(j))$ are such), with some
cell nonzero. In row $0$ at most one entry $c_{0j}$ equals $0$, so at least $\kappa - 1 \ge 2$ cells of
row $0$ lie in $Q^\circ_{c_{0j}} \cap (Q_0 \cup \{0\}) = \{0\}$, say cells $(0,j)$ and $(0,j')$ with $j \ne j'$. Then
$\bar\alpha_j = -\bar\beta_0 = \bar\alpha_{j'}$. For every $i$ the cells $(i,j),(i,j')$ then have the same value, lying in
$Q^\circ_{c_{ij}} \cap Q^\circ_{c_{ij'}} = \{0\}$ (Latin row), so $\bar\beta_i = -\bar\alpha_j$ for all $i$: all $\bar\beta_i$ are
equal. Then for each $j''$ the cells $(i,j'')$, $i \in \mathbb{Z}_\kappa$, all equal $\bar\alpha_{j''} + \bar\beta_0$ and lie in
the $\kappa$ distinct sets $Q^\circ_{c_{ij''}}$ (Latin column), hence vanish. So every cell is zero,
contradicting the nonzero cell. $\square$

*Scope and remarks.* (1) The theorem covers every "explicit" construction whose data are
algebraic numbers independent of $p$: small integers (the analogue of the Graham-Ringrose
intervals $\{1,\dots,n_p-1\}$ that give Paley cliques when all primes below $n_p$ are
residues), roots of unity ($\alpha_j = \zeta^j A$, $\beta_i = \zeta^i B$; TH2 §3.5, TH5 §2), and any
finite menu of such data selected by a rule depending on $p$. In particular the number-theoretic
lower bounds for the Paley clique number, which hold for infinitely many $p$ only, have no
all-$p$ analogue here, for a structural reason and not merely for lack of a proof.
(2) It does not cover per-prime searches, such as the $T_W$ ansatz $\beta_i = \xi^{-i} - 1$ with
the $\alpha_j$ then found in $\mathbb{F}_p$, or the transpose-symmetric family of TH5 §5, where the
unknowns are solved anew at each $p$. Those are counting problems and fall under §3-§4.
(3) Illustration (`square_gap_checks.py` part C, `extra_checks.py` part C$'$): among primes
$p \equiv 1 \pmod 4$ below $4\cdot10^5$, $2$ is a quartic residue at a fraction $0.246$ (Chebotarev:
$1/4$), and $2,3,5$ all are at $0.0136$ ($1/64 = 0.0156$); $p = 196681$ has every prime up to $13$,
hence every integer up to $16$, in $Q_0$, so at this prime every configuration of integers
in $[1,16]$ has constant pattern. For $\kappa = 5$: $0.199$ vs $1/5$ and $0.0069$ vs $1/125$.

### Proposition 3 (structure of the frequencies $S_e$) [proved]

With the convention (F3):

(a) If some row or some column of $e$ has exactly one nonzero entry, then $S_e = 0$.

(b) If $\sum_{i,j} e_{ij} \not\equiv 0 \pmod\kappa$, then $S_e = 0$.

(c) Let the support of $e$ be the 4-cycle $\{(i,j),(i,j'),(i',j),(i',j')\}$ with entries
$e_1, e_2, e_3, e_4$ in that order (so $e_1,e_2$ share row $i$ and $e_3,e_4$ share row $i'$), all
nonzero, and $\sum e \equiv 0$. If $e_1 + e_2 \not\equiv 0$ then

$$S_e = p^{2\kappa-4}\cdot p(p-1)\,\chi^{e_2+e_4}(-1)\,J(\chi^{e_1},\chi^{e_2})\,J(\chi^{e_3},\chi^{e_4}),
\qquad J(\psi,\psi') = \sum_{w \in \mathbb{F}_p}\psi(w)\psi'(1-w),$$

and if $e_1 + e_2 \equiv 0$ (hence $e_3 + e_4 \equiv 0$) then $S_e = p^{2\kappa-4}\cdot p^2(p-1)$. In both
cases $|S_e| = p^{2\kappa-2}(p-1)$.

(d) The total contribution of all 4-cycle frequencies to the term-by-term certificate is at
most $\binom{\kappa}{2}^2(\kappa-1)^3\,p^{2\kappa-1} < \kappa^7 p^{2\kappa-1}/4$, which is below $\varepsilon\,p^{2\kappa}$
as soon as $p > \kappa^7/(4\varepsilon)$.

*Proof.* (a) Say row $i$ has its only nonzero entry at $(i,j)$. Summing over $\beta_i$ with the other
coordinates fixed, the row contributes $\sum_{b}\chi^{e_{ij}}(\alpha_j + b)\prod_{j' \ne j}\chi^0(\alpha_{j'} + b) =
\sum_{u \in \mathbb{F}_p}\chi^{e_{ij}}(u) = 0$, since $\chi^{e_{ij}}$ is a nontrivial character and $\chi^{e_{ij}}(0) = 0$.
Columns likewise, summing over $\alpha_j$.
(b) For $\lambda \in \mathbb{F}_p^\times$, $\chi^s(\lambda u) = \chi^s(\lambda)\chi^s(u)$ holds for all $u$ (both sides vanish at
$u = 0$ when $s \ne 0$, and both are $1$ when $s = 0$). Substituting $(\alpha,\beta) \to \lambda(\alpha,\beta)$ gives
$S_e = \chi(\lambda)^{\sum e} S_e$; choose $\lambda$ with $\chi(\lambda)^{\sum e} \ne 1$.
(c) The $2\kappa - 4$ coordinates outside the cycle contribute a factor $p$ each. For the rest, fix
$A = \alpha_j$, $B = \alpha_{j'}$ and sum row $i$ over $b = \beta_i$. If $A \ne B$, substitute $b + A = (A - B)w$,
so $b + B = (A-B)(w-1)$:
$\sum_b \chi^{e_1}(b+A)\chi^{e_2}(b+B) = \chi^{e_1+e_2}(A-B)\,\chi^{e_2}(-1)\,J(\chi^{e_1},\chi^{e_2})$
(the terms $w = 0, 1$ vanish on both sides). Row $i'$ gives
$\chi^{e_3+e_4}(A-B)\chi^{e_4}(-1)J(\chi^{e_3},\chi^{e_4})$. The product contains $\chi^{\sum e}(A - B) = 1$, and
there are $p(p-1)$ ordered pairs $A \ne B$. If $A = B$, row $i$ gives $\sum_b \chi^{e_1}(b+A)\chi^{e_2}(b+A) =
\sum_{u \ne 0}\chi^{e_1+e_2}(u)$, which is $p - 1$ if $e_1 + e_2 \equiv 0$ and $0$ otherwise. When
$e_1 + e_2 \not\equiv 0$ the diagonal vanishes and the formula follows. When $e_1 + e_2 \equiv 0 \equiv e_3 + e_4$:
$J(\chi^a,\chi^{-a}) = \sum_{w \ne 0,1}\chi^a\bigl(w/(1-w)\bigr) = -\chi^a(-1)$, so each row's off-diagonal factor
is $\chi^{e_2}(-1)\cdot(-\chi^{e_1}(-1)) = -1$, the off-diagonal total is $p(p-1)$, the diagonal total is
$p(p-1)^2$, and the sum is $p^2(p-1)$. The modulus statement uses $|J(\psi,\psi')| = \sqrt p$ for
$\psi,\psi',\psi\psi'$ nontrivial.
(d) Choose two rows and two columns ($\binom\kappa2^2$ ways) and nonzero entries with $\sum e \equiv 0$
(at most $(\kappa-1)^3$ ways); each has $|S_e| \le p^{2\kappa-1}$. $\square$

*Remarks.* (1) Part (c) is the exact form of TH3 §2's observation "$\max|S_e|/p^5 \to 1$ on cycle
supports" at $\kappa = 3$ (and of TH2 §3.3's "$\approx (p-4)p^4$", which used the strict convention
$\chi^0(0) = 0$ and so differs in lower order). Checked by brute force over $\mathbb{F}_p^4$ at
$(\kappa,p) = (3,7),(3,13),(4,13),(5,11),(6,13)$ for both sub-cases, agreement to $10^{-11}$
(`square_gap_checks.out` B, `extra_checks.out` B$'$); frequencies with $\sum e \ne 0$ and
path-supported frequencies vanish to $10^{-12}$.
(2) The point of (c)-(d): the 4-cycle frequencies are exactly as large as Weil allows, so no
Katz, Deligne or additive-combinatorial estimate can shrink them, and they do not need
shrinking. By (a) the surviving frequencies are those whose support has every row and column
of degree $0$ or $\ge 2$; that excludes only a fraction $\le 2\kappa\cdot\kappa(\kappa-1)\kappa^{-\kappa}$ of all
$\kappa^{\kappa^2}$ frequencies. So the term-by-term certificate still carries $\kappa^{\kappa^2}(1-o(1))$
frequencies of (near-)full support. Their multiplicity alone forces $p \ge \kappa^\kappa$ even if each
had the ideal square-root size $p^\kappa$ ($\kappa^{-\kappa^2}\cdot\kappa^{\kappa^2}p^\kappa < p^{2\kappa}\kappa^{-\kappa^2}$ iff
$p > \kappa^\kappa$), and O1 shows that the ideal size fails for the row-complete supports.

### Proposition 4 (polynomial method) [proved]

(a) *Chevalley-Warning and Ax-Katz.* The natural polynomial system for (R),
$w_{ij}^\kappa = z_i z_j(\alpha_j + \beta_i)$ ($i,j \in \mathbb{Z}_\kappa$), has $\kappa^2$ equations of degree $\kappa$ in
$\kappa^2 + 2\kappa$ unknowns; $\sum\deg = \kappa^3 > \kappa^2 + 2\kappa$ for every $\kappa \ge 2$, so Chevalley-Warning
does not apply, and the Ax-Katz exponent $\lceil(\kappa^2 + 2\kappa - \kappa^3)/\kappa\rceil \le 0$ gives no
divisibility. Eliminating $(\alpha,\beta)$ instead gives $(\kappa-1)^2$ linear conditions on the $w_{ij}^\kappa$,
degree sum $\kappa(\kappa-1)^2 > \kappa^2$ for $\kappa \ge 3$. More fundamentally, any argument whose
hypotheses are uniform over all finite fields $\mathbb{F}_p$ with $p \equiv 1 \pmod\kappa$ would give
$E_2(\kappa) = \emptyset$, which is false for $4 \le \kappa \le 9$ (appendix §`app:s2-scope`) and for
$\kappa = p-1 \ge 4$ (appendix: $p \in E_2(p-1)$).

(b) *Combinatorial Nullstellensatz.* Let $\zeta = \xi^h$ and
$F(\alpha,\beta) = \prod_{i,j}\prod_{m \ne -(i+j)}\bigl((\alpha_j+\beta_i)^h - \zeta^m\bigr)$. Then $F(\alpha,\beta) \ne 0$ iff all
coset conditions of (R) hold (zero cells allowed), and $\deg F = \kappa^2(\kappa-1)h = \kappa(\kappa-1)(p-1)$.
Alon's theorem needs grids $S_j, T_i \subseteq \mathbb{F}_p$ with $\sum_j(|S_j| - 1) + \sum_i(|T_i| - 1) = \deg F$,
and the left side is at most $2\kappa(p-1)$. So the theorem is inapplicable for $\kappa \ge 4$. For
$\kappa = 3$ all grids must equal $\mathbb{F}_p$, and the required coefficient of $\prod_j\alpha_j^{p-1}\prod_i\beta_i^{p-1}$
equals $(-1)^{2\kappa}\sum_{(\alpha,\beta) \in \mathbb{F}_p^{2\kappa}}F(\alpha,\beta) = \sum_{\text{solutions}}F(\alpha,\beta)$ in $\mathbb{F}_p(\zeta)$; it is
nonzero only if solutions exist, so the Nullstellensatz certifies nothing that is not already
assumed (and $E_2(3) = \emptyset$ anyway, `cor:app-s2-small`). Reducing $F$ modulo
$(\alpha_j^p - \alpha_j, \beta_i^p - \beta_i)$ does not change this coefficient.

*Proof.* (a) is the degree count and `app:s2-scope`. (b) For $u \ne 0$, $u^h \in \mu_\kappa$ and
$u^h = \zeta^m$ iff $u \in Q_m$; for $u = 0$ every factor is $-\zeta^m \ne 0$. The coefficient identity:
for a polynomial of degree $\le n(p-1)$ in $n$ variables, $\sum_{x \in \mathbb{F}_p^n}\prod x_k^{a_k}$ is $(-1)^n$ if
every $a_k$ is a positive multiple of $p-1$ (forcing all $a_k = p-1$ under the degree bound) and
$0$ otherwise. $\square$

### Lemma 5 (several coset generators) [proved]

For generators $\xi$ and $\xi' = \xi^u q$ ($\gcd(u,\kappa) = 1$, $q \in Q_0$), the map of
`app:s2-contraction` is a bijection between solutions of (R) for $\xi$ and for $\xi'$, so the counts
agree exactly. The patterns $-u(i+j)$, $u \in \mathbb{Z}_\kappa^\times$, are $\varphi(\kappa)$ distinct patterns in the
orbit of $-(i+j)$ under row and column permutations; a configuration realizes at most one of
them. Hence the number of configurations that are a contraction for some generator is
$\varphi(\kappa)N(p)$, and any first- or second-moment threshold computed for the union differs from
the one for a single $\xi$ by a factor in $[\varphi(\kappa)^{-1/(2\kappa-2)}, 1] \subseteq [\kappa^{-1/(2\kappa-2)}, 1]$ on the
scale $\kappa^{(\kappa+1)/2}$. Any pattern-uniform certificate for the union is subject to O1 unchanged.

*Proof.* The bijection is `app:s2-contraction`. Distinct $u$ give distinct patterns because
$\kappa \ge 2$; a configuration has one pattern. The count scales by $\varphi(\kappa)$, and the first
moment on $\mathbb{F}_p^{2\kappa-2}$ is $p^{2\kappa-2}\varphi(\kappa)\kappa^{-(\kappa^2-1)}$, whose unit crossing moves by the
stated factor. $\square$

### Proposition 6 (no Harris/FKG inequality for the column events) [proved]

For every $\kappa \ge 2$ and every prime $p \equiv 1 \pmod\kappa$, $\Pr_y[n_j > 0] > 0$ for each $j$, while
$\Pr_y[\text{all } n_j > 0] = 0$ exactly when $p \in E_2(\kappa)$. Hence no inequality
$\Pr[\bigcap_j\{n_j > 0\}] \ge c\prod_j\Pr[n_j > 0]$ with $c > 0$ independent of $p$ holds for all primes
of a $\kappa$ with $E_2(\kappa) \ne \emptyset$ (all $4 \le \kappa \le 9$, and $\kappa = p - 1$); the same for the
$\kappa^2$ cell events $\{\alpha_j + \beta_i \in Q_{-(i+j)}\}$ under uniform $(\alpha,\beta)$ (TH5 §3.3).

*Proof.* Pick $x \in Q_0$ and $y_i \in Q_{-i} - x$ for $i \ge 1$ (nonempty, $|Q_{-i}| = h \ge 1$); then
$x \in X_0(y)$. The other columns follow by $X_j(y) = \xi^{-j}X_0(\xi^j y)$. The second statement
is (F2). $\square$

## 3. The brief's approaches, one by one

Each item states what the route can produce and which rigorous statement stops it.

1. **Second moment or Janson over structured witness families.** A second-moment certificate
   needs a probability space in which the number $N_{\mathcal{W}}$ of valid witnesses is a random
   variable with computable first and second moments. (i) If the randomness is $\beta$ (uniform or
   any law derived from the uniform joint law of the column counts) and the witnesses are
   columns or functions of at most $\kappa-1$ columns, Theorem 1(iv) applies: nothing below
   $\kappa^\kappa/2$. (ii) If the randomness is $(\alpha,\beta)$ uniform and the witnesses are cells, Janson's
   inequality and every forest-supported statistic see only the independent model, and TH5
   §3.3 refutes them at the exceptional primes ($\mu_G = 122$ at $(\kappa,p) = (6,859)$ with $N = 0$);
   Proposition 6 adds that no positive-association inequality survives either. (iii) If the
   randomness is the pattern $c$ (Parseval over $\mathbb{Z}_\kappa^{\kappa\times\kappa}$), the certificate is
   pattern-uniform and O1$'$ gives $\gtrsim e\,\kappa^{\kappa-1/2}$. (iv) A structured family of witnesses
   $w_k(\beta) = (\alpha^{(k)}(\beta),\beta)$ with explicit $\alpha^{(k)}$ has $\mathbb{E}\, N_{\mathcal{W}} = \sum_k \Pr_\beta[w_k \text{ valid}]$,
   where each term is a $\kappa^2$-cell event in $\kappa-1$ variables; for linear $\alpha^{(k)}$ TH5 §2 classifies
   these and finds no family whose square-root certificate beats exponent $\kappa$ by more than
   $1/(\kappa-1)$; and by Theorem 2, $\alpha^{(k)}$ cannot be $p$-uniform algebraic data. No rigorous
   barrier covers arbitrary nonlinear witness families; none was found that helps.

2. **Many coset generators simultaneously.** Lemma 5: exactly the same count for each
   generator, a factor $\varphi(\kappa)$ on the union, no change of exponent, and O1 unchanged.

3. **Katz-type bounds over hyperplanes or varieties.** TH3 §2 shows the general-position
   hypothesis of Katz's nonsingular theorem fails for every $S_e$ (the arrangement
   $\alpha_j + \beta_i = 0$ is the graphic arrangement of $K_{\kappa,\kappa}$). Independently of that, any
   bound $|S_e| \le B_e$ used term by term is pattern-uniform, so O1 applies: no $p \le 2^{-1/(\kappa-1)}\kappa^\kappa$.
   Even the ideal $|S_e| \le p^\kappa$ for all $e \ne 0$ gives only $p > \kappa^\kappa$ (Proposition 3, Remark 2),
   and it is false (Proposition 3(c): 4-cycle frequencies have size $p^{2\kappa-1}$). Rojas-León's
   singular estimates (TH3 §7(iii)) remain unread; they would still be term-by-term bounds.

4. **Stepanov's method.** It proves the one-variable Weil bound and, in the Hanson-Petridis
   form, upper bounds for $A + B \subseteq Q_0 \cup \{0\}$ ($|A||B| \le h + |B \cap -A|$; TH3 §5). Any
   lower-bound certificate it yields is a Weil-type bound on complete one-variable sums, hence
   enters only through the brackets of Theorem 1(iv) or the terms of O1. It supplies no
   multi-variable cancellation and no $\kappa$-column fact.

5. **Sum-product and additive energy of the cosets.** The subgroup has order $h = (p-1)/\kappa$,
   so $|Q_0| \ge p^{1-o(1)}$. The Bourgain-Glibichuk-Konyagin and Shkredov-type theorems, as far
   as this pass knows them (no new text was read; TH3 §5 and TH5 §4 record what was read),
   improve on Weil for subgroups of order at most $p^{c}$ with $c < 1$; for $|H| = p/\kappa$
   the two-fold statistics ($r_{Q_a+Q_b}(d)$, $E(Q_a,Q_b;Q_c,Q_d)$) are the cyclotomic numbers,
   determined to within $O(\kappa^2\sqrt p)$ by `lem:app-s2-cyclo`, and the error is genuinely of that
   order because the Jacobi sums entering have modulus exactly $\sqrt p$. In the cell graph these
   statistics are exactly the 4-cycle frequencies of Proposition 3(c): exact, sharp, and
   harmless. Forest statistics are exact (TH5 Lemma 3.1). So additive combinatorics of
   two-fold sums adds no information beyond what the expansion already has exactly, and the
   missing information is the $\kappa^{\kappa^2}$ dense frequencies, equivalently the $\kappa$-column
   statistic $\mathbb{E}\prod_j n_j = N(p)/p^{\kappa-1}$ (TH3 O3).

6. **Chevalley-Warning with restricted variables; Combinatorial Nullstellensatz.**
   Proposition 4. Restricting $\alpha_j$ or $\beta_i$ to cosets or unions of cosets adds conditions and
   removes none (TH9 Lemma 6).

7. **Explicit algebraic constructions (number-field data, small integers, roots of unity).**
   Theorem 2: excluded for all-$p$ statements, with positive density of exceptions.

## 4. The square-root heuristic, labelled [heuristic]

For a family with $v$ free parameters over $\mathbb{F}_p$ and $c$ distinct coset conditions, the first
moment is $p^v\kappa^{-c}$ and a square-root-cancellation certificate has error of order $p^{v/2}$,
so it certifies only $p > \kappa^{2c/v}$ while the first moment is above $1$ from $p > \kappa^{c/v}$.
After normalisation the full problem has $v = 2\kappa-2$ and $c = \kappa^2 - 1$, so $c/v = (\kappa+1)/2$:
the heuristic threshold is $\kappa^{(\kappa+1)/2}$ (the observed scale) and the square-root threshold
is $\kappa^{\kappa+1}$, which is $T_A$'s exponent. Linear sub-families cannot lower $c/v$: a proportionality
between two cell functions on the family is one linear relation, which lowers $v$ and $c$ by one
each, so $c - v = (\kappa-1)^2$ is preserved and $c/v$ grows. This is TH6 §6.2 and TH5 §2. Two
reasons it is not a theorem: (i) cells constant on the family are pre-tuned, not counted, and the
difficulty is moved into the pre-tuning (e.g. $T_W$: column $0$ constant, $\kappa$ conditions on each
$\alpha_j$, threshold $\kappa^{2\kappa}$); (ii) a term-by-term certificate's error is $\sum_{e\ne0}|S_e|$, which
is of order $\kappa^c p^{v/2}$ only when the mass $\sum_e|S_e|^2 = \kappa^c\sum_{\text{patterns}}(N_c - \mu)^2$ is spread
evenly over the frequencies; when it concentrates, the L$^1$ norm is smaller and O1 is the
relevant rigorous statement. The rigorous instances are O1 (term-by-term) and Theorem 1(iv)
($\beta$-averaging); the heuristic is recorded only to explain why $T_A$ is where it is.

## 5. Comparison with $T_A$, the observed scale, and the data

| $\kappa$ | largest known $p \in E_2(\kappa)$ | $1.5\,\kappa^{(\kappa+1)/2}$ | $\kappa^\kappa/2$ (Thm 1 barrier) | $2^{-1/(\kappa-1)}\kappa^\kappa$ (O1) | $(\kappa-1)\kappa^\kappa \approx T_A$ |
|---|---|---|---|---|---|
| 4 | 53 | 48 | 128 | 203 | 768 |
| 5 | 181 | 188 | 1563 | 2628 | $1.25\cdot10^4$ |
| 6 | 859 | 794 | $2.33\cdot10^4$ | $4.06\cdot10^4$ | $2.33\cdot10^5$ |
| 7 | 3221 | 3602 | $4.12\cdot10^5$ | $7.34\cdot10^5$ | $4.94\cdot10^6$ |
| 8 | $\ge 14281$ | $1.74\cdot10^4$ | $8.39\cdot10^6$ | $1.52\cdot10^7$ | $1.17\cdot10^8$ |
| 9 | $\ge 18199$ | $8.86\cdot10^4$ | $1.94\cdot10^8$ | $3.55\cdot10^8$ | $3.10\cdot10^9$ |

(`square_gap_checks.out` D; data from `main.tex` and `app:s2-scope`.) No threshold is claimed
here, so nothing can conflict with the data. The two rigorous barriers lie between the observed
scale and $T_A$: every certificate of the two excluded kinds must have its threshold above the
third or fourth column, and $T_A$ is within a factor $\kappa$ of both; the conditional $6\kappa^\kappa+1$ of
TH9 (for $\kappa \ge 729$) is within a factor $12$ of the Theorem 1 barrier. The known members of
$E_2(\kappa)$ sit a factor $\kappa^{(\kappa-1)/2}$ below the barriers, which is the square gap.

Numerical sanity checks run (all passed; outputs in the artifact folder):
Theorem 1(i)-(ii) in exact rationals, $\kappa = 3..6$; Proposition 3(a),(b),(c) by brute force at five
$(\kappa,p)$ pairs, both sub-cases of (c); Chebotarev densities for $\kappa = 4,5,7$ against $1/\kappa$ and
$\kappa^{-3}$; the table above.

## 6. What would suffice [conditional target, not proved]

Any proof of an exponent below $\kappa$ must supply a fact about all $\kappa$ columns jointly that
is false under $(\kappa-1)$-wise independence (Theorem 1), is not a term-by-term bound on the
expansion (O1), and is not a reduction of $(\alpha,\beta)$ to $p$-uniform algebraic data (Theorem 2).
The single quantity that carries it is $\mathbb{E}_y\prod_j n_j = N(p)/p^{\kappa-1}$ or
$\mathbb{E}_y\prod_j\mathbf{1}[n_j > 0]$. TH6 Conjecture 6.4 (there is an absolute $c$ with
$p^{2\kappa-2}q^{\kappa^2-1} \ge c \Rightarrow p \notin E_2(\kappa)$, $q = (h+1)/p$) is the statement whose proof
for a single $\kappa \ge 8$ at $p \in (C\kappa^{(\kappa+1)/2}, \kappa^\kappa/2]$ would be the first step; the data
force $c \ge 156$ (TH6 §6.4). The closest classical analogue, the clique number of the Paley
graph, has the same gap, open since Erdős-Szekeres; Theorem 2 shows that the only known
unconditional progress there (intervals of small integers, infinitely many $p$) cannot give an
all-$p$ statement for (R).

## 7. Claim gates that stay false

- The square gap is closed: **false**. No exponent below $\kappa$ is proved, unconditionally or
  conditionally beyond what TH2/TH9 already record.
- Any threshold $T = o(\kappa^\kappa)$ is proved: **false**. $T_A$, $T_W$, $T_S$ and Table
  `tab:app-s2-thresholds` are unchanged.
- The conditional $6\kappa^\kappa + 1$ ($\kappa \ge 729$) is now unconditional: **false** (TH2 Theorem 5 is
  still only proved in the reports, not in the paper).
- Theorem 2 bounds $E_2(\kappa)$ or lowers any threshold: **false**. It restricts a class of proofs.
- Theorem 1 changes any number in the paper: **false**. It replaces a citation by a proof.
- Any statement here about Katz, Rojas-León, Bourgain-Glibichuk-Konyagin or Shkredov is a
  reading of their papers: **false**. Only the published hypotheses as recorded in TH3 (Katz,
  Hanson-Petridis, read there) and the general regime of subgroup size are used; no new text
  was read (no network).

## 8. Proposed paper text (AI-checked, pending human review; NOT applied)

(a) `appendix-schedule2.tex`, Remark `rem:app-s2-joint-moments`, replace the clause "The law of
Benjamini, Gurel-Gurevich and Peled cited in Remark~\ref{rem:two-level-threshold-size}, which
agrees ..." by:

> Such a law is explicit. Let $q = \Pr[n_0 > 0] \le \mathbb{E}\,n_0 < p/\kappa^\kappa \le 1/2$. On $\{0,1\}^\kappa$ put
> $P(x) = q^{|x|}(1-q)^{\kappa-|x|} - (-1)^{\kappa-|x|}q^\kappa$; it is a probability law because $q \le 1/2$, its
> marginal on every proper subset of coordinates is the product Bernoulli$(q)$ law (the
> correction is a multiple of the top Walsh character), and $P(1,\dots,1) = 0$. Drawing $B \sim P$
> and setting $n_j = B_j m_j$ with $m_j$ independent copies of the law of $n_0$ conditioned on
> $n_0 > 0$ gives a law on $(n_0,\dots,n_{\kappa-1})$ that agrees with independent copies of the law of
> $n_0$ on every $\kappa-1$ columns and gives probability $0$ to every column being nonempty
> (\file{research/audits/reviews/2026-11-05-rees-square-gap-attack.md}, Theorem~1). Conversely no
> such law exists when $q > 1/2$.

(b) `main.tex`, Remark `rem:two-level-threshold-size`, after "...where the analogous gap is a
long-standing open problem.":

> The number-theoretic lower bounds for that clique number (intervals of small integers, valid
> for infinitely many primes) have no all-prime analogue here: for $\kappa \ge 3$, any finite set of
> configurations with coordinates in a number field reduces to a two-level contraction at no
> prime that splits completely in the field generated by the $\kappa$-th roots of its cells, a set
> of primes of positive density (Chebotarev; \file{research/audits/reviews/2026-11-05-rees-square-gap-attack.md},
> Theorem~2; AI-checked, pending human review).

## 9. Artifacts (`2026-11-05-rees-square-gap-attack/`)

- `square_gap_checks.py` / `.out`: Theorem 1 (exact rationals), Proposition 3 (brute force,
  generic sub-case, vanishing cases), Chebotarev fractions to $6\cdot10^4$, the table of §5.
- `extra_checks.py` / `.out`: Proposition 3(c) degenerate sub-case at five $(\kappa,p)$; Chebotarev
  fractions to $4\cdot10^5$ and the prime $196681$.
- Both run in under a second with `/opt/anaconda3/bin/python -I` under `nice -n 19`.
