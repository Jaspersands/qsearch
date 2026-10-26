# Standalone Guarded Cyclic-H Dispatcher And 127-Bit Row Compression

**Status: bounded reference implementation of the five-step trivial / normal /
transverse / abelian cyclic-H promise handler from actual normal-word coset
states; outer ISS normalizer recursion, general-prime SDE backend, and full
class-three HSP remain unexecuted.**

## Scope And Motivation

In `theorems/nil3_cocycle_receiver.py`, `learn_quotient_line` assumes a
nontrivial cyclic subgroup transverse to the derived ideal $N = [G,G]$ and
terminates as soon as the observed Fourier frequencies in $\mathbb{F}_p^m$
reach rank $m-1$. As documented in `research/NIL3_NORMAL_WORD_BRIDGE.md`
("Two Missing Promise Cases In The Current Receiver") and
`research/CLASS_THREE_HSP_THEOREM_DRAFT.md` ("The Cyclic Promise Handler"),
the published reduction of [Ivanyos, Sanselme and Santha (2010)](https://www.irif.fr/~santha/Papers/iss12.pdf)
produces subproblems with $|H| \in \{1, p\}$ where $H$ may be:

1. **Abelian ambient** ($[G,G] = 1$, $|H| \in \{1, p\}$),
2. **Normal cyclic** ($H \le N = [G,G]$, $|H| = p$),
3. **Trivial** ($H = \{1\}$ in a nonabelian class-$\le 3$ group), or
4. **Transverse cyclic** ($H \cap N = \{1\}$, $|H| = p$).

`theorems/nil3_guarded_cyclic_dispatch.py` implements this complete five-step
guarded dispatch directly on a supplied `NormalWordLieBridge` and actual
normal-word coset states without modifying the upstream bridge or receiver
artifacts.

## Five-Step Guarded Dispatch And Fixed-Batch Accounting

Given `bridge: NormalWordLieBridge(p, d, collect)` ($p \equiv 11 \pmod{12}$
for the reference degree-3/degree-2 phase-erasure backend) and error target
$\epsilon \in (0, 1/2]$ with $\eta = \epsilon / 8$:

1. **Public Presentation & Abelian Routing**:
   Using `adapted_presentation_exact(bridge)` (backed by arbitrary-precision
   `fmpz_mod_mat` RREF), compute all $\binom{d}{2}$ generator brackets. If all
   brackets vanish, route directly to the abelian HSP handler using a fixed
   batch of $t_G = d + \lceil \log_p(1/\eta) \rceil + 1$ original coset copies:
   - Nullity `0` (rank $d$): return `ABELIAN_TRIVIAL` (`generators = []`).
   - Nullity `1` (rank $d-1$): return `ABELIAN_CYCLIC`.
   - Nullity `> 1`: return `INCOMPLETE_ABELIAN_RANK_FAILURE` (`generators = None`).
2. **Normal-Intersection Stage ($H \le N$)**:
   On $t_N = n + \lceil \log_p(1/\eta) \rceil + 1$ fresh original cosets,
   convert normal words to adapted chart coordinates `(q, normal)`, measure
   $q$, apply the public inverse conjugation twist $\Phi(-q)$, and sample a
   Fourier frequency on $\mathbb{F}_p^n$:
   - Nullity `1` (rank $n-1$): return `NORMAL_CYCLIC` after mapping the learned
     normal generator back to a normal word via `bridge.element(forward * v)`.
   - Nullity `> 1`: return `INCOMPLETE_NORMAL_RANK_FAILURE`.
   - Nullity `0` (rank $n$): $H \cap N = \{1\}$; proceed to quotient phase erasure.
3. **Collective Affine-Support Phase Erasure**:
   Produce a fixed batch of $t_V = m + \lceil \log_p(1/\eta) \rceil + 1$
   phase-erased quotient states (`copy_budget(m, n)` original cosets per output).
   Both $H = \{1\}$ (support size $1$ per branch) and transverse cyclic $|H| = p$
   (support size $p$ per branch) pass through the same public controller without
   branching on state support size.
4. **Fixed-Batch Quotient Annihilator Resolution**:
   Evaluate all $t_V$ quotient Fourier frequencies before solving the homogeneous
   system over $\mathbb{F}_p^m$:
   - Nullity `0` (full rank $m$): return `TRIVIAL` (`generators = []`).
   - Nullity `1` (rank $m-1$): extract the learned quotient direction $v \in \mathbb{F}_p^m$
     and proceed to Step 5.
   - Nullity `> 1`: return `INCOMPLETE_QUOTIENT_RANK_FAILURE`.
5. **Quadratic HPGP Normal-Coordinate Completion**:
   Only when nullity is `1`, invoke `learn_normal_generator(group, adapted_source, direction, rng)`
   on fresh adapted coset states, combine `(direction, normal_coord)` via
   `group.from_chart`, and map back to the normal-word presentation.

### Executed Controls (`p = 11`, $\epsilon = 1/3$)

| Presentation | True Case | Generator Fixture | Dispatched Case | Normal Copies | Erasure Copies | HPGP Copies | Total Oracle Copies | Exact Subgroup Recovered |
|---|---|---|---|---:|---:|---:|---:|---|
| 4D non-split filiform class-3 ($m=2, n=2$) | `TRIVIAL` | `(0, 0, 0, 0)` | `TRIVIAL` | 5 | 9,555 | 0 | 9,560 | `True` |
| 4D non-split filiform class-3 ($m=2, n=2$) | `NORMAL_CYCLIC` | `(0, 2, 0, 5)` | `NORMAL_CYCLIC` | 5 | 0 | 0 | 5 | `True` |
| 4D non-split filiform class-3 ($m=2, n=2$) | `TRANSVERSE_CYCLIC` | `(1, 3, 2, 4)` | `TRANSVERSE_CYCLIC` | 5 | 9,555 | 7 | 9,567 | `True` |
| 3D abelian $\mathbb{F}_{11}^3$ ($d=3$) | `ABELIAN_TRIVIAL` | `(0, 0, 0)` | `ABELIAN_TRIVIAL` | 6 | 0 | 0 | 6 | `True` |
| 3D abelian $\mathbb{F}_{11}^3$ ($d=3$) | `ABELIAN_CYCLIC` | `(2, 5, 7)` | `ABELIAN_CYCLIC` | 6 | 0 | 0 | 6 | `True` |

## Arbitrary-Precision Row Compression And Capped Conic Solver

To address the general-prime backend contract without mutating frozen upstream
modules, `theorems/nil3_guarded_cyclic_dispatch.py` also provides:

- `independent_columns_exact(columns, p)`: uses FLINT `fmpz_mod_mat(..., fmpz_mod_ctx(p)).rref()`
  to compress equation rows while preserving every physical input column at
  arbitrary prime bit-lengths (verified at the 127-bit Mersenne prime $p = 2^{127}-1$).
- `square_weights_capped(p, columns, rng, conic_attempt_cap=128)` and
  `conic_failure_bound(p, attempts)`: replaces the unbounded conic search loop
  with a deterministic attempt cap $T$ whose exact failure probability on
  uniform draws from $\mathbb{F}_p$ ($p \equiv 3 \pmod 4$) is
  $\left(\frac{p-1}{2p}\right)^T < 2^{-T}$.

## Reproduction

```
python -m theorems.nil3_guarded_cyclic_dispatch --write
python -m pytest -q tests/test_nil3_guarded_cyclic_dispatch.py -W error::RuntimeWarning
```
