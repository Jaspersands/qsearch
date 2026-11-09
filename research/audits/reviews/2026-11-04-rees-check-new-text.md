# Referee check of new Rees text (2026-11-04)

**Status: AI-checked, pending human review.** Independent referee pass by an AI
session on the paper text only (`docs/papers/rees-hsp/main.tex`,
`appendix-torsion-blackbox.tex`, `appendix-free-coordinate.tex`,
`appendix-codimension.tex`). No paper file was edited. Checks are in
`research/audits/reviews/2026-11-04-rees-check-new-text/` and run with
`/opt/anaconda3/bin/python <script>`; they can only falsify.

Severity scale: error (a stated claim is false), gap (a step needed by the
proof is missing), imprecision (true in substance but misstated, or a constant
or citation is off), typo.

(Report written incrementally; sections below are filled part by part.)

## Summary

No finding breaks a headline result (the query exponents, the chart cost
O_c(dk^2+k^4), Cor. fpt-r, Cor. codim(ii), the q_max count). The findings
are one false general statement (the E_W dichotomy, false at c = 13), one false
side claim in a lemma statement ("then k >= n"), three gaps (the Dirichlet step
behind that dichotomy; a worst-case trial cap in the free-coordinate route of
Cor. codim(ii); the poly(log p) solver factor in the time exponent of
Thm. bb-envelope), one typo, and imprecisions in constants and hypotheses.
The values E_W(c) = 5, 11, 23, 38, 56, 77, 107, 143 are correct. Part 4 has no
error.

| # | Severity | Location | One line |
|---|----------|----------|----------|
| 1.1 | error (statement; harmless where used) | `appendix-torsion-blackbox.tex`, Lemma tb-chart, "Let $Y \in ...$ ... then $k \ge n$" and Step 1, "In particular $|A| = ...$" | $k \ge n$ does not follow; $C_{3^{20}}$ |
| 2.1 | error (general statement) | Lemma tb-count-exponent, "Consequently $E_W(c) = E_1(c)$ if ..." | dichotomy false at $c = 13$ ($E_W = 323 = E_1 - 6$) |
| 2.2 | gap | proof of Lemma tb-count-exponent, "such primes exist by Dirichlet's theorem" | Dirichlet gives no prime below $104976$ |
| 2.3 | typo | same proof, "exceed $104976$ for $d \ge 3$" | $16\cdot3^8 = 104976$ exactly |
| 2.4 | imprecision | Prop. tb-count-gates(a), "each with $O_c(n_p(2b_M + A_c)) = O_c(\ell)$ multiplication calls" | it is $\Theta(\ell^2)$ for $C_{3^e}\times C_3^e$; conclusion survives |
| 2.5 | imprecision | Prop. tb-count-gates (H1) and its use in (a) | (H1) says $\ell^3$, the proof uses $(\log p)^3$ |
| 2.6 | imprecision | Prop. tb-count-gates(b) and Thm. bb-envelope(iii), "$O_c(s^c\ell^5)$ gates" | the $\operatorname{polylog}(1/\eta)$ factor of (H1) is dropped; $kd$ vs $2kd$ transforms |
| 2.7 | gap | Prop. tb-count-gates, final sentence, and Thm. bb-envelope, "the total time is $O_c(N^{E_W(c)+1+\max(3,\hat\beta_c)+o(1)})$" | the $\poly(\log p)$ solver factor is not $N^{o(1)}$ |
| 2.8 | imprecision | proof of Thm. bb-envelope(i), "and $t \le N + 5$" | needs $\log = \log_2$ in $N$ |
| 2.9 | imprecision | Thm. bb-envelope(iii), "Classical time is $O_c(s^c\ell^5 + \ell^6)$" and "at most $Q_f\cdot\ell^{\hat\beta_c}\poly(\log p)$" | weaker than / missing a factor of Prop. tb-count-gates(d) |
| 2.10 | imprecision | Lemma tb-count-grade, "one call of Theorem~\ref{thm:main} with error ..." | Thm. main is Schedule 1 only; the combined-rule count is Rem. combined-schedule |
| 3.1 | gap | `appendix-codimension.tex`, "Part (ii) from Theorem free-coordinate(iii)", "Each free-coordinate node draws at most ..."; main.tex Cor. codim proof, "its trial counts use the observed rank" | no rank guard, so the cap fails off the ideal support |
| 3.2 | imprecision | main.tex Cor. fpt-r(i), "(for coset-copy input this is argued, not proved)" | the proof's last sentences do prove it |
| 4 | none | Thm. uniform-compilation(iii), $q_{\max}$ | matches the instrument definitions |

## Part 1. Lemma tb-chart, route (R2), Proposition black-box(iv)

