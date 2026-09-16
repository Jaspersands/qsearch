# Exact Spatial Transfer For The One-Round Echo

Status: IMPLEMENTED EXACT EVALUATOR AND SCOPED INTEGER CERTIFICATES.
The derivations remain review-pending; independent review, formal verification,
novelty and a quantum speedup are not established.

This continues [the costed echo experiment](COHERENT_OVERLAP_ECHO.md), without
changing its standard mixed coset inputs or replacing its fixed X readout.
The new result is negative: at S6, one round loses its signal as copies grow,
and no copy count makes it beat even one pair measurement. It is NOT a bound
for growing group degree or for the proposed r=n temporal rounds.

## Spatial Reduction

Let D=n!, H={e} under null and H={e,h} under the fixed-hidden alternative.
The SAME h is retained at every site. Write the known central reflection as

    U = sum_g (c_g/D) R_g,  c_g integer.

Each path bond occurs twice in one echo round. Its two group variables (a,c)
have weight w(a,c)=c_a c_c/D^2 and endpoint predicate E(a,c)=1[ca in H].
For an A bond (a,c) adjacent to a B bond (b,d), the chronological site word is
dcba. Hence the interior kernel is

    F((a,c),(b,d)) = 1[dcba in H].

Start with v_A(a,c)=w(a,c) E(a,c). At successive sites,

    v_B(b,d) = w(b,d) sum_(a,c) F((a,c),(b,d)) v_A(a,c),
    v_A(a,c) = w(a,c) sum_(b,d) F((a,c),(b,d)) v_B(b,d).

After K-1 bonds, contract the final vector with E. This gives exactly
Tr[W rho_H^tensor K], not a norm diagnostic. The boundary has D^2 entries
independent of K; it is not a D^K state or D^(2K) density matrix.

For a fixed output (b,d), choose a and t in H, then set
c=d^-1 t a^-1 b^-1. In the reverse transfer, for output (a,c), choose b and t
then set d=t a^-1 b^-1 c^-1. Each row therefore has at most |H|D incoming
assignments. Zero coefficients can be omitted because they are zero terms
of the operator expansion. This is not physical postselection or omitted
source probability.

## Correct Symmetry

Under null, quotient pairs (a,c) by simultaneous G conjugation. For fixed h,
use ONLY its centralizer C_G(h). Using all G would change the endpoint and
interior predicates and silently replace the input model.

The state vector stores a value PER PAIR, constant on an orbit. A quotient
matrix entry counts how many incoming pairs in that orbit satisfy the
constraint for one output representative. It is not an orbit-averaged weight.
The final contraction MUST multiply by each orbit size:

    m_K = sum_orbits |orbit| E(orbit) v_final(orbit).

The coefficient support, endpoints and transfer respect the specified group.
Tests compare full unquotiented Python-integer transfer, physical source-block
matrices, different hidden members, and the three-copy endpoint-elimination
formula. A nonmissing S4/transposition four-copy matrix control checks the
alternating spatial orientation beyond the previous three-copy case.

At S6, D^2=518400, of which 342225 pairs have nonzero coefficient weight.
The null quotient has 585 states. The fixed-hidden quotient has 7438 states
under a centralizer of order 48. Each hidden transfer has 6245474 nonzeros.
Construction, storage and arithmetic still depend factorially on n.
Polynomial-in-K evaluation at fixed degree is NOT polynomial-in-n
dequantization, a quantum measurement compiler, or a classical solver for an
unknown instance.

## Exact Arithmetic

Signed transfer weights can suffer severe cancellation. The final moments
are reconstructed as exact rationals using independent prime moduli and CRT.
For e=K-1 bonds, the numerator has the unconditional algebraic bound

    |N_K| <= (sum_g |c_g|)^(2e).

This follows by bounding the absolute sum of all operator-expansion terms,
with site predicates at most one. It does not assume the numerical answer
already satisfies unitarity. The combined CRT modulus exceeds twice this
bound; an additional unused prime checks the reconstructed integer. The
denominator before cancellation is D^(2e). Physical |m_K|<=1 is checked
separately. Hexadecimal integers preserve exact large certificates.

Sparse count multiplication uses float64 ONLY where every product and every
nonnegative partial sum is an exactly representable integer below 2^52.
The code derives a safe modulus bound. Signed coefficient multiplication and
terminal orbit-weight sums use int64 below 2^62. There is no floating-point
cancellation in the reconstructed result. The S6 sweep through K=64 uses 57
CRT primes plus a held-out prime.

For arbitrary-size witness integers, count multiplication is split into
24-bit digits, contracted within the same exact-integer range, then joined
with Python integers. This is also used to verify the all-copy inequalities.

## All-Copy Decay Certificate

Let C_AB and C_BA be the nonnegative integer quotient count matrices, and
W_abs=diag(|c_a c_c|). The signed transfers are bounded entrywise by

    A_AB = W_abs C_AB / D^2,  A_BA = W_abs C_BA / D^2,
    P = A_BA A_AB.

