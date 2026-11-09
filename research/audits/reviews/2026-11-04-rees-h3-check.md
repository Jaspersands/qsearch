# Rees HSP: can hypothesis (H3) of prop:tb-count-gates be dropped?

4 November 2026. AI-only read of `docs/papers/rees-hsp/{appendix-torsion-blackbox,main}.tex`
(prop:tb-count-gates, lem:tb-sylow, thm:bb-envelope, lem:qft-mod and its proof, the paragraph
"Binary arithmetic and explicit transforms"), `theorems/rees_circuit_arith.py`,
`theorems/rees_qft_mod.py`, and the primary sources (Shor arXiv:quant-ph/9508027, Vedral-Barenco-Ekert
arXiv:quant-ph/9511018, Cleve-Ekert-Macchiavello-Mosca arXiv:quant-ph/9708016, AKS Annals 2004).
No .tex or .bib file edited, no commit. One finite check was run: the artifact
`2026-11-04-rees-h3-check/modexp_check.py` and its output `modexp_check.out`.
**Every claim below is AI-checked, pending human review.**

## Verdict

**(H3) can be discharged, with stated citations. But discharging it exposes a counting gap, so
item (c) has to change.**

* Every quantum block that a run of order finding needs is already built in the paper:
  * modular arithmetic modulo an odd integer, composite allowed. The adder, comparison, modular
    adder and shift-and-add multiplier in the proof of lem:qft-mod work for any odd modulus and
    are run there at N = 9, 25, 27. Primality is never used. `mod_double` needs N odd, and
    `ArithBuilder`'s "odd prime" guard is not on this path.
  * the approximate inverse transform over Z/2^t, in product form with CR_k, k > r, omitted.
    The step E in the proof of lem:qft-mod builds it and proves the error bound 2*pi*t*2^-r.
* The classical parts are standard: continued fractions; Shor's reduction of factoring to order
  finding (Shor 1997, Section 5); the 4/pi^2 and two-run bounds (CEMM 1998, Sections 5-6),
  which lem:tb-sylow(d) already uses; and AKS.
* The bound O(ell^3) per run is right. No polylog(1/eps) factor appears, because each run needs
  only constant precision.
* **The gap:** "one factorization per generator" in (c) and in lem:tb-sylow(d) is not one run.
  * A complete factorization of v < 2^{2 ell} with failure at most eps/(2s) needs up to
    T = O(ell + log(s/eps)) attempts, each a pair of order-finding runs.
  * The lemma never bounds this failure probability, and it spends the whole eps_pre/s on
    order finding.
  * The correct count for (c) is **O(s ell^3 (ell + log(s/eps)))**, not O(s ell^3 log(s/eps)).
  * The exponents do not change: s ell^4 = (s ell) ell^3 <= N^4, so (c) is still O(N^4) and
    the totals N^{E_W(c)+4+o(1)} and N^{E_W(c)+1+max(3,beta)+o(1)} stand.

"Discharged" therefore means: the circuits come from the paper's own blocks; the counts follow
from the block counts already stated (checked by computation, see below); the success-probability
lemmas are cited. As for (H2), general-width correctness of the blocks is the standard argued one,
not machine-checked.

## (1) Where (H3) is used, and what is run

* Uses: the statement of prop:tb-count-gates ("Assume ... (H3) below" and the (H3) sentence),
  proof (c) ("apply (H3)"), main.tex thm:bb-envelope(iii), the status sentence after it, and the
  proof sketch, which still says "(H2) and (H3)". That last one is stale after the (H2) edit.
  Nothing in (a), (b) or (d) uses (H3).
* What (c) runs, from lem:tb-sylow(d):
  1. **Order finding in the black box**, for each generator g_i. Out-of-place exponentiation
     k -> g_i^k, with z_{j+1} = z_j * (k_j ? g_i^{2^j} : 1) in fresh registers. The constants
     g_i^{2^j} come from classical squaring with the oracle. Then 2 ell + 1 control qubits, the
     inverse QFT over Z/2^{2 ell + 1}, and continued fractions. A pair succeeds with probability
     > 1/11. At most ceil(11 ln(s/eps_pre)) pairs are run. The test g^v = 1 is classical.
     * Cost per run: 2(2 ell + 1) = 4 ell + 2 oracle multiplications.
     * Plus O(ell^2) other gates: controlled loads of classical ell-bit constants, at most 2 ell
       CNOT/X per step, twice for uncompute, plus the copy-out.
     * Plus the transform, O(ell log ell).
     * So the paper counts oracle calls, already in thm(ii)'s O(s ell^2 + s ell log(s/eps))
       multiplications, plus O(ell^2) gates. This is *below* O(ell^3).
  2. **Factoring of integers**: v = lcm of two denominators, so v <= 2^{2 ell} (see the edge
     case below). This is Shor's order finding modulo divisors F of v, on n <= 2 ell bits.
     (H3) is actually needed only here.
  3. Prime stripping, using group multiplications only. AKS certification is classical.