**What was re-derived.** Step 0 (Lyndon table: content grading, at most
$\binom{m}{\alpha}/m \le (m-1)!$ Lyndon words per content, order-preserving
relabelling) is correct. Step 1 ($B^{\perp\perp} = B$ over $\mathbb{Z}/M$,
$\ker Y = \ker\pi$, the bracket $[Yu,Yv] := Y[u,v]$ is well defined because
$\ker\pi$ is an ideal) is correct. Step 2: the membership proof (induction on
$v \in S_t$ at position $j_t$, with the case $v_{j_t} = 0$ covered by "any
lift ... is congruent to $\lambda_t$") and the construction ((H2) from
$\langle R\rangle = \langle r_{\rm new}\rangle + \langle R'\rangle$ and the
appended $p^{e-a}\cdot$pivot, which is zero at position $j$) are correct.
Step 3 (incremental rebuild from at most $k$ Howell rows plus one column, so
$q_0 \le k+1$), Step 4 (Smith form; $PA = \bigoplus_{i\in I} p^{a_i}(\mathbb{Z}/M)e_i$,
$\varepsilon_i = CQe_i$, $Y\tilde\varepsilon_i = \varepsilon_i$, coordinates by exact
division) and Step 5 ($O_c(r^2k) + O(r^3k) + O(m^2k^2)$) are correct, and the
totals give $O_c(dk^2 + k^4)$ once $r \le n \le k$. The multiplication count
$n\cdot 2b_e + (n-1)(m_+ + 2b_eq_+)$ per lift is correct. The $C_9\times C_3$
remark is correct.

**Checks.** `chart_check.py` implements Steps 2-5 literally. The Howell
construction and membership test agree with brute-force spans on 300 random
submodules of $(\mathbb{Z}/p^e)^k$ ($p^e \in \{9,27,25,8\}$, $k \le 3$), and (H2) holds.
On 27 random quotients $F/I$ of $F_{2,2}$ and $F_{3,2}$ over $\mathbb{Z}/9$,
$\mathbb{Z}/27$, $\mathbb{Z}/25$ (random ideals $I$, random generating $Y$ of
$I^\perp$ with $k = n+2$ rows), the output has $\sum e_i = \log_p|F/I|$,
$\ker(u\mapsto Yu) = I$ exactly (all $u$ enumerated), the coordinate map is onto
$\bigoplus\mathbb{Z}/p^{e_i}$, and the structure constants reproduce
$Y[u,v]$ on 200 random pairs each. The $C_9\times C_3$ remark is confirmed.
Output: `chart_check.out`.

### Finding 1.1 (error in the statement; harmless where the lemma is used)

*Location.* `appendix-torsion-blackbox.tex`, Lemma tb-chart, sentence "Let
$Y \in (\mathbb{Z}/M)^{k\times d}$ be a matrix whose rows generate
$(\ker\pi)^\perp$, as the samples of Lemma~\ref{lem:tb-kernel} do on its success
event; then $k \ge n$." and Step 1, sentence "In particular $|A| = |\pi(F)| = |G| = p^n$,
and $n \le \lfloor\ell/\log_2 p\rfloor \le k$ by unique encodings and the definition of $k$
in Lemma~\ref{lem:tb-kernel}."

*Failing step.* Rows generating $(\ker\pi)^\perp$ do not force $k \ge n$, and
Lemma tb-kernel's sample count is $t = \min(d,\lfloor\ell/\log_2p\rfloor) +
\lceil\log_p(2/\delta)\rceil$, which can be smaller than $n$ (inside Lemma tb-kernel
the letter $k$ denotes $\operatorname{d}((\ker\pi)^\perp) \le n$, the opposite
inequality). Smallest counterexample to the first clause: $G = C_{27}$, $p = 3$, $s = 1$,
$d = 1$, $Y = (1)$, so $k = 1 < n = 3$. Counterexample with Lemma tb-kernel's own count:
$G = C_{3^{20}}$, $\ell = 32$, $\eps = 1/3$, $\delta = \eps/(4\ell)$: $t = 1 + \lceil\log_3 768\rceil = 8 < n = 20$
(`count_checks.py`, item 8). The bound $r \le n \le k$ is what makes Steps 3-5 cost
$O(k^4)$, so the lemma's count is not proved under its stated hypothesis. In the uses
(Proposition black-box(iv), route (R2), Theorem bb-envelope) $k = \lfloor\ell/\log_2 p\rfloor
+ \lceil\log_p(8\ell/\eps)\rceil \ge n$, so nothing downstream changes.

