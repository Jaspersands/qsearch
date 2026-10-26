# Full-Target Classical Feedback, Multilevel Beam Search, J16 Scaling, And 924-Bit Cosine Attacks

## Result And Decision

A fixed-budget, full-target-aware nearest-plane search (`integer_character_feedback_v2`),
along with a non-greedy multilevel beam search (`multilevel_beam_search`), a
predeclared multi-length/multi-center J16 scaling campaign (`multi_length_j16_campaign`
across $m \in \{32, 64, 96, 128\}$), and a matched 924-bit $J=1$ cosine attack campaign
(`cosine_family_924bit_attack_campaign`), was executed on the SAME 1024-coordinate J16
input (`seed = 2026102016`, 1119-bit cyclic order, saved reduced basis), on finite J16
controls at $m \in \{32, 64, 96, 128\}$, and on the frozen 924-bit $J=1$ prime-character
instance (`seeds = 2026102001, 2026102002`). Neither the modulus, center vector nor
acceptance thresholds (`0.065` for $J=16$ squared distance, `0.3` for $J=1$ cosine) changed.

On the native $m=1024$ J16 instance, neither greedy 24-level feedback nor width-4
multilevel beam search improved on the `.06266165019` last-plane seed:

| Native $m=1024$ Comparator | Levels / Planes | Proposals | Distinct Assignments | Distinct `D <= 0.065` Witnesses | Best Mean Square $D$ | Strict Improvements |
|---|---|---:|---:|---:|---:|---:|
| Greedy feedback (`feedback_search`, $r=4$) | `188..165` (24 levels) | 216 | 193 | 6 | `0.06266165019` | 0 |
| Non-greedy beam (`multilevel_beam_search`, $B=4, r=2$) | `188..186` (3 levels) | 60 | 52 | 2 | `0.06266165019` | 0 |

## Multi-Length J16 Scaling And The LLL Read-Fraction Transition ($m \in \{32, 64, 96, 128, 1024\}$)

Across $m \in \{32, 64, 96, 128\}$ (2 predeclared center seeds per length, with separate
finite-length $J=16$ quantum certificates and full LLL / basis-profile accounting),
the LLL coordinate-prefix (`blind_rank > 0`) emerges between $m=64$ and $m=96$, and once
`blind_rank > 0` ($m \in \{96, 128\}$), non-greedy `multilevel_beam_search` ($B=3, r=2$)
strictly improves over 33-branch last-plane branching on **all 4 out of 4 seeds**
(and single-winner greedy feedback strictly improves on `seed = 2026114801` at $m=128$):

| Length `m` | Cap | Order Bits | LLL Prefix (`blind_rank`) | Core (`read_count`) | Read Fraction | Center Seed | Plain Babai $D$ | 33-Branch Last Plane $D$ | Greedy Feedback $D$ | Multilevel Beam $D$ |
|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|
| 32 | 1 | 130 | 0 | 32 | `1` (`32/32`) | `2026105201` | `0.000397` | `0.000349` | `0.000349` | **`0.000266`** |
| 32 | 1 | 130 | 0 | 32 | `1` (`32/32`) | `2026105202` | `0.000335` | `0.000335` | `0.000335` | `0.000335` |
| 64 | 2 | 168 | 0 | 64 | `1` (`64/64`) | `2026108401` | `0.004060` | `0.004060` | `0.004060` | `0.004060` |
| 64 | 2 | 168 | 0 | 64 | `1` (`64/64`) | `2026108402` | `0.004592` | `0.004410` | `0.004410` | **`0.004129`** |
| 96 | 3 | 200 | 9 | 87 | `29/32` (`87/96`) | `2026111601` | `0.021911` | `0.017798` | `0.017798` | **`0.015399`** |
| 96 | 3 | 200 | 9 | 87 | `29/32` (`87/96`) | `2026111602` | `0.018850` | `0.017895` | `0.017895` | **`0.016611`** |
| 128 | 4 | 230 | 38 | 90 | `45/64` (`90/128`) | `2026114801` | `0.032761` | `0.027646` | **`0.026084`** | **`0.026084`** |
| 128 | 4 | 230 | 38 | 90 | `45/64` (`90/128`) | `2026114802` | `0.041422` | `0.028652` | `0.028652` | **`0.026643`** |
| 1024 | 35 | 1119 | 834 | 190 | `95/512` (`190/1024`) | `2026102016` | `0.068841` | `0.062662` | `0.062662` | `0.062662` |

