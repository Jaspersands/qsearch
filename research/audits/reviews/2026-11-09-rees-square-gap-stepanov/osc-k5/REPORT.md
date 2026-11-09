# OSC at κ = 5: report (exact computations; all files in `research/audits/reviews/2026-11-09-rees-square-gap-stepanov/osc-k5/`)

AI-only (2026-11-09). A compute subagent wrote this report; the parent saved it unchanged below this line. Pending human review.


The new enumerator reproduces `orbit_types_fast` exactly at p = 271 and 311. PW_pair is below 1 at every tested prime from 821 to 2311, and PW at every tested prime from 1231 to 2311. Both crossings are far below the O1 barrier 2628. (N) and (L) look bounded. **(H) as stated looks false at κ = 5:** B_H grows like p^{2.3}, because the (3,3) classes sit at |F̂|/F̂(0) ≈ c/p.

## 1. Enumerator and validation [computed]

- **Files.** `osc_kernel.c` is a C kernel called through ctypes, with `nice -n 19` and 2 threads per run. `osc_k5.py` is the driver plus the statistics, using the cert_check definitions.
- **What it computes.** The same F(U,V) as `orbit_types_fast`, with two reductions:
  - S is enumerated unlabelled mod PGL₂. It uses the lexicographic-minimum normal form, weighted by orbit size 5!/|Stab|, and the V-labels are re-symmetrised over S₅ afterwards.
  - T is never enumerated. For each (S, z, bucket), every 5-multiset of U-values is added with weight ∏C(m_a, n_a), then relabelled with weight ∏n_a!.
- **Speed.** Enumeration at p = 271 takes 0.03 s (the reference takes 34 s). Run cost grows like p^{4.5}: 0.31 core-h at 2011, 0.41 at 2111, 0.76 at 2311.
- **Validation.**
  - `validate_k5.out`: at p = 271 and 311 the full 5^10 F array is identical to `orbit_types_fast.run` (max |ΔF| = 0). Rees = 50 and 1450; PW = 18.116 and 9.339.
  - `validate_k4.out`: at κ = 4, p = 61, 149, 197, 229, 509, F is identical to `sep_types`. PW, PW_pair, N₁/μ₁, B_L_cc and B_H_cc all reproduce `cert_k4.out` (for example p = 149: 0.7307 / 0.391 / 1.026 / 12.388).
  - Every run satisfies these internal checks:
    - the sum of orbit sizes equals (p−2)(p−3);
    - N₁ from the kernel equals F̂(0)/κ²;
    - the F values are integral.
- **Primes covered.** The six primes of the stopped parent sweep (401, 521, 641, 761, 881, 1031) are in `sweep_C_parentprimes.out`. They agree with the parent's 401 and 521 values (PW 4.486 / 1.945, Rees 12700 / 38800).
- **Runs stopped.** All of these were my own processes:
  - 2521 was killed at the 1 h wall cutoff, with no result;
  - 2711 was stopped because it was projected over 1 h;
  - 2801, 3001 and 3461 were never run, per the budget.

## 2. Per-prime table [computed]

Sources: `summary.out`, built from `sweep_A.out`, `sweep_B1.out`, `sweep_B2.out`, `sweep_B3.out`, `sweep_C_parentprimes.out`, `run_1051.out` and `validate_k5.out`.

Column definitions:
- λ = p/625.
- B_L = max over non-pair classes with m ≤ 5 of n|F̂|/(κF̂(0)).
- B_H = max over non-pair classes with m ≥ 6 of |F̂|/(√(m/N₁)F̂(0)).
- sh_pair, sh_L, sh_H = the parts of PW_pair coming from pair classes, L classes and H classes.

