# Affine-Walsh MPI Attack: Exact Structure, Negative Native Result

2026-10-23. A bounded classical attack on the SAME public native instance.
No dequantization, hardness, sampling, mixing or quantum-speedup conclusion.

## 1. Scientific Decision

The native evaluation set has exploitable affine structure, but the
predeclared use of that structure does NOT improve the inherited best
assignment or reach score 0.3. Do not grow this into another search-engine
subsystem or budget-tuning campaign. Its algebraic identity remains useful
as an explicit structural baseline for future genuinely different attacks.

## 2. Exact Algebraic Mechanism

Write the additive field coordinates as F2^h. Let k(t)=log_g(t) in Z_N for
t!=0 and set k(0)=0 to define a full convolution. The chosen zero value
never occurs on the disjoint native support/evaluation rows.

Suppose evaluations contain a COMPLETE affine block a+U, where U is a
binary subspace. For a character chi:U->{+1,-1}, define a direction

    v_chi(a+u)=chi(u), with zero entries outside the block.

Its row-phase change is

    D_chi(t)=sum_(u in U) chi(u) k(t+a+u) mod N.

For every w in U, substitution u'=u+w gives

    D_chi(t+w)=chi(w) D_chi(t).                             (1)

Thus only one residue up to sign is needed for each coset of U. Since
support points avoid the entire evaluation block, at most 2^h/|U|-1
such residues occur. This fact is true for ANY convolution kernel, not
only discrete logarithms. It is not itself a hardness result or a new
quantum mechanism.

The full Walsh matrix W_U satisfies W_U^2=|U| I. Since N=2^h-1 is odd,
|U| is a unit even when N is composite. Thus W_U is invertible over Z_N.
Taking the direct sum over a partition of all evaluation columns gives a
complete valid change of classical search basis, not a restriction to a
secret subspace or a different optimization problem. The existing solver's
argument called basis_inv accepts this update matrix: it uses B W_U and
updates x by a multiple of a column of W_U. No missing inverse is assumed.

For the native interval 6000..6419, the maximal aligned dyadic partition is

    6000+[0,16), 6016+[0,128), 6144+[0,256),
    6400+[0,16), 6416+[0,4).

All 256 directions in the largest block have exactly 24 distinct row-phase
values up to sign on the 6,000 actual rows. The general bound is 31. Exact
translation checks cover 25,231,360 scalar congruences across all blocks;
independent direct sums check transform signs and indexing. This count is
not a claim of independent theorem verification.

The block transform can be computed by O(m sum_U |U| log|U|) modular
operations using Walsh butterflies. The inherited solver in this experiment
still recomputes dense B W_U as part of its unchanged interface. No optimized
runtime or new asymptotic classical speedup is claimed.

## 3. Matched Native Results

Input: h=13, m=6000, n=420, N=8191, center seed 261006753. The field
polynomial, primitive generator, support/evaluation lists and center hash
are checked against the existing artifact. Its best assignment is replayed
before use. This is the repository instance, NOT a claimed reproduction
of the paper's differently seeded instance.

Each run used the unchanged fft_line_search body, with at most two full
sweeps. Every accepted candidate uses the full-row objective. The final
assignments are replayed through BOTH explicit B multiplication and the
original exact fast convolution, then scored using 96-bit Arb intervals.

| Start | Basis | Initial score | Final score | Scans | Accepted moves |
|---|---|---:|---:|---:|---:|
| Zero | Original | 0.0116794080 | 0.0457866694 | 840 | 2 |
| Zero | Affine Walsh | 0.0116794080 | 0.0556826324 | 840 | 8 |
| Inherited best | Original | 0.1166489027 | 0.1166489027 | 420 | 0 |
| Inherited best | Affine Walsh | 0.1166489027 | 0.1166489027 | 420 | 0 |

Total: 2,520 scanned lines, representing 20,641,320 scalar displacements
via FFTs. These are not 20 million independently materialized witnesses.
The target remains 0.3. All four returned scores are certified BELOW it.

Search decisions use the inherited floating FFT and its 1e-12 acceptance
tolerance. The score intervals certify the returned witnesses, NOT every
line comparison or an exact local-optimality theorem. In particular, zero
accepted moves is not a new rigorous heat-bath trap or a hardness claim.

The old README-style note BALANCED_SIGNED_MPI.md lists the zero-start
initial score as -0.006702. The existing JSON and this same-instance replay
both give +0.0116794080. The final 0.0457866694 and inherited best score
agree. Treat this as stale prose, not a changed instance; defer its small
correction until the checkout is no longer moving.

## 4. Small-Step Falsifier

One possible benefit of few frequencies is a scalar d such that all
centered d*D_chi(t) residues are small. For the five modes fixed before
execution, exhaustive integer minimax checks over all 8,190 nonzero d give:

| Mode | Best displacement | Largest centered residue / 8191 |
|---:|---:|---:|
| 0 | 1711 | 2678/8191 |
| 1 | 3513 | 2826/8191 |
| 2 | 2448 | 2833/8191 |
| 127 | 3420 | 2730/8191 |
| 255 | 2658 | 2787/8191 |

Even the best simultaneous steps rotate some rows by 0.327 to 0.346 full
turns. Hence these modes do not supply uniformly gentle steps at native
size. This is an exhaustive certificate only for these FIVE modes.

With K distinct frequencies, a pigeonhole argument among N torus points
can force a centered displacement of size at most N/Q per coordinate only
when Q^K<N. Here K=24 and N=8191, so the largest such integer Q is 1:
the generic bound is vacuous. The fact that K is constant along some
larger affine-block families does not create a useful native guarantee or
prove efficient optimization. For composite N a nonzero displacement also
need not be a unit; do not silently treat it as a new invertible basis.

## 5. Attempts To Prove The Proposal Wrong

- The sign-coset identity could have failed because of a truncated affine
  block. Every block is complete, disjoint, and checked; the identity holds.
- A different modulus or field presentation could have produced an easier
  input. The saved field, points, generator and center hash are verified.
- Improvement from zero could merely reflect a weak start. It does: neither
  basis improves the inherited stronger witness.
- A small frequency alphabet might imply small modular moves. The exact
  five-mode minimax result and vacuous native pigeonhole bound reject that
  inference for the tested directions.
- A search failure might be described as a quantum signal. It is not:
  only a bounded greedy algorithm was tested, with no lower bound against
  different moves, larger blocks, lattice methods or other classical solvers.
- The algebra depends on highly structured public point selection. It does
  not automatically extend to arbitrary random evaluation sets lacking large
  complete affine blocks. Their absence would not imply classical hardness.

## 6. Next Research Decision

Do not spend another pass changing the Walsh mode order, seed, or restart
budget. Reconsider this route only with a qualitatively new joint-mode
optimization mechanism or a theorem giving useful rounding/mixing under
the SAME input contract. The generic integer-lattice attack already exists
in the primary MPI paper; merely increasing its budget is execution work,
not new theory.

The larger unresolved issue remains a meaningful end-to-end application
or a serious classical complexity comparison for the constructive quantum
candidate. The new native failure does not make MPI Shor-level in relevance.

Prior art for MPI, its rational decoder and generic classical searches:
[Mazumder and Niroula](https://arxiv.org/html/2610.06753). This note derives
its own finite-block identity and records a bounded attack; it makes no
claim of novelty for Walsh diagonalization or change-of-basis search.