* Edge case: lem:tb-sylow(d) keeps "only denominators below 2^ell". But o_i = |G| = 2^ell is
  possible (G cyclic of order 2^ell), so this should say "at most 2^ell".
  * With t = 2 ell + 1 we still have 2^{t+1} = 2^{2 ell + 2} > 2 o_i^2, so continued fractions
    still recover k/o_i.
  * Then v <= 2^{2 ell}, and Omega(v) <= 2 ell.

## (2) Do the paper's pieces suffice? Counts

**Modular arithmetic modulo odd F (composite).**
* In-place controlled multiplication by a unit kappa (classical, gcd(kappa, F) = 1 is checked
  classically) takes three steps:
  1. y <- y + c*kappa*x, using `const_mul_acc` with guard c.
  2. x <- x - c*kappa^{-1}*y: the reversed gate list of `const_mul_acc(kappa^{-1})`, with
     kappa^{-1} mod F computed by Euclid.
  3. A controlled swap of x and y.
* Gates, from the stated block counts:
  * one modular addition is at most 38n + 12;
  * each pass has n bits, each with 2 loads of at most n controlled X plus one modular addition,
    so at most 40n^2 + 12n;
  * two passes plus 3n for the controlled swap: **at most 80n^2 + 27n**;
  * ancillas: the same 3n + 5.
* Finite check (`modexp_check.py`):
  * exhaustive on all units kappa, c in {0,1} and x < F, for F in {9,15,21,25,27,33,35,45,49,
    51,55,57,63}. Output correct, every ancilla clean, count <= 80n^2 + 27n in all cases;
  * the full exponentiation |j>|1> -> |j>|a^j mod F> on all 5-bit j, for (F, a) = (15,7),
    (21,2), (33,5), (35,3);
  * gate count bound confirmed for 2^b - 1, b <= 32 (counted, not simulated).
* VBE agree: their Section IV gives O(n^2) per controlled modular multiplication and O(n^3)
  for the exponentiation. Their construction needs only a coprime to N, not N prime.

**Transform.**
* lem:qft-mod needs N odd and does not cover 2^n. But its proof, step E, contains exactly the
  approximate inverse transform over Z/2^t needed here:
  * t gates H and at most t*r rotations CR_k^{-1}, k <= r;
  * operator error at most 2*pi*t*2^-r (eps_aq in that proof).
* Take r = ceil(log2(800 pi t)) = log2 ell + O(1). Each run's output distribution then moves by
  at most 1/400 in total variation (pure-state trace distance is at most the norm distance).
* A pair moves by at most 1/200, and (4/pi^2)^2 * 6/pi^2 - 1/200 = 0.09985 - 0.005 = 0.0949
  > 1/11 = 0.0909. So the lemma's constant 11 survives.
* Over a fixed finite gate set, the O(ell log ell) rotations with k = O(log ell) are synthesized
  to total error 1/400 at a polylog(ell) factor (Dawson-Nielsen). Negligible.
* The same remark gives (H1)'s "standard approximate transform over Z/2^e" for p = 2. It could
  point to step E of the proof of lem:qft-mod.

**One run modulo F** (n = ceil(log2 F) <= 2 ell, t = 2n + 1).
* Gates: t H, then 1 X, then t controlled multiplications, then the transform. In all at most
  (2n+1)(80n^2 + 27n) + (2n+1)(r+2) + 1 = 160 n^3 + O(n^2), so <= 1280 ell^3 + O(ell^2).
* Qubits: 7n + 6.
* So **O(ell^3) is right**. It is not O(ell^3 polylog(1/eps)): eps enters only through the
  number of runs.
* O(n^2 log n log log n) is possible with Schonhage-Strassen (Shor, Section 3), but not needed.