| p | λ | Rees | PW | PW_pair | N₁/μ₁ | B_L | B_H | sh_pair | sh_L | sh_H |
|---|---|---|---|---|---|---|---|---|---|---|
| 181 | .29 | 0 | 34.8 | 21.7 | .840 | 4.99 | 74 | .062 | 3.75 | 17.9 |
| 191 | .31 | 0 | no (C1) configuration | | | | | | | |
| 211 | .34 | 0 | 32.0 | 21.1 | .140 | 1.83 | 62 | .033 | 2.76 | 18.4 |
| 241 | .39 | 0 | no (C1) configuration | | | | | | | |
| 251 | .40 | 0 | 19.5 | 13.5 | .121 | 1.51 | 67 | .025 | 1.59 | 11.9 |
| 271 | .43 | 50 | 18.1 | 12.9 | .117 | 2.06 | 91 | .035 | 1.69 | 11.1 |
| 281 | .45 | 50 | 10.6 | 7.52 | .288 | 1.56 | 74 | .008 | 1.45 | 6.06 |
| 311 | .50 | 1450 | 9.34 | 6.77 | .411 | 1.25 | 66 | .020 | 1.42 | 5.32 |
| 331 | .53 | 1750 | 7.20 | 5.26 | .343 | .80 | 84 | .025 | 1.00 | 4.24 |
| 401 | .64 | 12700 | 4.49 | 3.37 | .800 | 1.01 | 67 | .013 | 1.02 | 2.34 |
| 421 | .67 | 4500 | 3.42 | 2.56 | .275 | .44 | 56 | .008 | .68 | 1.87 |
| 431 | .69 | 7450 | 2.93 | 2.18 | .272 | .49 | 62 | .004 | .48 | 1.69 |
| 461 | .74 | 21600 | 2.93 | 2.22 | .577 | .41 | 65 | .005 | .56 | 1.65 |
| 491 | .79 | 64700 | 3.85 | 3.02 | .737 | .70 | 80 | .013 | .97 | 2.04 |
| 521 | .83 | 38800 | 1.94 | 1.47 | .327 | .26 | 77 | .003 | .42 | 1.05 |
| 541 | .87 | 128960 | 2.67 | 2.09 | .790 | .53 | 113 | .008 | .77 | 1.32 |
| 571 | .91 | 112250 | 1.86 | 1.43 | .531 | .36 | 71 | .005 | .51 | .91 |
| 601 | .96 | 212360 | 1.62 | 1.24 | .578 | .38 | 90 | .006 | .51 | .73 |
| 631 | 1.01 | 317925 | 1.63 | 1.26 | .570 | .40 | 119 | .006 | .53 | .73 |
| 641 | 1.03 | 246750 | 1.30 | **.985** | .442 | .31 | 89 | .004 | .36 | .62 |
| 661 | 1.06 | 338625 | **.947** | .696 | .552 | .36 | 123 | .004 | .30 | .39 |
| 691 | 1.11 | 698900 | 1.89 | 1.52 | .617 | .34 | 158 | .004 | .43 | 1.09 |
| 701 | 1.12 | 993975 | 1.69 | 1.35 | .772 | .49 | 203 | .005 | .54 | .81 |
| 751 | 1.20 | 1179075 | 1.37 | 1.09 | .564 | .51 | 189 | .005 | .37 | .71 |
| 761 | 1.22 | 1429335 | 1.13 | .877 | .616 | .33 | 181 | .004 | .42 | .45 |
| 811 | 1.30 | 2902010 | 1.31 | 1.05 | .697 | .37 | 287 | .006 | .38 | .67 |
| 821 | 1.31 | 2349425 | 1.14 | .908 | .596 | .50 | 212 | .005 | .37 | .53 |
| 881 | 1.41 | 4301000 | .702 | .527 | .611 | .24 | 214 | .001 | .20 | .32 |
| 911 | 1.46 | 6208425 | .905 | .715 | .638 | .23 | 320 | .003 | .24 | .47 |
| 941 | 1.51 | 8907825 | 1.001 | .807 | .722 | .36 | 420 | .003 | .37 | .44 |
| 971 | 1.55 | 12114400 | .641 | .487 | .796 | .39 | 356 | .002 | .26 | .23 |
| 991 | 1.59 | 13476950 | .682 | .526 | .761 | .32 | 446 | .001 | .23 | .30 |
| 1021 | 1.63 | 14455725 | .450 | .320 | .704 | .31 | 237 | .001 | .17 | .15 |
| 1031 | 1.65 | 17132585 | .486 | .355 | .721 | .32 | 332 | .002 | .19 | .16 |
| 1051 | 1.68 | 17126050 | .395 | .274 | .664 | .25 | 218 | .000 | .15 | .13 |
| 1061 | 1.70 | 19447710 | .403 | .283 | .728 | .38 | 156 | .001 | .17 | .11 |
| 1091 | 1.75 | 23266020 | .374 | .260 | .688 | .34 | 154 | .001 | .16 | .10 |
| 1151 | 1.84 | 41745695 | .473 | .354 | .714 | .22 | 450 | .001 | .15 | .20 |
| 1171 | 1.87 | 47515850 | .312 | .209 | .746 | .26 | 287 | .001 | .11 | .10 |
| 1181 | 1.89 | 51577735 | .474 | .359 | .743 | .31 | 534 | .001 | .20 | .16 |
| 1201 | 1.92 | 70370125 | 1.13 | .967 | .787 | .40 | 999 | .004 | .32 | .65 |
| 1231 | 1.97 | 63222310 | .296 | .200 | .714 | .39 | 154 | .001 | .13 | .07 |
| 1291 | 2.07 | 104038050 | .547 | .435 | .728 | .47 | 780 | .002 | .21 | .23 |
| 1301 | 2.08 | 128144960 | .893 | .757 | .783 | .44 | 1164 | .003 | .25 | .51 |
| 1321 | 2.11 | 117726875 | .269 | .180 | .745 | .30 | 296 | .001 | .11 | .07 |
| 1361 | 2.18 | 171290350 | .672 | .556 | .759 | .49 | 1134 | .002 | .21 | .34 |
| 1381 | 2.21 | 216292285 | .641 | .529 | .857 | .45 | 1255 | .002 | .26 | .27 |
| 1451 | 2.32 | 292718360 | .503 | .405 | .772 | .38 | 1224 | .002 | .18 | .23 |
| 1471 | 2.35 | 314554135 | .315 | .232 | .814 | .35 | 880 | .001 | .13 | .10 |
| 1481 | 2.37 | 292915420 | .228 | .151 | .747 | .35 | 360 | .000 | .10 | .05 |
| 1511 | 2.42 | 392664225 | .291 | .210 | .790 | .24 | 1122 | .001 | .12 | .09 |
| 1601 | 2.56 | 628747325 | .308 | .231 | .806 | .30 | 1328 | .001 | .13 | .10 |
| 1801 | 2.88 | 1464438770 | .172 | .111 | .776 | .35 | 690 | .000 | .07 | .04 |
| 2011 | 3.22 | 3861569335 | .184 | .127 | .810 | .34 | 1825 | .000 | .08 | .05 |
| 2111 | 3.38 | 6200973785 | .225 | .170 | .871 | .41 | 2790 | .001 | .11 | .06 |
| 2311 | 3.70 | 12417441600 | .177 | .128 | .849 | .39 | 3440 | .000 | .08 | .04 |

