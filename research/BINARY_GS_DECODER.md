# Deterministic Binary-Field List Decoding For Coherent Erasure

2026-10-22. KNOWN ALGORITHMS, local composition audit REVIEW-PENDING.
This removes the need for a randomized factorization backend in the binary
GS route. It is not a new quantum algorithm, an independent validation of
the whole codeword-filter theorem, a compiled circuit, or a speedup claim.

## The Scientific Question

BALANCED_CODEWORD_FILTER.md requires the COMPLETE radius-w list of ordinary
RS[N,K] codewords for every received z over F_(2^n). It then measures only
whether that list is a singleton, erases the original codeword/message,
and cleans the decoder workspace. Incomplete lists can manufacture false
singletons. Measuring a correct codeword/list instead destroys coherence.

The existing note left finite-field factorization randomness and coherent
failure accounting as implementation obligations. For this fixed-small-
characteristic setting they need not be introduced at all. The construction
below is deterministic polynomial BIT complexity in n,N for every input,
given the public irreducible modulus and field basis. It does not search
for one lucky seed valid on exponentially many words.

## Known Ingredients And Attribution

Berlekamp trace splitting is established prior art. [Petit, Section 2.2](https://people.maths.ox.ac.uk/petit/files/SRA.pdf)
describes squarefree split extraction with gcd(Y^q-Y,f) and successive
trace cuts for small characteristic. This is not the generally unresolved
problem of deterministic polynomial root finding in arbitrary large prime
characteristic. The polynomial degree and field bit length are both charged.

Guruswami-Sudan interpolation and Roth-Ruckenstein coefficient extraction
are also prior art. [McEliece, Sections V-IX](https://ipnpr.jpl.nasa.gov/progress_report/42-153/153F.pdf)
gives the interpolation/factorization route. Here we spell out a deterministic
root backend, a worst-input branching ledger and the clean-erasure interface.
No claim of discovering these classical algorithms is intended.

## 1. All Linear Roots Without Field Enumeration

For nonzero f in F_q[Y], degree d, compute

    G = monic gcd(f, Y^q-Y).

Compute Y^q modulo f by n modular squarings, not by expanding degree q.
G is exactly the product of the DISTINCT base-field linear factors, even
when f is inseparable or has repeated/nonlinear factors. A nonzero constant
has no roots. The zero polynomial is an explicit unsupported all-field case,
never an empty complete list.

For each public binary basis element e_j, form modulo G

    T_j(Y) = sum_{r=0}^{n-1} (e_j Y)^(2^r).

Split each current factor p by gcd(p,T_j) and its exact complementary
quotient. On a field root u, T_j(u)=Tr(e_j u) is zero or one. Distinct
roots u,v differ on at least one of these n cuts, by nondegeneracy of the
trace pairing. After all cuts, every remaining factor is linear.
Sort the encoded roots canonically and verify their product equals G.

There are at most n basis rounds and at most d pieces. Even naive arithmetic
uses only polynomially many operations on degree-d polynomials and n-bit
field elements. No random factorization call, scan over q elements, advice
table, or source-distribution premise is present. The implementation reports
trace/gcd work separately; it does not interpret those counts as gate counts.

## 2. A Worst-Input Roth-Ruckenstein Width Bound

Given nonzero Q(X,Y), remove its common X power so Q(0,Y) is nonzero.
To find every f(X)=f_0+...+f_(K-1)X^(K-1) with Q(X,f)=0, branch over
ALL roots gamma of Q(0,Y), substitute Y=gamma+X Y, remove common X
content again, and recurse for exactly K coefficient positions. At depth K
verify the full formal identity Q(X,f)=0, not just equality modulo X^K.

Let gamma have multiplicity m in the parent specialization Q(0,Y).
In Q(X,gamma+X Y), the coefficient of X^m Y^m is nonzero: its only
contribution of that X/Y degree comes from the original X^0 specialization.
The extracted X valuation v is therefore <=m. After normalization, the
child specialization has Y degree <=v<=m, since each Y^r introduced by
the substitution carries at least X^r. Summing over all root branches
shows that the total specialization degree cannot increase at any level.

Writing ell=deg_Y Q, every noninitial level has at most ell nodes, and
the full tree has at most 1+K*ell nodes. The X degree never exceeds
deg_X Q+K*ell. These are WORST-INPUT bounds, including repeated roots,
dead branches and long common coefficient prefixes. They justify fixed
workspace and loop budgets, not just favorable average branching.

Completeness follows by following each actual polynomial root's next
coefficient. Soundness follows from the final full identity test.
Do NOT stop a branch merely because its current polynomial vanishes at
Y=0. For example Q=Y(Y+X) has both polynomial roots 0 and X. Returning
0 immediately loses X. Likewise Q=Y+X^K has a length-K zero prefix but
NO root of degree<K. Both are retained regression countercontrols.

## 3. Interpolation And The Complete Radius List

Let a=N-w and require a^2>N(K-1). For K>=2 use

    s = floor(N(K-1)/(a^2-N(K-1)))+1,
    D = s*a-1,
    monomials X^i Y^j with i+(K-1)j<=D.

There are more monomials than N*s*(s+1)/2 Hasse-derivative constraints.
Deterministic canonical Gaussian elimination returns a nonzero Q vanishing
with multiplicity s at all (alpha_i,z_i). No probabilistic linear algebra
is needed. The reference verifies the nullspace equations exactly.

For any degree<K polynomial f agreeing at >=a positions, Q(X,f(X)) has
degree <=D and at least s*a zeros counted with multiplicity, hence is zero.
Thus all radius-w messages appear among the polynomial roots above. Evaluate
each candidate at all public points, discard candidates outside the radius,
and sort the survivors. This is the EXACT radius list, not merely a superset
of plausible codewords or a collection of independently valid candidates.
For K=1 count received symbols directly; no general field scan is necessary.

The complete decoder is polynomial in n,N with fixed public parameters.
At a fixed Johnson margin, s and ell are constant. Dense interpolation still
costs O(N^3) field operations and O(N^2) field storage; it is not a practical
gate estimate. Field inversion/multiplication and reversible overhead are
additional polynomial bit costs. The executable dense reference deliberately
caps its matrix cells; the n17/n31/n61 N=n^2 layouts are budgets, NOT runs.

## 4. Clean Coherent Interface, Without Random Tapes

Use a fixed-length payload consisting of a singleton bit and K field
coefficients, zero padded when not a singleton. Keep this separate from
the all-zero message, which can be a legitimate singleton. A deterministic
bounded Boolean implementation can be made reversible by keeping its history,
copying the payload, then reversing the computation. This standard construction
is polynomial, though not space optimal. It is NOT accomplished by putting
Python/FLINT into a quantum register.

The public bounds above allow a fixed number of padded RR node slots, fixed
polynomial degrees, and input-controlled arithmetic. Field division uses
explicit zero handling; normalized polynomials have nonzero selected divisors.
Gaussian pivot selection, Euclidean iteration, root sorting, candidate
verification and every comparison must be implemented and charged. A circuit
may use a supplied, checked irreducible modulus; random field construction is
not part of the coherent decoder. The software fixtures record the existing
repository field modulus rather than claiming a new field-construction method.

For the actual singleton erasure:

1. Compute the clean payload from the received z, retaining z unchanged.
2. Measure ONLY the singleton bit, retaining all rejected mass in the budget.
3. In the successful branch XOR the unique message into the original message
   register. Since that message was within the retained radius, completeness
   forces equality, so the original register becomes zero.
4. Run the payload oracle backwards using the unchanged z, cleaning the
   decoded message, flag and all workspace. Then perform the inverse Fourier
   readout from the existing construction.

The same reasoning applies with encoded codewords if encoding/decoding the
message is paid. No exact error-weight, error-support, list, root path or
codeword record may remain. Branch-dependent workspace is uncomputed, not
discarded or measured. A gate implementation built from exact classical
reversible gates has no randomized decoder error term. Physical gate errors
and any chosen approximate synthesis still require their own budget.

This closes an ALGORITHMIC dependency: a deterministic complete decoder can
be coherently compiled with polynomial overhead. It does not mean the
repository contains that circuit. It also does not independently validate
the support-mask lemma or establish hardness of the explicit native problem.

## Controls And What Would Falsify This Closure

- Exhaustively compare complete decoder lists on every received word in
  bounded codes, including empty, singleton and ambiguous lists. Check
  erasure on every retained (received,message) pair.
- Check repeated/inseparable factors, root-free factors, zero roots, long
  shared prefixes, forbidden early termination and truncated false roots.
- Check the width, specialization-degree and X-degree ledgers at every node.
- Run small-length decoder fixtures over F_(2^17), F_(2^31), F_(2^61) using
  nontrivial field elements, without enumerating q. These are planted decoder
  regressions, not hardness evidence or native N=n^2 quantum experiments.
- A missing true candidate, false singleton, superpolynomial branch count,
  uncharged field scan, or retained workspace record would invalidate the
  corresponding implementation claim. Passing finite tests alone does not
  prove the full theorem; the algebraic arguments above still need review.

## Next Decision

Do not spend the next GPT pass optimizing Gaussian elimination or synthesizing
thousands of gates. Those are known implementation tasks, not the scientific
uncertainty. The explicit quantum candidate now has a deterministic decoder
route; its strongest unresolved question remains classical solvability of
the SAME inverse-trace relation, plus independent review of the composed
quantum proof. The native Gibbs pilot is already specified for Gemini.

Replay: `python -m theorems.binary_gs_decoder --write`, with
PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache in this workspace.