**Classical post-processing.**
* Continued fractions on 2n-bit numbers take O(ell^2) bit operations; Hardy-Wright Thm 184
  (|x - p/q| < 1/(2q^2) implies p/q is a convergent).
* The check a^u = 1 mod F is classical.

**Complete factorization of v: the gap and its fix.**
* Keep a list of factors of v. Divide out 2s. Split perfect powers classically. A factor that
  AKS certifies prime is final.
* Otherwise F is odd with >= 2 distinct primes. An *attempt*:
  1. Draw a uniform in {1..F-1}. If gcd(a, F) > 1, that already splits F.
  2. Otherwise run a pair of order-finding runs, getting u with a^u = 1 with probability > 1/11.
  3. Write u = 2^j m, m odd, and let x be the last non-1 term of a^m, a^{2m}, ..., a^{2^j m}.
* Lemma: with r = ord(a) and r | u, if r is even then x = a^{r/2}; if r is odd there is no such
  x. Proof sketch:
  * a^{2^i m} = 1 iff i >= v_2(r), since odd(r) | m;
  * so x = (a^{r/2})^{m/odd(r)};
  * m/odd(r) is odd and (a^{r/2})^2 = 1, so x = a^{r/2}.
  * Hence any multiple u works as well as the exact order.
* Then gcd(x - 1, F) is proper whenever r is even and a^{r/2} != -1. For a uniform unit this has
  probability >= 1 - 2^{-(k-1)} >= 1/2, with k the number of distinct odd primes (Shor 1997,
  Section 5, which states exactly this bound).
* So an attempt splits with probability >= 1/22, conditional on the past.
* Fewer than 2 ell splits are needed (Omega(v) <= 2 ell).
* With T = ceil(88 ell + 176 ln(2s/eps_pre)) attempts, the mean is mu = T/22 >= 4 ell +
  8 ln(2s/eps_pre). By Chernoff, Pr[X <= mu/2] <= e^{-mu/8} <= eps_pre/(2s), and mu/2 >= 2 ell.
  The failure is detected.
* Gates: 2T runs, O(ell^3 (ell + log(s/eps))) per generator.
* Possible improvement to O(ell^3 log(s ell/eps)): take the lcm of the orders of
  O(log(ell s/eps)) random a's, which is a multiple of lambda(F), then factor classically
  (Miller). It needs one more cited classical lemma, and the exponents do not need it. Not
  recommended.

**Side finding (classical time; not about (H3)).**
* Prop (d) does not list the classical time of the Sylow preprocessing.
* The dominant term is AKS, at most 4 ell certifications per generator on <= 2 ell-bit numbers.
* With AKS Thm 5.3 (O~(log^{15/2} n); checked in the Annals text) this is
  O~(s ell^{17/2}) <= N^{8.5+o(1)}. That is below the smallest total exponent,
  E_W(2) + 1 + 3 = 9, so the theorem stands.
* With AKS Thm 5.1 (O~(log^{21/2})) it would be N^{11.5}, which exceeds 9 at c = 2. So cite
  Thm 5.3, or Lenstra-Pomerance's O~(log^6).
* An optional (d) clause is given below.

## (3) Citations

* **Beauregard 2003 is not the right citation for O(n^3).** His 2n+3-qubit circuit uses
  O(n^3 lg n) gates (depth O(n^3)), because Draper's adder needs arbitrary rotations (abstract,
  checked). Do not cite it for (H3).
* For O(n^3): VedralBarencoEkert1996 (key exists), Section IV. Also Shor 1997, Section 3:
  "O(l^3) time" with schoolbook multiplication, O(l) space.
* For the reduction and the 1 - 1/2^{k-1} bound: Shor 1997, Section 5.
* For 4/pi^2 and the two-run lcm: CEMM 1998, Sections 5 and 6 (checked).
* For continued fractions: Hardy-Wright, Thm 184.
* Cleve-Watrous 2000 (key exists) is about depth. It is not needed here.
* Existing keys: VedralBarencoEkert1996, CuccaroDraperKutinMoulton2004, DawsonNielsen2006,
  CleveWatrous2000. Missing: Shor1997 (only in the appendix's comment list), AKS2004 (cited
  inline in prose), CEMM, Hardy-Wright.