Sanity checks:
- Rees = 0 only at 181, 211 and 251.
- 191 and 241 have no (C1) configuration at all.
- Rees > 0 at every other tested p > 181.

## 3. Crossing points [computed]

Source: `trend_421.out`.

- **PW_pair.**
  - First below 1 at p = 641 (0.985).
  - Still ≥ 1 at 691, 701, 751 and 811.
  - Below 1 at every tested prime from 821 to 2311.
- **PW.**
  - First below 1 at p = 661.
  - Still ≥ 1 at 691–821, 941 (1.001) and 1201 (1.13).
  - Below 1 at every tested prime from 1231 to 2311.
- **Against the barriers.** Both crossings are far below the O1 barrier 2628 and T_A(5) ≈ 1.25·10⁴. They are also below T_strong(1) = 3450.
- **Decay.** Over p ≥ 421 the log-log slope is about −1.85 for both PW and PW_pair. The decay is not monotone: there are prime-dependent spikes, for example 1201, 1301 and 1361.
- **Limitations.**
  - Primes 2521–2628 were not reached.
  - These are finite values at single primes, not an asymptotic statement.
  - A p⁻² trend would leave PW_pair ≈ 0.1 at 2628 [heuristic extrapolation].

## 4. OSC parts

**(N): bounded, no adverse drift [computed].**
- N₁/μ₁ is 0.12–0.42 for p ≤ 331, where λ < 0.55.
- It is 0.27–0.87 for p ≥ 401, and it creeps upward (slope +0.45).
- It is 0.85 at 2311. This is consistent with the (N) agent's proof of B ≤ 8.6 near λ ≈ 4.8.