*Fix.* In the statement replace
"Let $Y \in (\mathbb{Z}/M)^{k\times d}$ be a matrix whose rows generate $(\ker\pi)^\perp$, as the samples of Lemma~\ref{lem:tb-kernel} do on its success event; then $k \ge n$."
by
"Let $k \ge \lfloor\ell/\log_2 p\rfloor$ and let $Y \in (\mathbb{Z}/M)^{k\times d}$ be a matrix whose rows generate $(\ker\pi)^\perp$, as the $k$ samples of Proposition~\ref{prop:black-box}(iv) do on the success event of Lemma~\ref{lem:tb-kernel} (which needs only $\min(d,\lfloor\ell/\log_2 p\rfloor) + \lceil\log_p(2/\delta)\rceil \le k$ of them); then $k \ge n$."
In Step 1 replace "by unique encodings and the definition of $k$ in Lemma~\ref{lem:tb-kernel}" by "by unique encodings and the hypothesis on $k$".

**Route (R2) and Proposition black-box(iv).** The citations are correct: (R2) uses
the lemma for the presentation, the lifts, the section and $\bar\Phi = \bar\pi$; (iv)
quotes $O_c(dk^2+k^4)$, the conversion to $O_c(s^c\ell^2+\ell^4)$ under
$\log_2(8\ell/\eps) \le \ell$ (from $d \le 2s^c$ for $s \ge 2$, $d = 1$ for $s = 1$, and
$k \le \ell + \log_2(8\ell/\eps) + 1$) and $4n(2b_M + A_c)$ per coherent use, all of
which follow. No further error in Part 1.

## Part 2. Subsection app:tb-counts against Theorem bb-envelope

**What was re-derived and holds.** Lemma tb-count-grade: the three cases
($C_d = 1$; $(\kappa-1)g+1 \le (\kappa-1)(g+1)$ so $C_d = \kappa-1$;
$B_\kappa(g) = \kappa^{\kappa(\kappa-1)\lceil\log_2(\kappa+1)\rceil/2}(g+1)^{\kappa\lceil\log_2(\kappa+1)\rceil}$)
and $\lceil\log_p(12\ell/\eps)\rceil \le t$. Lemma tb-count-prime: call $j$ only if
$S_j \ne K_j$ with $|K_j| \ge p^j$, so $j \le n_p - 1$ and the socle has dimension
$\le n_p - j$; $\sum_j Q_{\rm core}(n_p-j) \le n_pQ_{\rm core}(n_p) = cK_c\varphi(n_p)$;
$4n'(2b_M + A_c)$ per local query. Proof of (i): $\varphi$ is superadditive
($\varphi(x)/x$ is nondecreasing), $\sum_p\varphi(n_p) \le \varphi(L) \le (L+t)(L+1)^{E}$,
and the exponent-$p$ chain $\le 2^E(L+t)(L+1)^{E-1}$ with $X \le 2L$. Proof of (ii):
$2kd(2b_M+A_c)$ for $k$ evaluations with cleanup, $\min(d,n_p)^2 \le dn_p \le dk$.
Proof of (iv): the four quarters sum to $\eps$ ($L \le \ell$ charts at
$\eps/(4\ell)$, $L \le \ell$ core calls at $\eps/(4\ell)$). Prop. tb-count-gates (c),
(d): $k \le 2\Lambda/\log_2 p$ (uses $\log_2 p \le \ell$), $b_M \le 2e_p\log_2 p$,
$k^2b_M^2 \le 16\Lambda^2e_p^2$, $k^4b_M^2 \le 64\Lambda^4e_p^2$, $\sum_pe_p^2 \le L^2$;
solver calls $\le (c-1)SP$; $N_{\rm instr} \le S(cP+1) \le 2Q_f^{\rm call}$.

**Checks.** `count_checks.py` (output `count_checks.out`): superadditivity of
$\varphi$ on an integer grid for $E \in \{1,2,5,11,23,38,143\}$, $t < 30$; the
summation chains of (i) and Lemma tb-count-prime on every partition of $L \le 12$;
$\log_2(9K_9) = 1205.99$ (paper: about $1206$); $k \le 2\Lambda/\log_2 p$ and
$b_M \le 2e\log_2 p$ on a grid. `ew_values.py` (output `ew_values.out`) computes
$E_W(c)$ exactly: $e_d(p)$ depends only on $p \bmod \operatorname{lcm}(2,\dots,c)$ and
the threshold interval of $p$, every (unit residue, interval) pair is enumerated as an
upper bound, and a prime witness is searched for the maximizing pairs (the search is
exhaustive on all finite intervals that can matter). Result: $E_W(c) = 5, 11, 23, 38,
56, 77, 107, 143$ for $c = 2,\dots,9$, exactly as stated, attained at the listed primes
$3, 7, 13, 61, 61, 421, 2521, 2521$ ($2521$ is prime, $841 = 29^2$), against
$E_1(c) = 5,11,23,38,56,77,109,145$. These values hold for every prime $p > c$ (they
are the maxima over all of them). Also $E_W(10) = 183$, $E_W(11) = 227$,
$E_W(12) = 275$ ($= E_1 - 2$, witnesses $2521$, $55441$), and $E_W(13) = 323$.