```bibtex
@article{Shor1997,
  author  = {Shor, Peter W.},
  title   = {Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer},
  journal = {SIAM Journal on Computing},
  volume  = {26},
  number  = {5},
  pages   = {1484--1509},
  year    = {1997},
  doi     = {10.1137/S0097539795293172},
  note    = {arXiv:quant-ph/9508027}
}

@article{CleveEkertMacchiavelloMosca1998,
  author  = {Cleve, Richard and Ekert, Artur and Macchiavello, Chiara and Mosca, Michele},
  title   = {Quantum Algorithms Revisited},
  journal = {Proceedings of the Royal Society of London A},
  volume  = {454},
  number  = {1969},
  pages   = {339--354},
  year    = {1998},
  doi     = {10.1098/rspa.1998.0164},
  note    = {arXiv:quant-ph/9708016}
}

@article{AKS2004,
  author  = {Agrawal, Manindra and Kayal, Neeraj and Saxena, Nitin},
  title   = {{PRIMES} is in {P}},
  journal = {Annals of Mathematics},
  volume  = {160},
  number  = {2},
  pages   = {781--793},
  year    = {2004},
  doi     = {10.4007/annals.2004.160.781}
}

@book{HardyWright2008,
  author    = {Hardy, G. H. and Wright, E. M.},
  title     = {An Introduction to the Theory of Numbers},
  edition   = {6th},
  note      = {Revised by D. R. Heath-Brown and J. H. Silverman},
  publisher = {Oxford University Press},
  year      = {2008}
}
```

The details of Shor, CEMM and AKS were confirmed against the arXiv and Annals texts and the DOI
records. HardyWright2008 is from memory, and the theorem number should be confirmed by a human.

## Proposed LaTeX

### Appendix, prop:tb-count-gates

Replace `Assume, in addition to the results cited by Theorem~\ref{thm:bb-envelope}, \textup{(H3)} below. The statement \textup{(H1)},` by

```
Assume the results cited by Theorem~\ref{thm:bb-envelope}. The statement \textup{(H1)},
```

Replace `Hypothesis \textup{(H3)}: one run of` + newline + `Shor's order finding or factoring on $O(\ell)$-bit integers costs $O(\ell^3)$ gates. Then, with` + newline + `every oracle call counted once:` by

```
\textup{(H3)}, that one run of Shor's order finding costs $O(\ell^3)$ gates, is not a
hypothesis either. Modulo an odd $F \ge 3$ with $n = \lceil\log_2 F\rceil \le 2\ell$ bits and
for a unit $a$, one run uses $t = 2n+1$ control qubits, $t$ gates $H$, the exponentiation
$|j\rangle|1\rangle \mapsto |j\rangle|a^j \bmod F\rangle$ as $t$ controlled in-place
multiplications by the classical constants $\kappa = a^{2^i} \bmod F$, and the inverse transform
over $\mathbb{Z}/2^t$ in the product form of step~$E$ of the proof of Lemma~\ref{lem:qft-mod},
with every $\mathrm{C}R_k^{-1}$, $k > r = \lceil\log_2(800\pi t)\rceil$, omitted; by the bound
$2\pi t2^{-r}$ proved there, this moves the output distribution of a run by at most $1/400$ in
total variation. A controlled multiplication $x \mapsto \kappa x \bmod F$ is
$y \leftarrow y + \kappa x$, then $x \leftarrow x - \kappa^{-1}y$ (the reversed gate list of
$x \leftarrow x + \kappa^{-1}y$, with $\kappa^{-1} \bmod F$ computed classically), then a swap of
$x$ and $y$, all controlled on the exponent qubit. It uses the shift-and-add multiplier and the
modular adder of the proof of Lemma~\ref{lem:qft-mod}, which need $F$ odd but not prime, at
most $80n^2+27n$ gates from $\{X,\mathrm{CNOT},\mathrm{SWAP},\mathrm{Toffoli}\}$ (two passes of
$n$ controlled loads and modular additions of at most $38n+12$ gates, and $3n$ gates for the
controlled swap) and the same $3n+5$ clean ancillas. One run therefore uses at most
$(2n+1)(80n^2+27n) + (2n+1)(r+2) + 1 = 160n^3 + O(n^2)$ gates on $7n+6$ qubits, as
in~\cite[Section~IV]{VedralBarencoEkert1996}, so $O(\ell^3)$; the continued-fraction step is
classical~\cite[Theorem~184]{HardyWright2008}. In the black box, one run of
Lemma~\ref{lem:tb-sylow}(d) uses $4\ell+2$ oracle multiplications and $O(\ell^2)$ further gates,
with the same transform. Each run needs only constant precision, so no factor in $1/\eps$ enters
it: over a fixed finite gate set its $O(\ell\log\ell)$ rotations, with $k = O(\log\ell)$, are
synthesized to total error $1/400$ by~\cite{DawsonNielsen2006} at a factor
$\operatorname{polylog}(\ell)$, and $\eps$ enters only through the number of runs. The success
bounds of Lemma~\ref{lem:tb-sylow}(d) are those of the exact transform~\cite[Sections~5
and~6]{CleveEkertMacchiavelloMosca1998}, less $1/200$ per pair of runs; the reduction of
factoring to order finding is that of~\cite[Section~5]{Shor1997}. The counts follow from those
of the blocks, and the controlled multiplication is checked exhaustively, with clean ancillas,
for every unit $\kappa$ and odd $F \in \{9,15,21,25,27,33,35,45,49,51,55,57,63\}$
(\file{research/audits/reviews/2026-11-04-rees-h3-check/modexp_check.py}; AI-checked, pending
human review). Then, with every oracle call counted once:
```