**(L): bounded, slight downward drift [computed].**
- B_L is 0.22–0.70 for p ≥ 421 (slope −0.15), and 0.39 at 2311.
- It is larger only at small p: 1.3–5.0 for p ≤ 311.
- The cert_check version B_L_cc, which includes pair classes, stays at about 1.0.

**(H): fails as stated; B_H drifts like p^{2.3} [computed].**
- B_H goes 56 → 3440 over 421–2311, with log-log slope +2.26.
- Over 1021–2311 the m = 6 maximum is always attained by the (3,3) class. The (2,4) class reaches about 1170–1260 there.
  - The maximising ρ has r and c with the same value multiset, for example {0,0,1,2,2} / {0,0,1,2,2} or {0,0,1,1,3} / {0,0,1,1,3}.

Decay of n|F̂|/F̂(0) by class (`class_fit.out`, from `analyze2_*.out`; RMS is taken over the whole class):

| class | RMS slope, p ≥ 1021 | RMS slope, p ≥ 661 | value at 2311 (max / RMS) | so \|F̂\|/F̂(0) behaves like |
|---|---|---|---|---|
| (2,2) | +0.08 | | 1.95 / 1.27 | exactly 1/p |
| (2,3) | −0.04 | | 0.12 / 0.10 | 1/p |
| (3,3) | +0.15 | −0.57 | 0.29 / 0.155 | 1/p; never as small as √(m/N₁) ~ p⁻⁴ |
| (2,4) | −0.68 | | max ≈ flat, median ≈ p^{-1.3} | |
| (4,4) | | −1.8 | | ≈ p^{-2.8} |
| (5,5) | | −2.5 | | ≈ p^{-3.5}; B_H(m=10) roughly flat at 41–270, slope +0.3 |

B_H restricted to m ≥ 7 still drifts mildly (slope +0.6; per-m slopes +1.0 to +1.5 for m = 7, 8, 9).

**Why B_H grows.**
- The (3,3) and (2,4) classes carry an O(1)/p bias, like the low-support classes, and not random-phase cancellation over the N₁ ~ p⁸/5¹⁶ orbits.
- So B_H ≈ (c/n)·√(N₁/m), which grows like p³ if c is constant. Fitted over all p it is about p^{2.3–2.6}, because c is still settling at small p.
- Probable source [heuristic, unproved]: a boundary term, as in Theorem 3. The z-sum runs over P¹∖(S∪T), and the 2κ excluded points give O(κ)/n terms. These terms do not cancel over (C1) orbits when the r- and c-patterns align.

**Scaling law the data support.**
- Every non-pair class satisfies |F̂(ρ)| ≤ B·κ·F̂(0)/n with B_all ≤ 0.71 for p ≥ 421 (0.39 at 2311, slope −0.15).
- In the data:
  - the 1/p bias reaches total support m = 6;
  - only m ≥ 7 decays faster, at about p^{-2.3} to p^{-3.5};
  - √(m/N₁) is reached only near m = 10.

**Rough consequence [estimate].** Moving the m = 6 classes into (L) raises the low weight from 698 to about 1798. The leading term of T_strong(B) becomes about 5·B·1798 ≈ 9·10³·B, which is still below T_A(5) = 1.25·10⁴ for B = 1. The observed PW_pair is far smaller than this bound, because most classes sit well below their class maximum.

## 5. Claim gates (stay false)

- OSC is proved, or (H) is disproved. The evidence for both is finite data.
- PW_pair < 1 for every p ≥ 821.
- Any statement for p in [2311, 2628].
- These numbers have had a second independent check beyond the exact F-array match with `orbit_types_fast` and `sep_types`.

**Next.**
- Run p = 2521 and 2621 on a less loaded machine. At about 1.0–1.2 core-h each, they must each be a single run.
- Try to prove the 1/p boundary term for the matched (3,3) classes, which would replace (H) at m = 6 by an (L)-type bound.

Other files in that folder:
- `summarize.py`, `trend.py`, `analyze2.py`, `class_fit.py`: post-processing.
- `acc_k5_p*.npy`: raw kernel output for every computed prime, so any statistic can be recomputed without enumerating again.