### Finding 2.1 (error in a general statement; the values for $c \le 9$ are right)

*Location.* `appendix-torsion-blackbox.tex`, Lemma tb-count-exponent, sentence
"Consequently $E_W(c) = E_1(c)$ if some prime $p < 1024$ satisfies
$\operatorname{lcm}(2,\dots,c) \mid p-1$, and $E_W(c) = E_1(c) - 2$ otherwise."

*Counterexample.* $c = 13$: $\operatorname{lcm}(2,\dots,13) = 360360 > 104976 = 16\cdot 3^8$,
so no prime $p < 104976$ has $\operatorname{lcm} \mid p-1$. A prime in $[1024,104976)$ then has
some $\kappa_d < d$ besides the two-level grade 2, and a prime $\ge 104976$ has grades 2
and 3 both two-level or linear (loss $\ge 2 + 4$). Exact enumeration gives
$E_W(13) = 323 = E_1(13) - 6$ (witness $p = 4324321$), not $E_1(13) - 2 = 327$. The
dichotomy holds for $c \le 12$ only.

*Fix.* Replace that sentence by:
"Consequently $E_W(c) = E_1(c)$ if some prime $p < 1024$ satisfies
$\operatorname{lcm}(2,\dots,c) \mid p-1$. Otherwise $E_W(c) \le E_1(c) - 2$, with equality if
some prime $p$ with $1024 \le p < 16\cdot 3^8 = 104976$ satisfies
$\operatorname{lcm}(2,\dots,c) \mid p-1$; such a prime exists for $c \le 12$ (for example
$2521$ for $c \in \{8,9,10\}$ and $55441$ for $c \in \{11,12\}$) and for no $c \ge 13$,
since then $\operatorname{lcm}(2,\dots,c) > 104976$."

### Finding 2.2 (gap in the proof)

*Location.* Proof of Lemma tb-count-exponent, "such primes exist by Dirichlet's
theorem, and $E_W(c)$, a maximum of finitely many values, is therefore $E_1(c) - 2$."

*Failing step.* Dirichlet's theorem gives infinitely many primes $\equiv 1 \pmod{\operatorname{lcm}}$,
not one in the bounded window $[1024, 104976)$; Finding 2.1 shows none exists for $c \ge 13$.

*Fix.* Replace by: "When such a prime exists, every prime loses at least $2$ and that
prime loses exactly $2$, so $E_W(c) = E_1(c) - 2$. Dirichlet's theorem does not supply
one, because the window is bounded; for $c \le 12$ the primes $2521$ and $55441$ are
checked directly." (Then append $55441$ to the list of witnesses if $c \le 12$ is
claimed, or restrict the "Consequently" sentence to $c \le 9$.)

### Finding 2.3 (typo)

*Location.* Same proof, "The thresholds $16\,d^{2d+2}$ equal $1024$ at $d = 2$ and
exceed $104976$ for $d \ge 3$".

*Fix.* "equal $1024$ at $d = 2$ and are at least $104976$ for $d \ge 3$, with
equality at $d = 3$".

### Finding 2.4 (imprecision; conclusion of (a) unaffected)

*Location.* Prop. tb-count-gates, proof of (a), "A leaf makes $c$ queries, each with
$O_c(n_p(2b_M + A_c)) = O_c(\ell)$ multiplication calls".

*Counterexample.* $G = C_{3^e}\times C_3^{\,e}$ (abelian, $p = 3 > c = 1$), minimal
$\ell = \lceil 2e\log_2 3\rceil$: the chart has $m = e+1$ basis elements and
$b_M = \lceil e\log_2 3\rceil$, so even $4m\cdot 2b_M$ is about $1.3\ell^2$
(`count_checks.py`, item 7: ratio to $\ell$ grows as $24, 44, 84, 165, 324$). In general
$n_pb_M \le \ell^2$, not $O(\ell)$.

*Fix.* "each with $O_c(n_p(2b_M + A_c)) = O_c(\ell^2)$ multiplication calls (as
$n_p, b_M \le \ell$)". The leaf total is still $O_c(\ell^3 + w)$ gates, so (a) stands.

### Finding 2.5 (imprecision in hypothesis (H1))