Item (c): replace `\item order finding and factoring use $O(s\ell^3\log(s/\eps))$ gates;` by

```
  \item order finding and factoring use $O(s\ell^3(\ell + \log(s/\eps)))$ gates;
```

Proof (c): replace `\emph{(c).} Lemma~\ref{lem:tb-sylow}(d) runs $O(\log(s/\eps))$ order-finding pairs and one` + newline + `factorization per generator; apply~(H3).` by

```
\emph{(c).} Per generator, Lemma~\ref{lem:tb-sylow}(d) runs at most
$\lceil 11\ln(2s/\eps_{\mathrm{pre}})\rceil$ pairs of black-box runs, $O(\ell^2)$ gates each
by~(H3) (their oracle calls are counted in Theorem~\ref{thm:bb-envelope}(ii)), and at most $2T$
runs modulo divisors of $v \le 2^{2\ell}$, with
$T = \lceil 88\ell + 176\ln(2s/\eps_{\mathrm{pre}})\rceil$, $O(\ell^3)$ gates each by~(H3).
That is $O(\ell^3(\ell+\log(s/\eps)))$ gates per generator.
```

Exponents line: replace `$s\ell^3\log(s/\eps) \le N^4$` by `$s\ell^3(\ell+\log(s/\eps)) \le 2N^4$`
(this holds because $s\ell^4 = (s\ell)\ell^3 \le N^4$).

Optional, item (d): after "for the diagonal-equation solvers" add

```
, plus $\tilde O(s\ell^{17/2})$ bit operations for the primality certificates of
Lemma~\ref{lem:tb-sylow}(d)~\cite[Theorem~5.3]{AKS2004}
```

and in the Exponents line add `$s\ell^{17/2} \le N^{17/2}$, below $E_W(c)+4 \ge 9$`.

### Appendix, lem:tb-sylow(d) proof (needed for the count above)

* Replace `\ge (4/\pi^2)^2\cdot 6/\pi^2 > 1/11$` by
  `\ge (4/\pi^2)^2\cdot 6/\pi^2 - 1/200 > 1/11$ (the $1/200$ is the transform error of~(H3) in
  Proposition~\ref{prop:tb-count-gates})`.
* Replace `\lceil 11\ln(s/\eps_{\mathrm{pre}})\rceil` by `\lceil 11\ln(2s/\eps_{\mathrm{pre}})\rceil`.
* Replace `(only denominators below` + newline + `$2^\ell$ are kept)` by `(only denominators at
  most $2^\ell$ are kept)`.
* Replace `Factor $v$ with` + newline + `Shor's algorithm and certify its prime factors
  deterministically (Agrawal, Kayal and` + newline + `Saxena, Ann.\ of Math.\ 2004); this uses no
  group multiplication.` by

