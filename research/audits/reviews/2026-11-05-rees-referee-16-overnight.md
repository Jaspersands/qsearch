# Referee 16 (2026-11-05, overnight pieces): independent adversarial check

Scope: the five pieces added to `docs/papers/rees-hsp/` overnight on 2026-11-05.
Each was checked from scratch (statement, every step, quantifiers, edge cases) before
any cited report was opened; the reports were consulted afterwards only to see whether
a gap I had found is filled there. Line numbers are those of the working copy at the
time of reading (main.tex shifted by two lines during the pass because another agent
was editing `app:s2-scope`; the quoted text is exact, so grep for it).

Numerical checks (my own code, `/opt/anaconda3/bin/python -I`, scratchpad files
`chkA2.py`, `chkB.py`) are summarised in Section 3.

## 1. Summary table

| # | Piece | Class | Location | One-line description |
|---|-------|-------|----------|----------------------|
| F1 | 1 (chains, rem tower-scope) | Imprecision | appendix-schedule2.tex:554 | Union-target variant of Lemma refine drops the hypothesis that the input classes lie in R |
| F2 | 1 (rem joint-moments) | Imprecision | appendix-schedule2.tex:427 | "most of this loss can be removed" asserted; the result is conditional on an unproved bound |
| F3 | 1 (main summary) | Imprecision | main.tex:683 | "this method cannot push below kappa^kappa/2" stated flatly; the appendix marks the key step as not proved |
| F4 | 1 (local, Prop cyclotomic (i)) | Style | appendix-schedule2.tex:~672 | "c = b - epsilon" where the computation gives c = b + epsilon; equal only because 2 epsilon = 0 |
| F5 | 3 (r_run) | Imprecision | main.tex:631 | "the following deterministic variant" is introduced under the prime-power hypothesis but later bounded "for every kappa_d >= 2" |
| F6 | 3 (r_run) | Imprecision | main.tex:631 | "a single run, with no restart, when kappa is prime": a restart trigger can occur; what is true is that no second run starts |
| F7 | 3 (r_run) | Imprecision | main.tex:631 | "a subgroup of a cyclic group of order dividing p-1" gives only log_2(p-1) restarts, not nu; the subgroup is of the Hall pi-subgroup |
| F8 | 4 (Theorem W) | Style | main.tex:1233 | Role of the hypothesis p > 2 delta-hat not stated (exactness needs only p > max((nu-1)delta-hat, delta-hat); 2 delta-hat is for the randomised test); nu and D collide with earlier notation |
| F9 | 2 (rem fc-witness-h3 (a)) | Style | appendix-free-coordinate.tex:315 | Upper bound on j*_h is justified by one clause ("a Minkowski vector ... gives short representatives"); the Babai step that gives the constant c_h phi^2/2 should be written |
| F10 | 2 (rem fc-witness-h3 (b)) | Style | appendix-free-coordinate.tex:317 | Constant (2 log_2 p + 5)^{j*} does not follow from sigma_p + 1 <= ceil(2 log_2(p-1)) + 5 literally; harmless inside O(.) |

Errors: 0. Gaps: 0. Imprecisions: 6. Style: 4.

No claim in the five pieces was refuted. Every numerical value I recomputed agrees
with the paper (Section 3).

## 2. Findings

### F1 (Imprecision) appendix-schedule2.tex:554, Remark rem:app-s2-tower-scope

Current text:

> Relax the cell condition to $\alpha_j + \beta_i \in \{0\}\cup\bigcup_{k\in K}Q^{(D)}_{k-i-j}$ for a set $K \ni 0$, keep $\alpha_0 + \beta_0 \in Q^{(D)}_0$, and ask the inputs only for one coefficient of class $0$.

The lemma's construction still needs $\beta_{i(b)}$ to be defined for every nonzero
input coefficient, that is, every input $D$-class must lie in $R$. "only for one
coefficient of class $0$" reads as dropping that hypothesis (it replaces the stronger
input requirement "$c^\nu_{b_\nu} = 1$", not the class requirement). Replacement:

> Relax the cell condition to $\alpha_j + \beta_i \in \{0\}\cup\bigcup_{k\in K}Q^{(D)}_{k-i-j}$ for a set $K \ni 0$, keep $\alpha_0 + \beta_0 \in Q^{(D)}_0$, keep the requirement that the $D$-classes of the inputs lie in $R$, and ask the inputs only for one coefficient of class $0$ in place of a coefficient equal to $1$.

### F2 (Imprecision) appendix-schedule2.tex:427, Remark rem:app-s2-joint-moments

Current text:

> The union bound over the $\kappa$ columns in Proposition~\ref{prop:app-s2-TA}(i) costs a factor of order $\kappa$ in the threshold, and most of this loss can be removed (\file{...threshold-9.md}, ...).

The removal is proved in the remark only for $6 \le \Lambda \le \sqrt{8\kappa}$ and
$\kappa \ge 729$; the range $\Lambda \ge \sqrt{8\kappa}$ rests on the cited, unproved
central-moment bound, and the remark itself says "If that bound is right". The opening
sentence should carry the same hedge. Replacement:

> The union bound over the $\kappa$ columns in Proposition~\ref{prop:app-s2-TA}(i) costs a factor of order $\kappa$ in the threshold. The cited reports argue that most of this loss can be removed for large $\kappa$, as follows (\file{...threshold-9.md}, ...); the part of the argument that this remark reproduces is the moment bracket and its consequence for $6 \le \Lambda \le \sqrt{8\kappa}$.

### F3 (Imprecision) main.tex:683, Remark rem:two-level-threshold-size

Current text:

> ... lowers this to $6\kappa^\kappa + 1$ for $\kappa \ge 729$, an $O(\kappa^\kappa)$ threshold that this method cannot push below $\kappa^\kappa/2$, since there no lower bound valid for every law of the column counts that satisfies the same Weil-controlled moment brackets is positive (Remark~\ref{rem:app-s2-joint-moments}; AI-checked, pending human review).

The barrier statement depends on the step "these products of one-column brackets lie
inside the brackets for $S$", which Remark rem:app-s2-joint-moments explicitly marks
"this step is not proved here. Granting it, ...". The main-text sentence should say
"argued". Replacement:

> ... lowers this to $6\kappa^\kappa + 1$ for $\kappa \ge 729$, an $O(\kappa^\kappa)$ threshold; the same reports argue, and this paper does not prove, that this method cannot push below $\kappa^\kappa/2$, because there no lower bound valid for every law of the column counts that satisfies the same Weil-controlled moment brackets is positive (Remark~\ref{rem:app-s2-joint-moments}; AI-checked, pending human review).

### F4 (Style) appendix-schedule2.tex:~672, proof of Proposition prop:app-s2-cyclotomic (i)

Current text:

> Writing $z = x - y$ with $x \in Q^\circ_0$ and $y \in Q^\circ_b$ is possible with $x = 0$ exactly when $c = b - \varepsilon$,

With $x = 0$ one has $z = -y \in Q_{b+\varepsilon}$, so the computation gives
$c = b + \varepsilon$. The statement is nevertheless correct because
$(-1)^2 = 1$ forces $2\varepsilon \equiv 0 \pmod\kappa$, hence $\varepsilon = -\varepsilon$;
this fact is used silently here and again in "$c \ne b - \varepsilon$ into $v \ne \varepsilon$".
Replacement:

> Writing $z = x - y$ with $x \in Q^\circ_0$ and $y \in Q^\circ_b$ is possible with $x = 0$ exactly when $c = b + \varepsilon = b - \varepsilon$ (as $2\varepsilon = 0$ in $\mathbb{Z}_\kappa$, since $(-1)^2 = 1$),

### F5 (Imprecision) main.tex:631, Remark rem:is-runtime

Current text:

> When $\kappa = q^e$ is a prime power, the following deterministic variant makes at most $e \le \log_2\kappa$ runs, and a single run, with no restart, when $\kappa$ is prime (AI-checked, pending human review).

Later in the same remark: "For every $\kappa_d \ge 2$ the variant makes at most
$r_{\mathrm{run}} = \dots$ runs". The variant is well defined for every $\kappa \ge 2$
(the check "the $\pi$-parts lie in one coset of $\langle\eta\rangle^\kappa$" and the
discrete logarithms do not use that $\kappa$ is a prime power), but the text introduces
it only under the prime-power hypothesis. Replacement:

> For every $\kappa \ge 2$ the following deterministic variant makes at most $r_{\mathrm{run}}$ runs, where $r_{\mathrm{run}}$ is defined below; when $\kappa = q^e$ is a prime power this is $e \le \log_2\kappa$ runs, and a single run when $\kappa$ is prime (AI-checked, pending human review).

I verified the bound $r_{\mathrm{run}} = \nu - \min_q v_q((p-1)/\kappa_d)$ independently:
with $|H_\pi| = \prod_q q^{a_q}$, $\kappa = \prod_q q^{e_q}$ and $|H_1| = \prod_q q^{h_q}$,
the check succeeds as soon as the $q$-part of $\langle\eta\rangle$ has order at least
$q^{h_q+e_q}$ for every $q$; a worst-case chain enlarges all other primes to $a_{q'}$
first, giving at most $\nu - \sum_q h_q - \min_q(a_q - e_q - h_q) \le \nu - \min_q(a_q - e_q)$
runs, and if the check never succeeds before $\langle\eta\rangle = H_\pi$ the count
$1 + \nu - \sum_q h_q$ is again at most $\nu - \min_q(a_q - e_q)$ because then some
$h_q > a_q - e_q$. The bounds $1 + \max_q v_q(p-1) \le r_{\mathrm{run}} \le \nu$ for
two or more prime factors also hold (algebraically, and numerically for
$\kappa \in \{6,10,12,15,30,36,60\}$, $p < 20000$).

### F6 (Imprecision) main.tex:631, Remark rem:is-runtime

Current text:

> and a single run, with no restart, when $\kappa$ is prime

When $|H_1| < |H_\pi|$ the first run can meet a coefficient whose $\pi$-part lies
outside $\langle\eta_1\rangle$; that is a restart trigger. What the argument gives is
that after this trigger the check succeeds and the witness is read off the first $a+1$
columns, so no second run starts. Replacement:

> and a single run when $\kappa$ is prime: a restart can be triggered at most once, and the check that follows it returns the witness without a second run

### F7 (Imprecision) main.tex:631, Remark rem:is-runtime

Current text:

> The algorithm of Theorem~\ref{thm:is-import} makes at most $\nu+1$ runs, since each restart strictly enlarges a subgroup of a cyclic group of order dividing $p-1$.

A subgroup of a cyclic group of order dividing $p-1$ can be enlarged $\Omega(\log p)$
times; the bound $\nu$ needs the subgroup to lie in $H_\pi$. Replacement:

> The algorithm of Theorem~\ref{thm:is-import} makes at most $\nu+1$ runs, since each restart strictly enlarges a subgroup of the Hall $\pi$-subgroup $H_\pi$ of $\Fp^\times$, a cyclic group whose order has exactly $\nu$ prime factors counted with multiplicity.

### F8 (Style) main.tex:1233, paragraph after Remark rem:filters (Theorem W)

Current text:

> Suppose that a bound $\hat\delta \ge \delta(F)$ is known, that $p > \max((\nu-1)\hat\delta, 2\hat\delta)$, and that $p^K$ exceeds the formal degree of $F$. Then $t \mapsto R_F(\exp(tA)u)$ has degree less than $p$ for every $A \in \mathcal{L}$, so the first-order Lie method applied to $R_F$ is exact

I re-derived exactness: ($\Leftarrow$) if the Lie derivative $D_AR_F$ vanishes, the
polynomial $t \mapsto R_F(\exp(tA)u)$, of degree at most $(\nu-1)\hat\delta < p$, has zero
derivative and is constant; ($\Rightarrow$) if $\exp(A) \in H$ then $\exp(kA) \in H$ for
all $k$, so that polynomial has $p$ roots and vanishes, and $D_AR_F$, of degree at most
$\hat\delta < p$, vanishes on $\Fp^{KD}$ and hence identically. This uses only
$p > \max((\nu-1)\hat\delta, \hat\delta)$. The factor $2$ is needed for the randomised
kernel computation (a nonzero polynomial of degree $\le \hat\delta$ vanishes at a uniform
point with probability at most $\hat\delta/p < 1/2$), which the text does not say.
Also $\nu$ here is a nilpotency index while $\nu$ in Remark rem:is-runtime is a count of
prime factors, and $D$ here is a number of variables while $D$ is a divisor of $\kappa$
in Appendix app:s2-tower and a digit set in Appendix app:schedule3. Replacement (first
sentence):

> Suppose that a bound $\hat\delta \ge \delta(F)$ is known, that $p > \max((\nu-1)\hat\delta, 2\hat\delta)$ (the first term makes the Lie method exact, the second is used only by the randomised kernel computation below), and that $p^K$ exceeds the formal degree of $F$.

and add "(in this paragraph $\nu$ and $D$ have the meanings just defined)" after the
definitions of $\nu$ and $D$.

### F9 (Style) appendix-free-coordinate.tex:315, Remark rem:fc-witness-h3 (a)

Current text:

> every element of $D_j$ is the image of a signed sum of at most $2^j$ powers of $\zeta_h$, and a Minkowski vector of the prime $(p,\zeta_h-\omega)$, $\omega \in \Fp$ of order $h$, gives short representatives of every residue.

The upper bound $j^*_h \le \lceil\log_2(c_h\varphi(h)^2p^{1/\varphi(h)}/2)\rceil + 1$ is
right, but the clause hides the step that produces the constant. I checked it as
follows: Minkowski's theorem for the $\ell_\infty$ norm gives $0 \ne v \in \mathfrak p$
with $\|v\|_\infty \le p^{1/\varphi}$; rounding a residue representative against the
basis $v\zeta_h^i$ ($0 \le i < \varphi$) of the sublattice $(v) \subseteq \mathfrak p$
leaves a representative of $\ell_1$-norm at most
$\tfrac12\sum_i\|v\zeta_h^i\|_1 \le \tfrac12\varphi c_h\|v\|_1 \le c_h\varphi^2p^{1/\varphi}/2$;
and $D_j$ contains every signed sum with at most $2^{j-1}$ positive and $2^{j-1}$
negative terms (induction, using that $D_{j-1}$ is symmetric for $j \ge 2$). Replacement:

> every element of $D_j$ is the image of a signed sum of at most $2^j$ powers of $\zeta_h$, and conversely $D_j$ contains every signed sum with at most $2^{j-1}$ positive and $2^{j-1}$ negative terms; for the upper bound, Minkowski's theorem gives $0 \ne v$ in the degree-one prime $\mathfrak p = (p,\zeta_h-\omega)$, $\omega \in \Fp$ of order $h$, with $\|v\|_\infty \le p^{1/\varphi(h)}$, and rounding against the basis $v\zeta_h^i$ of $(v) \subseteq \mathfrak p$ gives every residue a representative of $\ell_1$-norm at most $c_h\varphi(h)^2p^{1/\varphi(h)}/2$.

### F10 (Style) appendix-free-coordinate.tex:317, Remark rem:fc-witness-h3 (b)

Current text:

> Its arity is $M_d = O((2\log_2p+5)^{j^*_h}g_d^{\,1+j^*_h}\log(1/\tau))$

From $\sigma_p \le \lceil 2\log_2(p-1)\rceil + 4$ one gets $\sigma_p + 1 \le 2\log_2(p-1) + 6$,
which exceeds $2\log_2 p + 5$ for $p \ge 5$. The ratio is bounded by a constant
($\le e^{1/2}$ over $j^*_h \le \lceil\log_2\kappa_d\rceil$), so the $O(\cdot)$ is correct;
for readability replace $(2\log_2p+5)$ by $(2\log_2p+6)$, or write
$O((\sigma_p+1)^{j^*_h}\dots)$.

## 3. Checks performed (all agree with the paper)

Piece 1, Appendix app:s2-tower.
- Lemma lem:app-s2-refine: class bookkeeping $j + (-(i+j)) + i = 0$, the vanishing of the
  output relation, and $c'_{b_{\nu^\ast}} = \alpha_0+\beta_0$ re-derived; $\alpha$ must
  indeed run over all of $\mathbb{Z}_D$ and $\beta$ only over $R$.
- Theorem thm:app-s2-tower: induction, $P_{D_{t-1}} \to$ classes in $R_t$, division by
  $\alpha_0+\beta_0 \in P_{D_t}$, count of eliminations $\sum_t M/M_t \le M$, independence
  of $\xi$ via $u R_t = R_t$: all correct.
- Proposition prop:app-s2-step-threshold (i): $A = (r-1-r/D)D^r+1$ equals the coefficient
  of $\sqrt p$ in $r + D^rE_D(r,p)$; $W(D,D) = T_W(D)$; $W(D,2) < ((D-1)^2+1)^2$ reduces to
  $D^2-4D+2 > 0$. (ii): second-moment formula with rows restricted to $R$, $\Gamma \le 1$,
  the first-order expansion with remainder, and every numerical constant
  ($1.001$, $1.0005$, $0.5003$, $0.2502$, $0.1251$, $0.7225$, $0.1809$, $0.4312$) re-derived.
- Corollary cor:app-s2-tower: $4q^2\kappa^5 \le 4\kappa^7$, $T_A(q) \le q^{q+1}$, the
  $2^L$ case ($W(2^t,2)$, $t \ge 2$, so $D \ge 4$) and the $2^i3^j$ case ($36\kappa^5$).
- Finding the scalars: $A + rD^{r-1} = (r-1)D^r + 1$ and the $O(\kappa^5)$ count.
- Remark rem:app-s2-tower-scope: exhaustive search at $\kappa = 4$ over
  $E_2(4) = \{5,13,17,29,37,53\}$: no two-level contraction at any of them; tower
  $\mathrm{RC}(4;\{0,2\})$ exists at $17, 37, 53$; at $29$ union chains with
  $K = \{0,1\},\{0,3\}$ exist; nothing at $5, 13$. Matches $\{5,13\}$. Also $W(9,3) = 1.479\cdot10^6$.

Piece 1, Appendix app:s2-chains.
- Theorem thm:app-s2-chain: the induction (hockey-stick count $f_t(m)$, class of the
  round weights, back substitution $\tau_k$, final value $-\tau_0 \in U$, designated weight
  $1$) re-derived; $\binom{13}{3} = 286$, $1331$, $2541$ at $a = 10$.
- Proposition prop:app-s2-union-step: indicator expansion, character-sum cases
  (modulus $1$ for one index zero or $s+t = 0$, Weil otherwise), $\Delta_U$,
  $\sum_c\delta_{ij}(c) = 1 - p/|A_{ij}| < 0$, the ratio $1/N_1 + p^{-1}\sum_c\prod_i(1+\delta)$,
  the $j = 0$ bound, monotonicity of $\Psi_U$; (ii) constants $0.4989$, $1.0203$,
  $0.2996$, $0.1619$, $0.0522$, $0.73$; $G \le 1 + \ln D$, $H \le (1.2+\ln D)^2$.
- Corollary cor:app-s2-union-chain: all five terms of $\Theta^{\mathrm{cf}}_2$ traced to
  their sources; asymptotic bound at $\kappa = 16$ ($14.87 < 16.32$) and the
  $\kappa^{\kappa/2}$ comparison at $\kappa = 19$ ($27.81 < 27.97$); numerically
  $\min_k\Theta^{\mathrm{cf}}_2(5,k) = 2.205\cdot10^5$ ($k=4$),
  $\min_k\Theta^{\mathrm{cf}}_2(7,k) = 1.681\cdot10^6$ ($k=5$), and at $\kappa = 16, 19$
  the bound $4.05\kappa^2(\ln\kappa)^\kappa$ holds with the stated $k$.
- Remark rem:app-s2-chains-scope: $T_R(5,3) = 3780.8$, $T_R(7,3) = 30823.1$,
  $T_R(9,3) = 1.347\cdot10^5 < 135000$; union chain $\mathbb{Z}_5 \to \{0,u\} \to \{0\}$:
  step 2 fails at $p = 11$ for every $u$ and both steps succeed at $31, 41$ for every $u$;
  the barrier bound at $\kappa = 4$, $p = 17$, $h' = 2$ first drops below $1$ at $a' = 146$.

Piece 1, Appendix app:s2-local.
- Lemma lem:app-s2-two-rows, Proposition prop:app-s2-cyclotomic (i)-(iii) (pair counts
  $(\kappa-1)(\kappa-2)$ and $\kappa^2-3\kappa+3$, the bound $3(\kappa-1) + (\kappa-1)(\kappa-2)\sqrt p$,
  the inequality $(\kappa-1)(2\kappa-7)+2 > 0$ for $\kappa \ge 4$, "$p \ge 940$" at $\kappa = 7$),
  Lemma lem:app-s2-divisor ($\xi^{(p-1)/D}$ has order $D$; $Q_m \subseteq Q^{(D)}_{m \bmod D}$):
  all correct. Edge $\kappa = 2$: (ii) is vacuous and (i) never applies, consistent with
  $E_2(2) = \emptyset$. Numerically the largest prime to which (i) applies is
  $29, 11, 223, 71, 761, 163$ for $\kappa = 4,\dots,9$, the set is empty at $\kappa = 3$,
  and it contains every prime listed as having no chain. Consistency with
  Lemma lem:app-s2-divisor: $17 \in E_2(4)$ gives $17 \in E_2(8)$ (listed); $E_2(5) \subseteq E_2(10)$
  agrees with the $E_2(10)$ sweep.
- The subsection and main.tex:683 say that these results bound $E_2$ from below only and
  do not narrow the square gap: correct, and correctly labelled.

Piece 1, Remark rem:app-s2-joint-moments.
- Moment bracket re-derived from Lemma lem:app-s2-weil-count with $\ell = m$ over the
  $\kappa-1$ random rows; the use of the exact error term for $m > \kappa$ is legitimate
  (the lemma has no upper bound on $\ell$). $\eta_{\kappa-1} \ge 1$ at $p = \kappa^\kappa/2$
  for $3 \le \kappa \le 11$ (values $1.63, 7.7, 35, \dots$), and $\eta$ decreases in $p$.
  Conditional statements are marked conditional except as in F2, F3.

Piece 2, Remark rem:fc-zero-sum-arity (checked as the base of rem:fc-witness-h3).
- $D^{(j+1)} = D^{(j)} - D^{(j)}$ with $x = \lceil\alpha/2\rceil$, $x' = -\lfloor\alpha/2\rfloor$;
  recursion $N_j(n) = 1 + \sigma_p\sum_{e<n}N_{j+1}(e)$ (Wald); $\sigma_3 = 3$ and
  $N_0(n) = 1 + 3n(n+1)/2$ at $p = 3$; the bound $(\sigma_p+1)^{j^*}\binom{n+j^*+1}{j^*+1}$;
  $\sigma_p \le p$ via Cauchy--Davenport; the node's abort bound $\tau/2 + \tau/2$; the
  non-totality example; the degree comparisons $12$ vs $3$, $4$ vs $3$, $5$ vs $6$.

Piece 2, Remark rem:fc-witness-h3.
- (a) $|D_j| \ge \min(p, 2^jh+1)$, $j^*_h \le \lceil\log_2\kappa\rceil$; the Jacobi-sum
  count equals $m_{-c}$ of Lemma lem:app-s2-cyclo and is positive once
  $\sqrt p > (\kappa-1)(\kappa-2)+3$ ($3\kappa^2-12\kappa+16 > 0$); probability $1/(2\kappa)$
  once $\sqrt p \ge 2(\kappa-1)(\kappa-2)+4$ ($8\kappa^2-30\kappa+35 > 0$); lower bound via
  the lattice-point count $(2^{j+1}c_h+1)^{\varphi}$; upper bound as in F9.
  Computed: $j^*_3 = 1,1,2,2$ at $p = 7,13,19,31$; $j^*_4 = 1,2$ at $13,17$;
  $j^*_3 - \tfrac12\log_2p \in [-0.850, 0.562]$ for $p < 6000$ (inside the stated $[-0.85,0.60]$).
- (b) Rescaled form: expected columns $1 + \lceil\log_2p\rceil\frac{p}{p-1}\frac{n(n+1)}{2}$
  re-derived (each dimension-$n'$ block costs $n'p/(p-1)$ columns, $\lceil\log_2p\rceil$
  blocks per dimension, plus one base column); the split trial count gives failure
  $2^{-B}/M$ per entry; the binary digits replace the covering loop. The leading
  coefficient $\sigma_p^{j^*}/(1+j^*)!$ of $N_0$ is right.
- (c) The exponent $E = 1 + \sum_d(1+j_d)$ recomputed by my own code for every prime
  $p > c$ up to the threshold $\max_\kappa((\kappa-1)(\kappa-2)+3)^2$ (above which
  $E \le 2c-1$): $\max_{p>c}E = 3, 6, 8, 10, 13, 14, 16, 19$ for $c = 2,\dots,9$, attained
  at $p = 3, 7, 7, 11, 7, 31, 31, 19$; at $c = 9$ at $p = 19$ as stated. The error budget
  ($\tau_d$ sums to $\epsilon/9$; the $3\cdot2^{-B}$ terms arise only at $\Gamma_{\mathrm F}$
  nodes, so $N$ in $B$ is unchanged) is consistent with Lemma lem:fc-forest(b). The remark
  states correctly that $E$ is not comparable with $E_W(c)$, and main.tex:775 states
  correctly that at $c = 9$ no grade has $\kappa_d = p-1$.

Piece 3 (r_run): see F5--F7; the formula and both bounds verified algebraically and
numerically; prime-power case equals $e$ for $\kappa \in \{4,8,9,27\}$, $p < 3000$.

Piece 4 (Theorem W): see F8; exactness re-derived; the evaluation count
$O(d(d+\log(1/\epsilon))(\hat\delta+1))$ is consistent with interpolating
$t \mapsto R_F(u + tAu)$ (degree $\le \hat\delta$) at $\hat\delta+1$ points for each of
$d$ basis elements and $O(d+\log(1/\epsilon))$ random points; the choice
$\hat\delta = \lfloor(p-1)/\max(\nu-1,2)\rfloor$ is exactly the largest value allowed by
the hypothesis; the Moore-form and "superpolynomial $p$ for fixed $D$" consequences follow.
Labels "(proved)", "(computed)" and "AI-checked, pending human review" are present.

Piece 5 (SDE column counts).
- $M_J(a)$: $J = 2$ gives $(a+1)(a+2)/2$ and $J = 3$ gives $\lfloor(a+2)^2/4\rfloor + [a\ \mathrm{odd}]$
  for all $0 \le a < 50$ (algebraically for all $a$); $M_J(a) - a^2/(2(J-1)) \le 2.94a$ for
  $2 \le J \le 9$, $a < 200$, so "$+O(a)$" holds uniformly in $J$.
- $D_3(q) = \lfloor(q+2)^2/4\rfloor$ for $1 \le q \le 60$ (the maximum is attained at
  $k = q$ for $q \ge 4$, and $D_3(q) - D_3(q-2) = q+1$); $D_J(q) \le q^2/(2(J-1)) + q(1/(J-1)+5/2)$
  for $3 \le J \le 11$, $q < 200$.
- General position: $D_3(a) + a = \lfloor(a+2)^2/4\rfloor + a$; failure $\le 1/2$ per back
  substitution from $\rho_{\mathrm{pr}}\max(1/\mathcal{G}^*_3, \kappa/(p-1))$ at $p \ge 20a$
  ($\kappa = 2$) and $p \ge 162a$ ($\kappa = 3$); the pencil argument for $p + r - 1$
  columns; $O(a^2/\log a)$ with $J = \lceil\log_\kappa a\rceil$ and $\kappa^J \le \kappa a$;
  the prime condition $2aJ\kappa^J$ covers the required $\approx 1.56\,aJ\kappa^J$. The
  i.i.d. case ($p \ge 64a^2$, $p \ge \max(2750,1000a^2)$; failure $1/16$ and $8^{-k}$)
  checked against $M_3(a)$, $\Lambda \le \lceil a/2\rceil$ and $\mathcal{G}_3 \ge p/10$, $p/54$.
  Both remarks are labelled "conditional" / "AI-checked" and say that nothing else uses
  them and that the proved worst-case arity stays $(a+1)(a+2)/2$.

## 4. Verdict per piece

1. **appendix-schedule2 (tower, chains, local, joint moments).** Correct as stated. The
   theorems and propositions marked "proved here" are proved; the finite computations I
   could repeat ($\kappa = 4, 5$ chains; cyclotomic prime lists; $T_R$, $W$, $\Theta^{\mathrm{cf}}$;
   barrier at $a' = 146$) agree. Two hedging imprecisions (F2, F3) and one hypothesis
   dropped in a remark (F1); one notational slip that happens to be harmless (F4). Labels
   present; the lower bounds on $E_2$ are not presented as narrowing the square gap.
2. **appendix-free-coordinate remarks.** Correct as stated; all computed values and the
   exponents $E$ reproduced exactly. One proof clause could be expanded (F9) and one
   constant inside an $O(\cdot)$ is loosely derived (F10). Labels present.
3. **Composite-$\kappa$ restart count.** The formula $r_{\mathrm{run}} = \nu - \min_q v_q((p-1)/\kappa_d)$
   and the bounds $e$ and $1 + \max_q v_q(p-1) \le r_{\mathrm{run}} \le \nu$ are correct.
   Three imprecisions in the surrounding prose (F5--F7). The tightness constructions
   are not reproduced here and are labelled as proved for the default kernel vector.
4. **Theorem W.** Correct; the hypothesis is sufficient (and the first term is necessary
   for the stated proof). One style item (F8). Labels present, including a priority flag.
5. **SDE column counts.** All three counts are exactly right, including the edge cases
   $a = 0, 1$ (the i.i.d. statement restricts to $a \ge 2$, correctly). No finding beyond
   confirming the labels "conditional" and "AI-checked".

Overall: 0 Errors, 0 Gaps, 6 Imprecisions, 4 Style.

## 5. After forming the verdicts: cited reports

Consulted only for the items above. `2026-11-05-rees-is-restarts.md` (lines 150-154)
confirms that for prime $\kappa$ "the first trigger always collapses, so the single run
is never repeated" (F6: the paper's "with no restart" compresses this).
`2026-11-05-rees-threshold-7-check.md` (lines 145-146) records the same no-chain lists
I reproduced for $\kappa = 4, 5$. `2026-11-05-rees-application-4.md` (lines 181, 230)
uses Schwartz--Zippel over $\Fp$, which is where $p > 2\hat\delta$ enters (F8).
`2026-11-05-rees-s3-witness-h3-check.md` (line 78) states the Minkowski step at the
same level of detail as the paper (F9 stands). No cited report changes a verdict.