*Location.* Prop. tb-count-gates, "(H1) a single-coordinate quantum Fourier transform
over $\Fp$, or over $\mathbb{Z}/p^e$ on at most $\ell$ bits, to isometry error $\eta$
compiles into $O(\ell^3\operatorname{polylog}(1/\eta))$ gates", used in (a) as "a
transform over $\Fp$ costs $O((\log p)^3\operatorname{polylog}(\ell/\eps))$".

*Failing step.* (H1) as written gives only $O(\ell^3)$ per $\Fp$ transform; with
$O_c(n_p)$ transforms per slot that is $O_c(\ell^4)$, not the $O_c(\ell^3)$ that (a) needs.

*Fix.* "(H1) a single-coordinate quantum Fourier transform over $\Fp$, or over
$\mathbb{Z}/p^e$, on $b \le \ell$ bits, to isometry error $\eta$ compiles into
$O(b^3\operatorname{polylog}(1/\eta))$ gates".

### Finding 2.6 (imprecision in the chart gate count)

*Location.* Prop. tb-count-gates(b), "that is $O_c(s^c\ell^5)$ gates when
$\log_2(8\ell/\eps) \le \ell$", its proof "by~(H1), $\sum_p k\,d\,\ell^3 \le \dots$
gates", and Thm. bb-envelope(iii), "$\sum_{p>c}k\,d$ transforms over
$\mathbb{Z}/p^{e_p}$, in all $O_c(s^c\ell^5)$ gates".

*Failing step.* (H1) charges $\operatorname{polylog}(1/\eta)$ per transform, with
$\eta \le \delta/(2\cdot\#\text{transforms})$, $\delta = \eps/(4\ell)$, so
$\log(1/\eta) = \Theta(\log(s\ell/\eps))$; it is dropped. Also, Fourier sampling uses
one transform to prepare each uniform coordinate and one to read it out (the
convention of Thm. uniform-compilation(iii), which charges $n$ transforms to a
lifted-source preparation), so a sample has $2d$ transforms, not $d$.

*Fix.* In (b) and in Thm. bb-envelope(iii): "$2\sum_{p>c}k\,d$ transforms over
$\mathbb{Z}/p^{e_p}$, each to isometry error $\eta = \eps/(16\ell kd)$, in all
$O_c(s^c\ell^5\operatorname{polylog}(s\ell))$ gates when $\log_2(8\ell/\eps) \le \ell$".
The $N^{E_W(c)+4+o(1)}$ total is unchanged.

### Finding 2.7 (gap in the total-time exponent)

*Location.* Prop. tb-count-gates, final sentence "the total time is
$O_c(N^{E_W(c)+1+\max(3,\hat\beta_c)+o(1)})$" and its proof "\emph{Exponents.} $Q_f =
O_c(N^{E_W(c)+1})$ by~(i), ..."; the same claim in Thm. bb-envelope after (iv).

*Failing step.* The solver term is $Q_f\,\ell^{\hat\beta_c}\poly(\log p)\operatorname{polylog}(\ell/\eps)$
and $\log p$ can be as large as $\ell$ (a Sylow subgroup of prime order near $2^\ell$),
so $\poly(\log p)$ is $N^{\Theta(1)}$, not $N^{o(1)}$. The exponents paragraph never
bounds it. The claim may still be true by trading $\log p$ against $n_p \le \ell/\log_2 p$,
but that is not argued, and it needs the degree of $\poly(\log p)$ to be at most about
$E_W(c) + \hat\beta_c$.

*Fix.* Fold $\log p$ into $\hat\beta_c$. In (d) replace "running within
$M_d(a+1)^{\hat\beta_c}\poly(\log p)\operatorname{polylog}(\ell/\eps)$" by "running within
$M_d\bigl((a+1)\log_2 p\bigr)^{\hat\beta_c}\operatorname{polylog}(\ell/\eps)$" and
"$\le Q_f^{\mathrm{call}}\ell^{\hat\beta_c}\poly(\log p)\operatorname{polylog}(\ell/\eps)$, using
$n_p + 1 \le \ell$" by "$\le Q_f^{\mathrm{call}}(2\ell)^{\hat\beta_c}\operatorname{polylog}(\ell/\eps)$,
using $(n_p+1)\log_2 p \le 2n_p\log_2 p \le 2\ell$"; replace
"$Q_f\,\ell^{\hat\beta_c}\poly(\log p)\operatorname{polylog}(\ell/\eps)$" in the statement of (d)
by "$Q_f\,(2\ell)^{\hat\beta_c}\operatorname{polylog}(\ell/\eps)$", and in Thm. bb-envelope(iii)
"at most $Q_f\cdot\ell^{\hat\beta_c}\poly(\log p)$" by "at most
$Q_f\cdot(2\ell)^{\hat\beta_c}\operatorname{polylog}(\ell/\eps)$". The exponent then follows as
written. ($\hat\beta_c$ still exists: a solver time $\poly(M_d,\log p)$ with
$M_d \le K_c(a+1)^{e_d}$ is at most $O_c(M_d((a+1)\log_2p)^{D})$ for some $D$.)

### Finding 2.8 (imprecision)

*Location.* Proof of Thm. bb-envelope(i), "With $L \le \ell \le N$ and $t \le N + 5$".

*Failing step.* $t = \lceil\log_2(12\ell/\eps)\rceil \le \log_2\ell + \log_2(1/\eps) + 4.6$;
this is $\le N + 5$ only if the $\log$ in $N = s\ell + w + \log(1/\eps)$ is base 2
(with natural log, $\eps = e^{-1000}$, $s = 1$, $\ell = 2$, $w = 0$ gives $t = 1448 > N + 5 = 1007$).

*Fix.* In Thm. bb-envelope write "$N = s\ell + w + \log_2(1/\eps)$", or in the proof
write "$t \le 2N + 5$". The $O_c$ statements are unaffected.

### Finding 2.9 (imprecision: main text weaker than, or missing a factor of, the appendix)

*Location.* main.tex, Thm. bb-envelope(iii), "Classical time is
$O_c(s^c\ell^5 + \ell^6)$ bit operations for the charts, ..., and at most
$Q_f\cdot\ell^{\hat\beta_c}\poly(\log p)$ for the diagonal-equation solvers".

*Issue.* Prop. tb-count-gates(d) proves $O_c(s^c\ell^4 + \ell^6)$ (when
$\Lambda \le 2\ell$), and its solver term carries an extra
$\operatorname{polylog}(\ell/\eps)$ that the theorem omits.

*Fix.* "Classical time is $O_c(s^c\ell^4 + \ell^6)$ bit operations for the charts when
$\log_2(8\ell/\eps) \le \ell$, polynomial normal-form arithmetic per normalizer step,
and at most $Q_f\cdot(2\ell)^{\hat\beta_c}\operatorname{polylog}(\ell/\eps)$ for the
diagonal-equation solvers" (with Finding 2.7's definition of $\hat\beta_c$).

### Finding 2.10 (imprecision in a citation)

*Location.* Proof of Lemma tb-count-grade, "The call makes at most
$c(m + \lceil\log_p(12\ell/\eps)\rceil)\prod_d M_d$ queries by
Theorem~\ref{thm:main} with $\eps' = \eps/(4\ell)$".

*Issue.* Theorem main fixes Schedule 1 ($M_d = B_d(g_d)$); the count with the combined
arities is the recursion count of Section~\ref{sec:recursion} under
Remark~\ref{rem:combined-schedule} (which the theorem lists as a condition).

*Fix.* "... queries, by the count of Section~\ref{sec:recursion} ($m + \lceil\log_p(3/\eps')\rceil$
terminal samples, each of $\prod_d M_d$ lifted sources of $c$ queries) with the arities of
Remark~\ref{rem:combined-schedule} and $\eps' = \eps/(4\ell)$".