A positive integer vector u satisfying P u <= theta u is a sufficient
contraction certificate. Numerical resolvent iteration PROPOSES u, but only
exact integer inequalities ACCEPT it:

    denominator(theta) (W_abs C_BA W_abs C_AB u)_i
       <= numerator(theta) D^4 u_i,  for every i.

For S6, theta=3/4 is verified independently for null and fixed h. All 8023
coordinate inequalities are retained through two saved vectors and kernel
fingerprints. This is not a fitted eigenvalue or an extrapolated decay curve.
The S3 protected alternative does not receive a false contraction certificate.

Put c=max_i |w_i| E_i/u_i, and t_i=|orbit_i| E_i. Entrywise domination gives

    |m_K| <= min(1,C_even theta^((K-2)/2))       for even K,
    |m_K| <= min(1,C_odd theta^((K-3)/2))        for odd K,
    C_even = c sum_i t_i u_i,
    C_odd  = c sum_i t_i (A_AB u)_i.

The stored exact prefactors are below three for both hypotheses. Conjugacy
covariance of the central phase word makes all h in the class have the same
output law. Since output TV=|m_h-m_0|/2, this proves the scoped conclusion

    TV <= min(1,3*(3/4)^floor((K-2)/2))  for EVERY K>=3.

Thus both X-readout distributions approach a fair coin. More preparation
and more pair queries erase this particular signal.

## Complete Prefix And Tail

The decay bound alone does not identify the best finite copy count. Exact
CRT evaluation covers EVERY K=3,...,31. The bound at K=32 and K=33 lies below
the exact prefix maximum; each subsequent parity cap decreases by 3/4 every
two copies. There is no unchecked interval or fitted tail.

The global maximum for this fixed-S6 one-round family is therefore

    max_(K>=3) TV = 16843/303750, attained only at K=3.

One pair's source/target-label measurement has TV=1271/7200, already larger.
It can ignore any additional supplied copies, so it dominates the entire
specified echo family, not merely the sampled sweep points.

Representative exact evaluations, shown here rounded only for readability:

| K | Null moment | Hidden moment | Echo TV | Pair-event count TV |
| --- | --- | --- | --- | --- |
| 3 | 0.399146 | 0.510047 | 0.0554502 | 0.176528 |
| 12 | 0.00189524 | 0.00898076 | 0.00354276 | 0.329989 |
| 36 | 9.31151e-10 | 1.61698e-7 | 8.03834e-8 | 0.550891 |
| 64 | 4.06403e-17 | 4.71344e-13 | 2.35652e-13 | 0.688718 |

The baseline measures disjoint quantum pairs and counts the event that the
known two-copy likelihood exceeds one. Its event law is the same for every
h in the class, so the count is binomial despite the shared hidden member.
This coarsened TV is a LOWER BOUND on the complete pair-label likelihood
readout. The existing `independent_pair_label_likelihood` evaluates the full
fixed-point-free score in polynomial bit complexity on actual supplied
labels; the factorial calculation of calibration probabilities is not part
of that readout. No classical sampler for the quantum front end is provided.
At K=36 the pair-event route uses 108 QFT/inverse calls versus 140 for the
one-round echo, with the same supplied-copy budget.

## Scope And Remaining Work

The two finite parameters must not be conflated:

- K grows in the exact transfer and all-copy theorem at FIXED S6.
- n does NOT grow in that theorem.
- r is exactly ONE; the r=n growing-degree proposal is not evaluated here.

APIs reject applying a certificate to another degree, hidden class or temporal
depth. A one-round boundary is a group-element pair; r rounds would require
a justified temporal-history contraction, not merely more iterations of this
same spatial matrix. Any degree-uniform bound needs explicit control of its
weights, quotient size, prefactors and contraction rate as n changes.

Potential next route: compare the two purified circuit orderings and use
disjoint backward light cones to bound their overlap by local return
probabilities. Those probabilities and their scaling must be proved; neither
Haar-random mixing nor free access to a purification is granted. This is a
lead, NOT a gate-enabled theorem or implemented new readout. If no substantive
degree/depth argument emerges, pivot rather than tuning more finite echoes.

## Reproduce And Replay

    python qsearch.py coset-overlap-transfer
    python qsearch.py coset-overlap-transfer --replay
    python qsearch.py run EXP-COSET-OVERLAP-SPATIAL-TRANSFER

The read-only replay rebuilds both kernels, rechecks integer decay vectors,
rates, scopes and parity prefactors, reconstructs all 58 prefix moments, and
checks the prefix/tail maximum and baseline domination. It does not re-run
every requested sweep point above K=31. `--no-registry` writes only the report.
The result, negative record, proof lemmas and mutation obligations preserve
the fixed-degree/one-round scope. No candidate is promoted.
