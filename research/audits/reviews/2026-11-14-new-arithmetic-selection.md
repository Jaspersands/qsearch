# Binary-index modular factorial: one concrete degree-avoidance screen

2026-11-14. STATE/TRAPS read; precise corpus `been-tried` and `baselines`
queries preceded targeted topic/source reads. No network, API, Git, tests,
archive scan, or shared-status edit. Weak-phase and hidden-field work is
not continued here.

**Selection: no new paid batch.** A residue-only Gross--Koblitz route has
a well-defined target, but the proposed norm compression loses precisely
the residue being sought. The available quantum Gauss-phase procedure
does not repair that loss in a binary-input clock. This is a falsifier of
that concrete composition, not a general modular-factorial lower bound.

## 1. Native endpoint and why it would matter

Input: a binary odd prime p and binary integer 0<=n<p. Output the exact
residue n! mod p, with failure <=eta, in poly(log p,log(1/eta)) bit/gate
time. No divisor of p-1, class/unit data, field of degree comparable to p,
Gauss-sum value, or p-adic gamma evaluator is supplied. Primitive roots
and factoring p-1 may be computed quantumly and must be charged.
The exact residue is useful in modular combinatorics and the arithmetic
factorial/gamma congruences studied by the actual sources; this is not a
request to sample a binomial law or approximate a real-valued factorial.

Exact central binomial residues are an equivalent narrow endpoint. Write
n=2m+b, b in {0,1}; then

    n! = (2m+1)^b * binomial(2m,m) * (m!)^2 mod p.          (1)

One halving chain uses O(log n) central-binomial calls. Conversely,
binomial(2m,m)=(2m)!/(m!)^2 when 2m<p. All denominators are nonzero.
This reduction supplies no fast coefficient oracle; normalized-amplitude
or binary-binomial SAMPLING routines are not exact modular coefficient
evaluators. General binomial(n,k), n<p, follows from three factorials.

## 2. Strongest retained baselines and the exact old scope

PRIME_INDEX_FACTORIAL_RESIDUE_NORMALIZATION.md already gives the written
quantum composition for ((p-1)/ell)! when ell is an odd prime dividing
p-1, in poly(NUMERICAL ell,log p,log(1/eta)). Its degree-ell fields, module
arithmetic, and selected-mode operations cannot be renamed poly(log ell).
Fixed half/third/quarter-index results are also already recorded.

The stronger current classical source is Tal, ECCC TR26-211, *Computing
Modular Factorials Below the Square-Root Barrier*. Actual Theorem 1.1
gives deterministic soft-O(q^c+sqrt(p/q)) bit time for a supplied divisor
q|p-1 and n<p, with an absolute c>=1. The q=1 baseline is always available;
an advantageous divisor must actually be found, and need not exist in a
desired size range. The general native factorial problem is not thereby
classically polynomial in log p.

Actual Theorem 1.3 also covers each FIXED odd prime-power index r and a
given q|Phi_r(p): at modulus p its clock is soft-O_r(q^(c_r) +
(Phi_r(p)/q)^(1/(2*phi(r)))). It is deterministic given the compatible
finite-field/character data, and has the same EXPECTED bound after their
charged Las Vegas construction (source lines 317-323). In particular,
r=3, q|p^2+p+1 gives expected soft-O(q^(c_3)+sqrt(p)/q^(1/4)). The index
r is fixed; finding a useful q is still charged. This is a stronger
comparator in applicable divisor regimes, not a uniform polylog-p claim.

Actual Section 1.2.1 and Theorem 1.5 already use an O(log a) addition
chain for repeated Jacobi sums. The resulting product representation and
recovery clock remain q^O(1) polylog(p). Thus “store the long product in
binary” is already present in the strongest baseline. It does not remove
the character-order/expanded-algebra dependence.

Sources read locally: audits/sources/jacobi_classical_eccc_2026_211.txt,
Theorems 1.1/1.3/1.5 and Sections 1.2.1/2.3; and the current
JACOBI_GROUP_RING_RECOVERY.md disposition. The corpus baseline keyword
search returned only generic arithmetic matches; those do not supersede
the actual factorial theorem.

## 3. Proposed genuinely smaller object: one local Gauss unit

For 1<=n<=p-2, let omega be the Teichmuller character, fix the compatible
additive character, and choose pi with

    pi^(p-1)=-p,  zeta_p=1+pi mod pi^2.

Gross--Koblitz, in the exact convention reproduced in Tal Section 2.3,
equations (13)--(14), gives

    u_n = -G(omega^(-n))/pi^n
        = Gamma_p(n/(p-1)) in Q_p^*,
    u_n mod p = (n!)^(-1).                                (2)

The endpoints n=0,p-1 are trivial. The final unit really is in the BASE
local field; it does not intrinsically require an output vector of length
p-1. This makes (2) a meaningful degree-avoidance target, not a proof that
expanded cyclotomic degree is unavoidable. The missing operation is to
compute that one normalized residue from p,n without already evaluating
the long Gauss sum or Gamma_p at this binary argument.

The source's p-adic functional equation alone moves the gamma argument
one step at a time. Its known valuation n can be stored in binary; doing
so does not compute the leading unit coefficient. A valued representation
containing that coefficient would already contain the requested answer.

## 4. Exact early falsifier of norm compression plus phase selection

Let E=Q_p(pi), of degree p-1 by Eisenstein. Even GRANTING an efficiently
computed exact local norm of u_n, one obtains only

    N_(E/Q_p)(u_n)=u_n^(p-1).                              (3)

For every Teichmuller root xi in mu_(p-1) contained in Q_p, u_n and xi*u_n
have the SAME (3), while their residues range over every element of
F_p^*. This ambiguity persists for the full p-adic norm, not merely its
first digit. Mod p, (3) is always 1. Norming the known uniformizer factor
out of a Gauss norm therefore does not determine the factorial residue.
The original p,n still specify a unique Gauss sum: this is loss in the
proposed intermediate data, not ambiguity of the full native input.

The tempting quantum repair is to select the root using the ordinary
complex Gauss phase. Local norm data does NOT provide a computable global
complex embedding or candidate-root list. Even GRANTING these extra
interfaces and all norm data, nearest-root selection among p-1 factors
needs phase error O(1/p). Actual van Dam--Seroussi Algorithm 3 and
Theorem 1/proof (local van_dam_seroussi_gauss_2002.txt:483-523) implement
the phase and estimate it in O(epsilon^(-1) poly(log p)) time. The proof
explicitly repeats the phase t=1/epsilon times; binary writing of t is
not a fast implementation of its powers. At epsilon=O(1/p), this supplied
procedure is not a polynomial-logarithmic repair. This is a statement
about that procedure, not a lower bound on all arithmetic root selection.

## 5. Source gate and next action

No quantum build or generic “compressed Jacobi” request is justified.
The exact source that could change this decision must supply a native
one-digit evaluation of (2), or a new canonical-root selector whose clock
is polynomial in log p and which does not call a factorial/gamma oracle.
An efficient norm, compact exponent, or coarse Gauss phase alone fails
the explicitly checked interface above.

For primary confirmation the parent can fetch Gross--Koblitz, *Gauss sums
and the p-adic Gamma-function*, Annals of Mathematics 109(3), 569--581
(1979), DOI 10.2307/1971226. Tal's retained actual formula is the current
source input, not a new gamma-evaluation theorem. Current algorithms for
Morita gamma at arbitrary binary arguments, with growing p, would be the
other relevant source search; fixed-p or numerical-p polynomial clocks do
not qualify. No concrete operation presently survives this screen.