**No other error in Part 2.** In particular the per-prime caps, the superadditivity
step, the exponent-$p$ bound, the error split and the values of $E_W(c)$ for
$c = 2,\dots,9$ are correct, and every \ref in the subsection points to a statement that
says what is used (apart from 2.10).

Note on the brief: Theorem bb-envelope(ii) in the text read here contains no $C_{27}$
example. The cyclic group $C_{27}$ (and $C_{3^{20}}$) is used above as the smallest
counterexample in Finding 1.1; for $C_{27}$ with $s = 1$, $d = 1$ the chart counts of (ii)
are $\min(d,n_p)^2 = 1 \le dk$ and $r = m = 1$, consistent with the theorem.

## Part 3. Corollary fpt-r, Corollary codim(ii) and the new appendix paragraph

**Corollary fpt-r(i), re-derived.** $g_2 > \dots > g_c \ge 1$ gives $c \le r+1$ and
$g_d \le r$. For $p \ge c+2$, $\kappa_d = p-1$ would force $d = p-1 > c$, so
$\Gamma_0 = \emptyset$ and $t_{\rm S1} = 0$. At error $1/3$, $S = m + \lceil\log_p 9\rceil \le m+2$;
the bound $M_d \le (1+2\log_2c)g_d + 3\log_2(72(c-1)Sn_d/\eps) + 3$ of the proof of
Prop. fc-uniform(b) (from Lemma fc-choice with $\ln(p/\kappa_d) \ge \ln h \ge \ln 2$, which
I re-derived, including $\beta \le \tau$) becomes $M_d \le \alpha + 3\log_2 n_d$ at
$\eps = 1/3$; $2^\alpha \ge 16(216cS)^3c^2$ for $r \ge 1$; $\log_2(4\alpha c) \le \alpha$;
the induction $\log_2 n_d \le (d-2)\log_2(4\alpha c)$, $M_d \le (1+3c)\alpha \le 4\alpha c$;
$x^r \le \max(r^{2r}, 2^{16}, 2^x)$ (if $x \le r^2$ the first; if $x > r^2 \ge 16$ then
$r\log_2x < \sqrt x\log_2 x \le x$; otherwise $x^r < 2^{12}$), hence
$Q_1 \le 2^{O(r\log(r+2))}S^2$. The Hoeffding constant is right:
$\Pr[X \le R/2] \le \exp(-2R(1/6)^2) = e^{-R/18} \le \eps$ for $R = \lceil18\ln(1/\eps)\rceil$.
$N_{\rm instr} \le S((2c-1)P + 1) \le 2Q_1 \le 3Q_1$. The time bound uses
$\kappa_d^{g_d} \le (r+1)^r$, which holds on every branch because the observed rank is
always at most $g_d \le r$. All \ref targets (Thm. free-coordinate(iii),
Prop. fc-uniform(b), Lemma fc-choice, Lemma s3-law, Lemma copy-lift,
Thm. uniform-compilation) say what is used.