```
Factor $v \le 2^{2\ell}$ completely, with no group multiplication, by Shor's
reduction~\cite[Section~5]{Shor1997}. Keep a list of factors with product $v$; divide out
powers of $2$, split perfect powers classically, and call a factor final when the test
of~\cite{AKS2004} certifies it prime. Any other factor $F$ is odd with at least two distinct
prime factors. An attempt on $F$ draws $a$ uniformly from $\{1,\dots,F-1\}$; if
$\gcd(a,F) \ne 1$ this splits $F$, and otherwise a pair of runs modulo $F$ as in~(H3) of
Proposition~\ref{prop:tb-count-gates} gives, with probability above $1/11$, some $u$ with
$a^u \equiv 1 \pmod F$. Write $u = 2^jm$ with $m$ odd and let $x$ be the last term different
from $1$ of $a^m, a^{2m},\dots,a^{2^jm} \bmod F$. If $r$ is the order of $a$, then $r \mid u$
forces $x = a^{r/2}$ when $r$ is even (and no such term exists when $r$ is odd), so
$\gcd(x-1,F)$ is a proper factor whenever $r$ is even and $a^{r/2} \not\equiv -1$, which has
probability at least $1/2$~\cite[Section~5]{Shor1997}. So each attempt splits with probability at
least $1/22$, whatever happened before, and fewer than $2\ell$ splits are needed, since
$\Omega(v) \le 2\ell$. Within $T = \lceil 88\ell + 176\ln(2s/\eps_{\mathrm{pre}})\rceil$
attempts, the number of successes dominates a binomial variable of mean $\mu = T/22$, with
$\mu/2 \ge 2\ell$; by the Chernoff bound the factorization is incomplete with probability at most
$e^{-\mu/8} \le \eps_{\mathrm{pre}}/(2s)$.
```

and replace `A generator fails only if no` + newline + `pair succeeds, with probability at most
$\eps_{\mathrm{pre}}/s$, and the failure is` by `A generator fails only if no pair succeeds or the
factorization is incomplete after $T$ attempts, each with probability at most
$\eps_{\mathrm{pre}}/(2s)$, and the failure is`.