### Why Read Fraction Drops From `1` ($m=32, 64$) To `29/32` ($m=96$), `45/64` ($m=128$), And `95/512` ($m=1024$)

The dual numerator lattice $\Gamma_{\text{num}} = a \mathbb{Z} + N \mathbb{Z}^m$ has determinant
$N^{m-1}$, so a reduced vector has heuristic norm $\approx \gamma^{m/2} N^{(m-1)/m} = N \cdot \gamma^{m/2} N^{-1/m}$.
At $m=32$ ($\log_2 N / m \approx 4.06$) and $m=64$ ($\log_2 N / m \approx 2.63$), $N^{1/m}$ dominates
the LLL root-Hermite factor $\gamma^{m/2}$, so every reduced basis vector is shorter than $N$
(`blind_rank = 0`, `read_fraction = 1`). At $m=96$ (`200` bits, $\log_2 N / m \approx 2.08$) and
$m=128$ (`230` bits, $\log_2 N / m \approx 1.80$), the non-trivial core dimension stabilizes near
$d \approx 87\text{--}90$ while the remaining $9$ and $38$ rows stay at length $N$ (`±N e_j`).
At $m=1024$ (`1119` bits, $\log_2 N / m \approx 1.093$), LLL mixes $d = 190$ coordinates while
$834$ rows remain in the $\pm N e_j$ coordinate prefix (`read_fraction = 95/512 < 11/50 = 0.22`).

## Matched 924-Bit $J=1$ Cosine Attack Campaign (`cosine_family_924bit_attack_campaign`)

On the separate 924-bit $J=1$ public prime-character instance from
`research/phase_workbench/integer_character_interpolation.json` ($m=1024, \text{cap}=35, k=583, N=2 \cdot 3^{582}$,
source pilot mean lower bound `> 0.30404`), we evaluated 6 exact big-int classical methods
across 2 frozen independent uniform center seeds (`2026102001`, `2026102002`), verifying every
returned witness with 96-bit Arb ball intervals (`uniform.verify_score`):

| Method (`m=1024, 924-bit N`) | Evals | `seed = 2026102001` Arb Score Lower | `seed = 2026102002` Arb Score Lower | Accepted (`>= 0.3`) |
|---|---:|---:|---:|---|
| `zero_assignment_control` ($x=0$) | 1 | `-0.027279` | `0.011347` | `False` |
| `exact_crt_subgroup_order_162` ($x = 3^{k-1}e + 2 \cdot 3^{k-5}u$) | 162 | `0.045803` | `0.056009` | `False` |
| `padic_topdown_2trit_block_from_subgroup` (top 40 ternary places) | 482 | `0.051649` | `0.060995` | `False` |
| `tempered_padic_multistart_4x30` (4 CRT starts $\times$ 30 steps) | 124 | `0.059065` | `0.063118` | `False` |
| `row_subset_d64_lll_33branch` ($64 \times 64$ LLL + 33-branch Babai) | 33 | **`0.112904`** | **`0.113259`** | `False` |
| `row_subset_d64_lll_plus_padic_topdown_polish` | 233 | **`0.112904`** | **`0.113259`** | `False` |

This is a heuristic adaptation of standard nearest-plane branching, not a
new lattice algorithm. [Lindner and Peikert's nearest-planes attack](https://sites.cc.gatech.edu/fac/cpeikert/pubs/lwe-analysis.pdf)
is prior art for branching across multiple rounding planes.

## Reproduction

```
python theorems/integer_character_feedback.py --reuse-native-search
python -m pytest -q tests/test_integer_character_feedback.py -W error::RuntimeWarning
```

The producer reuses and verifies the saved paid basis; it does not rerun
the 1024-dimensional LLL. The original Babai and read-set artifacts are left unchanged.