**Corollary fpt-r(ii).** $p = c+1 \le r+2$ gives $|G'| = p^r \le (r+2)^r$. The
amplification (certify $H' \le H$ by $f(x) = f(1)$ on generators, compute $|H'|$ from the
Lie subalgebra generated by the logarithms, output the largest certified $H'$) is correct.
The content of \cite[Theorem~11]{IvanyosMagniezSantha2001} was not checked (no external
access in this pass).

**Corollary codim(ii) and the appendix paragraph, re-derived.** For $p \ge 2k+1$ the
terminal has $c_J \le 2k-1 \le p-2$, so $\Gamma_0 = \emptyset$. With $g_d \le k(k+1)/2$,
$c_J \le 2k-1$, $S_J \le k(k+1)/2+2$: $M_d \le \alpha_J + 3\log_2 n_d$ and
$\log_2 n_d = O(k\log k)$, so every arity is $O(k^2\log(k+2))$ as the main text says (the
crude $4\alpha_Jc_J = O(k^3\log k)$ also suffices for the query bound). Per run
$c_JS_J(4\alpha_Jc_J)^{c_J-1} = 2^{O(k\log(k+2))}$, independent of $m$ and $p$. For
$p \le 2k$, $B \le \sqrt2 p^{k/2} + 2 \le 4(2k)^{k/2}$. $R = \lceil 18\ln(2/\eps)\rceil$ gives
$e^{-R/18} \le \eps/2$, the terminal share.

**Checks.** `count_checks.py` item 4: exact binomial tails at success probability $2/3$
are below $\eps$ (largest ratio $0.278$) for $\eps \in [10^{-6}, 0.33]$, and below $\eps/2$
for the codimension appendix's $R$; item 5: $\log_2(4\alpha c) \le \alpha$ for
$2 \le c < 200$, $c-1 \le r < c+40$, $S$ up to $10^{12}$; the $x^r$ inequality on a grid;
the induction on $M_d$, $n_d$; Lemma fc-choice ($\beta \le \tau$ exactly in rationals and the
size bound) on 1932 cases. `codim_arity.py` (output `codim_arity.out`): at the worst
terminal shape ($c_J = 2k-1$, $g_d = k(k+1)/2$ at every grade) $\log_2$ of the per-run
queries divided by $k\log_2(k+2)$ stays below $5.2$ for $k \le 200$ (crude bound below
$8.1$), and $\max_dM_d/(k^2\log_2(k+2)) \le 8.2$.

### Finding 3.1 (gap: worst-case trial cap off the ideal support)

*Location.* `appendix-codimension.tex`, paragraph "Part~(ii) from
Theorem~\ref{thm:free-coordinate}(iii)", sentence "Each free-coordinate node draws at
most $\lceil 2B\ln 2\cdot q^{-r}\rceil \le 2B\ln 2\cdot(2k-1)^k + 1$ trials, because its
observed rank $r$ is at most $a_d \le k$ (Lemmas~\ref{lem:fc-rref}(a)
and~\ref{lem:app-codim-ad})."; main.tex, proof of Cor. codim, "and its trial counts use
the observed rank, which is at most $a_d \le k$".

*Failing step.* Lemma fc-rref(a) gives $r \le a_d$ only on the ideal support (labels in
$K_d^\perp$). With approximate instruments a bank can have any rank up to $g_d$, which at
the terminal can be about $k^2/2$; then (F3) runs $T_r = \lceil 2B\ln2\,q^{-r}\rceil$ up to
about $(2k-1)^{k(k+1)/2} = 2^{\Theta(k^2\log k)}$ trials. The error budget of the same
appendix ("The running-time bounds therefore hold on every branch, including ... those
reached after an approximation error") then fails for this route, and the claimed
deterministic time bound $2^{O(k\log(k+2))}\cdot\poly$ is not proved (only an expected or
high-probability bound). Thm. free-coordinate(iii) has no rank guard; part (ii) has one
("abort if $r > u-1$").

*Fix.* In the appendix replace that sentence by:
"At every free-coordinate node of these runs add to (F2) the guard ``abort if $r > k$''. On
the ideal support $r \le a_d \le k$ (Lemmas~\ref{lem:fc-rref}(a) and~\ref{lem:app-codim-ad}),
so the guard never fires there and Lemmas~\ref{lem:fc-node} and~\ref{lem:fc-forest} hold
unchanged; on every branch, including those reached after an approximation error, each
free-coordinate node then draws at most $\lceil 2B\ln 2\cdot q^{-r}\rceil \le
2B\ln 2\cdot(2k-1)^k + 1$ trials."
In main.tex replace "and its trial counts use the observed rank, which is at most
$a_d \le k$" by "and its trial counts use the observed rank, which a guard (abort if
$r > k$; it never fires on the ideal support, where $r \le a_d \le k$) keeps at most $k$ on
every branch".

### Finding 3.2 (imprecision: status of coset-copy input)

*Location.* main.tex, Cor. fpt-r(i), "(for coset-copy input this is argued, not
proved)", against its proof, "The vote evaluates no oracle, so it also applies to
coset-copy input, where Lemma~\ref{lem:copy-lift} makes each lifted source from $c$ copies."

*Issue.* The proof states the extension as proved; the statement says it is not. The
missing step, if any, is that Thm. free-coordinate(iii) is stated for oracle input.

*Fix.* In the proof replace that sentence by "The vote evaluates no oracle. For coset-copy
input, Lemma~\ref{lem:copy-lift} makes each lifted source from $c$ copies, and the proof
of Theorem~\ref{thm:free-coordinate}(iii) uses only the exact lifted sources; since that
theorem is stated for oracle input, this extension is argued rather than proved."

**No other error in Part 3.** Cor. codim(ii) is otherwise correct as stated, and the new
appendix paragraph is consistent with Thm. free-coordinate(iii), Prop. fc-uniform,
Lemma fc-choice and Lemma fc-rref.

## Part 4. Theorem uniform-compilation(iii): $q_{\max}$

The instruments of the approximation item of Section~\ref{sec:recursion} are: each
lifted-source preparation (uniform address on the cover, $n$ coordinates, then $c$
evaluations and queries with uncomputed workspace: $n$ transforms); each merge node at
stage $d$ ($M_d$ complete central instruments, each a uniform central ancilla, controlled
central translations and a Fourier readout on the $g_d$ top coordinates, so $2g_d$
transforms; the uniform quotient address register on $G_{d-1}$, of dimension
$D_{d-1} = \sum_{k \le d-1}g_k$, so $D_{d-1}$ transforms; controlled right actions, no
transforms); and each final readout on $t\mathcal{L} \cong \Fp^m$ ($m$ transforms). So
$q_{\max} = \max(n, m, \max_d(2M_dg_d + D_{d-1}))$ bounds the transforms of one instrument,
$N_{\rm QFT} \le N_{\rm instr}q_{\max}$, and $\eta = \eps/(3N_{\rm instr}q_{\max})$ keeps the
total within $\eps/3$ by Lemma hybrid. **No error.** (Cosmetic: $m \le n$, so the $m$ in
the maximum is redundant. Thm. free-coordinate(iii) groups each node's $M_d$ central
instruments and its conversion as $M_d+1$ instruments; each has at most $\max(2g_d, D_{d-1})
\le q_{\max}$ transforms, so the same $\eta$ is valid there.)

## Reproduction

```
cd research/audits/reviews/2026-11-04-rees-check-new-text
/opt/anaconda3/bin/python -I ew_values.py      # E_W(c), c = 2..13 (5 s)
/opt/anaconda3/bin/python -I count_checks.py   # counting inequalities (45 s)
/opt/anaconda3/bin/python -I chart_check.py    # Lemma tb-chart Steps 2-5 (30 s)
/opt/anaconda3/bin/python -I codim_arity.py    # Cor. codim(ii) arities (<1 s)
```

All findings are AI-checked, pending human review.