(Optional, appendix intro line ~46: "Shor's order finding and factoring" -> "Shor's reduction of
factoring to order finding and the order-finding success bounds~\cite{Shor1997,
CleveEkertMacchiavelloMosca1998}".)

### main.tex, thm:bb-envelope(iii)

Replace `Under the hypothesis (H3) of Proposition~\ref{prop:tb-count-gates}, with the field arithmetic of the paragraph ``Binary arithmetic and explicit transforms'' (its (H2), discharged there) and Lemma~\ref{lem:qft-mod} for the transforms,` by

```
With the field arithmetic of the paragraph ``Binary arithmetic and explicit transforms'',
Lemma~\ref{lem:qft-mod} for the transforms, and Shor's order finding built from the same blocks
((H2) and (H3) of Proposition~\ref{prop:tb-count-gates}, both discharged there),
```

and `and order finding and factoring use $O(s\ell^3\log(s/\eps))$;` by

```
and order finding and factoring use $O(s\ell^3(\ell+\log(s/\eps)))$;
```

### main.tex, status sentence after the theorem

Replace `the gate and time counts of~(iii) are proved there under the compilation hypothesis (H3) of Proposition~\ref{prop:tb-count-gates}, which this paper states but does not prove; (H1) is proved as Lemma~\ref{lem:qft-mod} and (H2) is discharged by the binary arithmetic of Section~\ref{sec:uniform-compilation}, both AI-checked, pending human review.` by

```
the gate and time counts of~(iii) are proved there by Proposition~\ref{prop:tb-count-gates},
with no compilation hypothesis: (H1) is proved as Lemma~\ref{lem:qft-mod}, (H2) is discharged by
the binary arithmetic of Section~\ref{sec:uniform-compilation}, and (H3) by Shor's order finding
built from the same blocks, with the reduction of factoring to order finding and the
order-finding success bounds cited from~\cite{Shor1997,CleveEkertMacchiavelloMosca1998}, all
AI-checked, pending human review.
```

### main.tex, proof sketch (stale reference)

Replace `Proposition~\ref{prop:tb-count-gates} the gate and time counts of~(iii) under the compilation hypotheses (H2) and (H3), with (H1) supplied by Lemma~\ref{lem:qft-mod}.` by

```
Proposition~\ref{prop:tb-count-gates} the gate and time counts of~(iii), with (H1)--(H3)
supplied by Lemma~\ref{lem:qft-mod}, the binary arithmetic of
Section~\ref{sec:uniform-compilation} and Shor's order finding built from it.
```

## Alternative if the owner prefers not to change (c)

Keep (H3), but restate it honestly:

> (H3) a complete factorization of an integer below 2^{2 ell}, with failure probability
> delta, costs O(ell^3 (ell + log(1/delta))) gates; one run of order finding costs O(ell^3).

Then fix (c) to O(s ell^3 (ell + log(s/eps))). The current wording, "one run ... factoring ...
O(ell^3)" applied once per generator, undercounts factoring, and the failure share of lem:tb-sylow(d)
is short by the factoring term.

Status: AI-checked, pending human review.

## Applied (11-04)

The main proposal was applied, not the fallback. I matched each replacement by exact string and
checked it against the current text and the math first. Backups:
`/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/bak-i174/`.
AI-checked, pending human review.

**Appendix (`appendix-torsion-blackbox.tex`)**
* **Opening of prop:tb-count-gates: applied.**
* **(H3) paragraph: applied verbatim.** Checks:
  * 80n^2+27n = 2n(2n+38n+12) + 3n;
  * (2n+1)(80n^2+27n) + (2n+1)(r+2) + 1, with leading term 160n^3;
  * 7n+6 = (2n+1) + 2n + (3n+5);
  * 2^r >= 800 pi t gives 2 pi t 2^-r <= 1/400;
  * step E of lem:qft-mod does omit CR_k^{-1} for k > r, with the bound 2 pi t 2^{-r};
  * 4l+2 = 2(2l+1).
* **Theorem 184 of Hardy-Wright: kept.** I am confident it is the statement
  |x - p/q| < 1/(2q^2) implies p/q is a convergent. Shor also cites this theorem number.
* **Item (c): applied.**
* **Proof (c): applied.**
* **lem:tb-sylow(d): all four edits applied.** These are the 1/200 term, ln(2s/eps_pre),
  "at most 2^ell", the factorization paragraph and the failure sentence. Checks:
  * (4/pi^2)^2 * 6/pi^2 = 0.09986, so subtracting 1/200 gives 0.0949 > 1/11 = 0.0909;
  * e^{-11 ln(2s/eps)/11} = eps/(2s);
  * mu = T/22 >= 4l + 8 ln(2s/eps), so mu/2 >= 2l and e^{-mu/8} <= eps/(2s);
  * the last-non-1-term lemma;
  * the attempt bound 1/22 = (1/2)(1/11): the 1/11 holds for every a, and a non-unit a
    splits F.
* **AKS time in (d): applied as given.** I also added one sentence to proof (d), taken from
  this review's side finding. Fewer than 4l factors are tested, each of at most 2l bits, at
  O~(l^{15/2}) each by AKS Thm 5.3.
* **Exponents line: applied, slightly modified.** It now reads
  `s l^3 (l + log(s/eps)) <= 2N^4 (as s l^4 = (s l) l^3 <= N^4)`, plus the AKS clause
  `s l^{17/2} <= N^{17/2}, below E_W(c)+4 >= 9`.
  * Check: s l^4 <= N^4. The existing s l^3 log(s/eps) <= N^4 still holds. N^4 is below
    N^{E_W(c)+4}, so the totals stand.
  * Caveat: "E_W(c)+4 >= 9" holds for c >= 2 only. That is the same range as the existing
    "E_W(c) >= max(c,5) for c >= 2" in that line.
  * c = 1 (E_W(1) = 1) is already outside what this line proves: l^6 > N^{E_W(1)+1+3}. This is
    an older gap, not new here, and was left unchanged.
* **Optional intro line ~46 and the (H1) p = 2 pointer: skipped.** They were not in the
  requested list.

**main.tex**
* **thm:bb-envelope(iii) opening clause: applied, modified.** The order is changed to "With
  Lemma qft-mod for the transforms, the field arithmetic of the paragraph ..., and Shor's order
  finding ...". The review's order made a 12.6pt overfull box. The content is the same.
* **(iii) (c) bound: applied.**
* **Status sentence after the theorem: applied verbatim.** The "AI-checked, pending human
  review" label is kept.
* **Stale "(H2) and (H3)" in the proof sketch: applied.**

**references.bib**
* **Shor1997, CleveEkertMacchiavelloMosca1998, AKS2004 and HardyWright2008: added as given.**
  There were no duplicate keys.

**Build and checks**
* latexmk in the scratchpad build directory gives 139 pages: no Overfull, no "Float too
  large", no undefined references or citations, and 0 BibTeX warnings.
* `tests/tools/test_rees_paper_numbers.py`: 2 passed.
* `modexp_check.py` reran in 6.7 s with exit 0. Its output is identical to `modexp_check.out`.
