# Rees cloud harvest: hard29

- Session: `session_01B1JoCgWKMPfB1JJvQ1yAz6` (claude.ai/code cloud session; AI-only, pending human review)
- Started: 2026-11-04 05:01 UTC; final message: 2026-11-04 05:38 UTC (last event 2026-11-05 01:23)
- Asked: Decide the 29 hard κ=8 primes in (20000, 49417] that had no explicit contraction, with a solver written from the definition.
- Harvested 2026-11-05 from the session event stream; nothing in the session was committed or pushed.

## Cross-check against local results (2026-11-05)

- Verdict claims parsed (verdict lines plus verdicts stated in prose or as whole ranges): 35.
- Complete FEASIBLE/FOUND witnesses re-verified locally with `wcheck.py` (least primitive root, all κ² cells by the power test): 31 distinct primes, 0 bad.
- The 9697 validation witness in the final message (beta=0,237,... alpha=1,5305,...) also passes `wcheck.py`. Its 9473/9769 INFEASIBLE verdicts come from its own solver `rows.c` (different symmetry rule), cross-checked with the prune off and by a second solver.
- Against `k8dec.txt` / `k9dec.txt`: 35 agree, 0 conflict, 0 not in the local decided files.

## Extracted verdict lines

Regex over the whole event stream (tool outputs and messages), deduplicated to one line per (verdict, κ, p); where a line appeared several times the longest copy is kept, and `</event>` debris was stripped. Lines cut short in the transcript are kept as found.

```
INFEASIBLE k=8 p=9473 nodes=187674624 secs=176.1 shard=0/3
FEASIBLE k=8 p=9697 g=10 beta=0,5304,3118,3937,1416,5809,7995,7176 alpha=1,238,6888,5669,8280,8043,1393,2612
INFEASIBLE k=8 p=9769 nodes=73467171 secs=18.0
FEASIBLE k=8 p=22921 g=7 beta=0,33,9,14725,9460,10581,17267,3204 alpha=1,9156,10222,18967,17898,20984,17162,7269
FEASIBLE k=8 p=22937 g=3 beta=0,55,3013,12915,14574,9048,19937,14711 alpha=1,22129,20124,16161,3037,22849,4860,21792
FEASIBLE k=8 p=23417 g=3 beta=0,28,1037,10025,17921,18620,12949,11822 alpha=1,22313,8658,15516,12730,23355,5522,11830
FEASIBLE k=8 p=23993 g=3 beta=0,46,22,12210,17300,6330,4591,16189 alpha=1,9206,10204,22951,21742,10820,2605,18691
FEASIBLE k=8 p=24169 g=11 beta=0,21,17,22638,5536,12239,22256,16351 alpha=1,1866,797,17710,19533,9819,15212,11000
FEASIBLE k=8 p=24473 g=3 beta=0,44,288,3159,10561,11546,13353,15595 alpha=1,12886,7549,3408,17031,12330,12967,4287
FEASIBLE k=8 p=24841 g=14 beta=0,51,1647,713,6416,8132,17451,3079 alpha=1,693,9972,7873,14612,24373,1236,1726
FEASIBLE k=8 p=25097 g=3 beta=0,23,112,8461,10193,9652,17994,4478 alpha=1,6980,3010,16534,3046,20711,10122,3266
FEASIBLE k=8 p=25657 g=5 beta=0,12,93,14694,23533,14957,6112,5087 alpha=1,1360,23378,3951,18866,23625,19839,6907
FEASIBLE k=8 p=26041 g=13 beta=0,67,379,11056,19451,17236,24799,25685 alpha=1,8751,9374,15875,1850,9582,2521,22880
FEASIBLE k=8 p=26393 g=3 beta=0,9,25,8981,8689,11823,14166,4931 alpha=1,16233,12944,7820,22373,40,20311,15592
FEASIBLE k=8 p=26777 g=3 beta=0,9,699,15612,17724,19692,22322,298 alpha=1,20052,18968,12342,13474,15532,609,8338
FEASIBLE k=8 p=27673 g=11 beta=0,9,24,64,2632,1015,18934,20720 alpha=1,803,7328,1754,2704,2586,13212,5093
FEASIBLE k=8 p=27817 g=5 beta=0,39,231,22350,24243,19519,20516,23759 alpha=1,9433,26959,6958,12821,10394,13335,25007
FEASIBLE k=8 p=28409 g=3 beta=0,53,172,2510,17909,277,7768,27798 alpha=1,795,27041,20348,23262,7285,20882,23367
FEASIBLE k=8 p=28729 g=22 beta=0,105,74,9243,2397,7039,28623,12510 alpha=1,15916,1174,7708,7869,14419,13988,634
FEASIBLE k=8 p=29129 g=3 beta=0,37,175,27172,12784,13166,22200,19226 alpha=1,8948,22402,20213,11736,24561,7969,9103
FEASIBLE k=8 p=29881 g=7 beta=0,42,32,23132,23807,23458,783,5553 alpha=1,19674,28493,15824,11451,4919,15053,5331
FEASIBLE k=8 p=30313 g=5 beta=0,6,1,9131,18388,10759,29477,26654 alpha=1,20928,2061,24500,21437,4710,12382,15947
FEASIBLE k=8 p=30713 g=3 beta=0,9,13,22270,24833,499,14899,10682 alpha=1,24220,15375,8626,4985,19754,4920,7500
FEASIBLE k=8 p=31193 g=5 beta=0,18,7,18006,14684,9831,25301,7803 alpha=1,7085,17990,21174,19967,6029,11243,9190
FEASIBLE k=8 p=31721 g=11 beta=0,42,27,13983,9790,11578,8684,9763 alpha=1,26754,19417,10589,3538,25996,13372,7800
FEASIBLE k=8 p=32089 g=13 beta=0,70,18,12128,1453,15071,22482,28555 alpha=1,21639,10681,12509,14223,11011,25284,4454
FEASIBLE k=8 p=33353 g=3 beta=0,19,33,4145,13490,7840,13743,24763 alpha=1,26878,10660,32860,17131,27296,6860,32368
FEASIBLE k=8 p=34361 g=3 beta=0,22,32,15918,4426,5667,21160,23959 alpha=1,18552,14821,22635,3120,10780,21566,5573
FEASIBLE k=8 p=35401 g=13 beta=0,30,2,21498,27827,18778,21927,16919 alpha=1,22040,14144,19284,10944,5336,14881,18555
FEASIBLE k=8 p=36313 g=5 beta=0,29,1,17320,34346,8676,18805,16658 alpha=1,26389,26586,14998,27934,9914,2331,6060
FEASIBLE k=8 p=37369 g=7 beta=0,10,1,13160,37008,3446,4462,17767 alpha=1,28590,16303,13423,17689,34282,34268,22074
FEASIBLE k=8 p=38569 g=14 beta=0,12,7,6839,37800,2248,2559,20868 alpha=1,29465,14898,4705,34246,28627,17785,28433
FEASIBLE k=8 p=43177 g=5 beta=0,39,7,3462,30355,36739,30315,36811 alpha=1,18632,7648,26611,16689,17067,3567,10610
```

## Final result message (verbatim)

None of the 29 primes is in E_2(8): each one has a witness, and every witness passed a separate check of all 64 cells. That closes (20000, 49417] for K = 8. Nothing here raises the known maximum of E_2(8) above 9769.

I wrote the solvers from the definition and did not look at or reuse anything in the repository. Nothing was committed, pushed or opened as a PR.

## (1) Validation

| p | Expected | Got | Details |
|---|---|---|---|
| 9473 | INFEASIBLE | INFEASIBLE | 62,255,835 nodes, 15.3 s on 4 threads |
| 9697 | FEASIBLE | FEASIBLE | `beta=0,237,6887,5668,8279,8042,1392,2611 alpha=1,5305,3119,3938,1417,5810,7996,7177` (g=10) |
| 22921 | FEASIBLE | FEASIBLE | `beta=0,33,9,14725,9460,10581,17267,3204 alpha=1,9156,10222,18967,17898,20984,17162,7269` (g=7), 0.1 s |
| 9769 (extra) | INFEASIBLE, per the paper | INFEASIBLE | 73,467,171 nodes, 18.0 s |

Two cross-checks of 9473, because the symmetry prune is the only step that matters for INFEASIBLE claims:
- **Same solver, symmetry prune off:** INFEASIBLE, 935,954,836 nodes, 182 s.
- **A second, separate solver:** it branches on both alphas and betas, with forward checking, the same symmetry rule and 3 shards. INFEASIBLE, 563,716,664 nodes, about 530 core-seconds. It also finds the same 9697 witness.

## (2) Results

The script `verify.py` recomputes the least primitive root g and checks every cell by the 8th-power test. All 29 witnesses passed, and none has a zero cell.

```
FEASIBLE k=8 p=22937 g=3 beta=0,55,3013,12915,14574,9048,19937,14711 alpha=1,22129,20124,16161,3037,22849,4860,21792
FEASIBLE k=8 p=23417 g=3 beta=0,28,1037,10025,17921,18620,12949,11822 alpha=1,22313,8658,15516,12730,23355,5522,11830
FEASIBLE k=8 p=23993 g=3 beta=0,46,22,12210,17300,6330,4591,16189 alpha=1,9206,10204,22951,21742,10820,2605,18691
FEASIBLE k=8 p=24169 g=11 beta=0,21,17,22638,5536,12239,22256,16351 alpha=1,1866,797,17710,19533,9819,15212,11000
FEASIBLE k=8 p=24473 g=3 beta=0,44,288,3159,10561,11546,13353,15595 alpha=1,12886,7549,3408,17031,12330,12967,4287
FEASIBLE k=8 p=24841 g=14 beta=0,51,1647,713,6416,8132,17451,3079 alpha=1,693,9972,7873,14612,24373,1236,1726
FEASIBLE k=8 p=25097 g=3 beta=0,23,112,8461,10193,9652,17994,4478 alpha=1,6980,3010,16534,3046,20711,10122,3266
FEASIBLE k=8 p=25657 g=5 beta=0,12,93,14694,23533,14957,6112,5087 alpha=1,1360,23378,3951,18866,23625,19839,6907
FEASIBLE k=8 p=26041 g=13 beta=0,67,379,11056,19451,17236,24799,25685 alpha=1,8751,9374,15875,1850,9582,2521,22880
FEASIBLE k=8 p=26393 g=3 beta=0,9,25,8981,8689,11823,14166,4931 alpha=1,16233,12944,7820,22373,40,20311,15592
FEASIBLE k=8 p=26777 g=3 beta=0,9,699,15612,17724,19692,22322,298 alpha=1,20052,18968,12342,13474,15532,609,8338
FEASIBLE k=8 p=27673 g=11 beta=0,9,24,64,2632,1015,18934,20720 alpha=1,803,7328,1754,2704,2586,13212,5093
FEASIBLE k=8 p=27817 g=5 beta=0,39,231,22350,24243,19519,20516,23759 alpha=1,9433,26959,6958,12821,10394,13335,25007
FEASIBLE k=8 p=28409 g=3 beta=0,53,172,2510,17909,277,7768,27798 alpha=1,795,27041,20348,23262,7285,20882,23367
FEASIBLE k=8 p=28729 g=22 beta=0,105,74,9243,2397,7039,28623,12510 alpha=1,15916,1174,7708,7869,14419,13988,634
FEASIBLE k=8 p=29129 g=3 beta=0,37,175,27172,12784,13166,22200,19226 alpha=1,8948,22402,20213,11736,24561,7969,9103
FEASIBLE k=8 p=29881 g=7 beta=0,42,32,23132,23807,23458,783,5553 alpha=1,19674,28493,15824,11451,4919,15053,5331
FEASIBLE k=8 p=30313 g=5 beta=0,6,1,9131,18388,10759,29477,26654 alpha=1,20928,2061,24500,21437,4710,12382,15947
FEASIBLE k=8 p=30713 g=3 beta=0,9,13,22270,24833,499,14899,10682 alpha=1,24220,15375,8626,4985,19754,4920,7500
FEASIBLE k=8 p=31193 g=5 beta=0,18,7,18006,14684,9831,25301,7803 alpha=1,7085,17990,21174,19967,6029,11243,9190
FEASIBLE k=8 p=31721 g=11 beta=0,42,27,13983,9790,11578,8684,9763 alpha=1,26754,19417,10589,3538,25996,13372,7800
FEASIBLE k=8 p=32089 g=13 beta=0,70,18,12128,1453,15071,22482,28555 alpha=1,21639,10681,12509,14223,11011,25284,4454
FEASIBLE k=8 p=33353 g=3 beta=0,19,33,4145,13490,7840,13743,24763 alpha=1,26878,10660,32860,17131,27296,6860,32368
FEASIBLE k=8 p=34361 g=3 beta=0,22,32,15918,4426,5667,21160,23959 alpha=1,18552,14821,22635,3120,10780,21566,5573
FEASIBLE k=8 p=35401 g=13 beta=0,30,2,21498,27827,18778,21927,16919 alpha=1,22040,14144,19284,10944,5336,14881,18555
FEASIBLE k=8 p=36313 g=5 beta=0,29,1,17320,34346,8676,18805,16658 alpha=1,26389,26586,14998,27934,9914,2331,6060
FEASIBLE k=8 p=37369 g=7 beta=0,10,1,13160,37008,3446,4462,17767 alpha=1,28590,16303,13423,17689,34282,34268,22074
FEASIBLE k=8 p=38569 g=14 beta=0,12,7,6839,37800,2248,2559,20868 alpha=1,29465,14898,4705,34246,28627,17785,28433
FEASIBLE k=8 p=43177 g=5 beta=0,39,7,3462,30355,36739,30315,36811 alpha=1,18632,7648,26611,16689,17067,3567,10610
```

Time to the first witness ranged from 0.1 s to 17.5 s per prime (22937 and 24841 were the slowest). The node counts I logged are lower bounds, because a thread adds its count only when it finishes a root value.

**Why the earlier searches likely missed these:** the canonical form below forces 1 + beta_1 to be the smallest of all 128 cell ratios. So in every orbit there is a witness with very small beta_1 (6 to 105 here). Scanning beta_1 upward from 0 reaches it almost at once.

## (3) Solver source

The main solver is `rows.c`, shown in full below. It builds with `gcc -O3 -march=native -pthread rows.c -o rows` and runs as `./rows <p> -j 4 [-T cap] [-u to turn the prune off] [-t self-test]`. The mixed cross-check solver `e2k8.c` and the witness checker `verify.py` are in the same folder; I can paste them too.

```c
/*
 * rows.c -- exhaustive decision of p in E_2(8), "rows first" search.
 *
 * PROBLEM. K = 8, g = least primitive root mod p (p = 1 mod 8), Q_m = {y != 0 : log_g y = m mod 8},
 * A_m = Q_m u {0}.  Decide whether alpha, beta in F_p^8 exist with alpha_0 = 1, beta_0 = 0 and
 *        M_ij = alpha_j + beta_i in A_{-(i+j) mod 8}   for all i, j in Z_8.
 *
 * SEARCH.  The rows beta_1, ..., beta_7 are assigned in this order (DFS).  The columns are never
 * branched on: for each column j = 1..7 we keep the set S_j of alpha_j values compatible with
 * every assigned row (row 0 gives alpha_j in A_{-j}).  Once all rows are fixed the columns are
 * independent of each other (every constraint couples one alpha and one beta), so a solution
 * exists below a full row assignment iff every S_j is nonempty; any choice alpha_j in S_j is a
 * solution.  A partial row assignment with some S_j empty has no extension (S_j can only
 * shrink), so pruning it is sound.  Column 0 (alpha_0 = 1) restricts row i to
 * D_i = { b : 1 + b in A_{-i} }.
 *
 * CANDIDATE GENERATION (exact, no pruning).  For row r and a value a in S_j, let
 * T_{r,a} = { b in D_r : a + b in A_{-(r+j)} } stored as a bitset over D_r.  The candidates for
 * row r are exactly AND_j OR_{a in S_j} T_{r,a}: b survives iff every S_j keeps a value.
 * T_{r,a} is computed from the cyclotomic sets Z(s,t) = { z : z in A_s, z+1 in A_t }:
 * with y = 1 + b and d = a - 1, the conditions are y in A_{-r}, y + d in A_{-(r+j)}.  If d = 0
 * this forces y in A_{-r} n A_{-(r+j)} = {0} (j != 0).  If d != 0, d in Q_e, write y = d z
 * (a bijection z <-> y); since 0 lies in every A_m and Q_a Q_b = Q_{a+b}, y in A_{-r} iff
 * z in A_{-r-e}, and y + d = d(z+1) in A_{-(r+j)} iff z+1 in A_{-(r+j)-e}.  So
 * T_{r,a} = { d z - 1 : z in Z(-r-e, -(r+j)-e) }.  (Self-test option -t checks this against the
 * definition by brute force.)
 *
 * SYMMETRY BREAKING (sound; proof).
 *  (a) Recentring.  If (alpha,beta) is a solution with matrix M and M_st != 0, then
 *      M'_ij = M_{i+s,j+t}/M_st is the matrix of a normalised solution: M_{i+s,j+t} lies in
 *      A_{-(i+j)-(s+t)}, 1/M_st lies in Q_{s+t} (M_st in Q_{-(s+t)}), Q_a Q_b = Q_{a+b}, and 0
 *      times anything is 0, so M'_ij in A_{-(i+j)}; M' is a sum matrix with
 *      alpha'_j = (alpha_{j+t} + beta_s)/M_st, beta'_i = (beta_{i+s} - beta_s)/M_st, giving
 *      beta'_0 = 0, alpha'_0 = 1.
 *  (b) A normalised solution is determined by its matrix: alpha_j = M_0j, beta_i = M_i0 - 1.
 *  For every cell (s,t) with M_st != 0 put R(s,t) = M_{s+1,t}/M_st and C(s,t) = M_{s,t+1}/M_st
 *  (integers in [0,p), indices mod 8).  Recentring at (s,t) sends the set of nonzero cells to
 *  its translate and R'(u,w) = R(u+s,w+t), C'(u,w) = C(u+s,w+t), so the multiset
 *  W = {R(s,t)} u {C(s,t)} is the same for every recentring of M.  (Transposition
 *  alpha''_j = beta_j + 1, beta''_i = alpha_i - 1 is also a symmetry and swaps R and C, so W is
 *  invariant under it too; we do not need this.)  Let w = min W.  If w = R(s,t), recentre at
 *  (s,t); if w = C(s,t), recentre the transpose at (t,s) [R of the transpose at (t,s) equals
 *  C(s,t)].  The result N is a normalised solution with R_N(0,0) = N_10/N_00 = 1 + beta_1(N)
 *  = w = min W(N).  Hence: IF ANY SOLUTION EXISTS, ONE EXISTS WITH
 *       R(s,t) >= v and C(s,t) >= v for every cell (s,t) with M_st != 0,  v := 1 + beta_1.
 *  The search imposes a SUBSET of these inequalities (all R(s,t), and C(s,0), C(s,7), i.e.
 *  those that involve at most one alpha), each as soon as all its cells are known except
 *  one alpha, whose set S_j is then filtered.  A constraint whose denominator cell is zero
 *  is vacuous (that cell is not a legal centre) and is skipped.  Imposing constraints that
 *  some solution in every nonempty solution set satisfies cannot hide feasibility.
 *  Option -u turns all of this off (v = 0 makes every inequality vacuous).
 *
 * Every witness is re-verified on all 64 cells from the definition before it is printed.
 *
 * usage: rows p [-j threads] [-u] [-T secs] [-t] [-s seed]   (-s shuffles root order)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <pthread.h>
#include <stdatomic.h>

static int P, G, PM1;
static uint8_t *mask;       /* bit m set iff x in A_m; mask[0] = 0xFF */
static uint32_t *inv_, *lg, *ex;   /* inverse, discrete log (x != 0), exp table (size 2(p-1)) */
static uint16_t *Dl[8];     /* D_r lists (r = 1..7), increasing */
static int Dn[8], Wn[8];    /* sizes and word counts */
static int32_t *Didx[8];    /* index of b in D_r or -1 */
static uint32_t *Zlog[8][8]; /* logs of nonzero z in Z(s,t) */
static int Zn[8][8], Zzero[8][8];
static uint16_t *Al[8]; static int An[8];  /* A_{-j} lists, j = 1..7 */

static int nosym = 0, nthreads = 4;
static double tcap = 0, t0;
static atomic_int next_root;
static atomic_int found;
static atomic_int stopflag;
static atomic_ullong total_nodes, roots_done;
static uint16_t *root_order; static int nroots;
static pthread_mutex_t outmx = PTHREAD_MUTEX_INITIALIZER;

static inline int md8(int x) { return ((x % 8) + 8) % 8; }
static inline uint32_t addp(uint32_t a, uint32_t b) { uint32_t x = a + b; return x >= (uint32_t)P ? x - P : x; }
static inline uint32_t subp(uint32_t a, uint32_t b) { return a >= b ? a - b : a + P - b; }
static inline uint32_t mulp(uint32_t a, uint32_t b) { return (uint32_t)((uint64_t)a * b % (uint32_t)P); }
static inline int inA(uint32_t x, int m) { return (mask[x] >> m) & 1; }
static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }
static long long powmod(long long b, long long e, long long m) { long long r = 1; b %= m; while (e) { if (e & 1) r = r * b % m; b = b * b % m; e >>= 1; } return r; }
static int least_primroot(int p) {
    int n = p - 1, f[32], nf = 0;
    for (int q = 2; (long)q * q <= n; q++) if (n % q == 0) { f[nf++] = q; while (n % q == 0) n /= q; }
    if (n > 1) f[nf++] = n;
    for (int g = 2; g < p; g++) { int ok = 1; for (int k = 0; k < nf; k++) if (powmod(g, (p - 1) / f[k], p) == 1) { ok = 0; break; } if (ok) return g; }
    return -1;
}
/* ratio test: num/den >= v, vacuous if den == 0 */
static inline int rat_ok(uint32_t num, uint32_t den, uint32_t v) { return den == 0 || mulp(num, inv_[den]) >= v; }

static int full_check(const uint32_t *al, const uint32_t *be) {
    if (al[0] != 1 || be[0] != 0) return 0;
    for (int i = 0; i < 8; i++) for (int j = 0; j < 8; j++) if (!inA((al[j] + be[i]) % P, md8(-(i + j)))) return 0;
    return 1;
}

/* ---------------- per-thread state ---------------- */
typedef struct {
    uint32_t b[8], v;
    int nS1; uint16_t *S1val; int *S1col;   /* level-1 alpha pool: value and column */
    uint64_t *T;          /* T[(r*nS1 + pos)*WMAX] for r = 2..7 (r index used directly, 8 slots) */
    int WMAX;
    int *S[8][8]; int Sn[8][8];   /* S[level][j] = list of pool positions */
    uint64_t *cand[8];    /* candidate bitsets per level */
    uint64_t nodes;
} TS;

static void build_T(TS *ts, int r, int pos) {
    uint64_t *bs = ts->T + ((size_t)r * ts->nS1 + pos) * ts->WMAX;
    memset(bs, 0, Wn[r] * 8);
    uint32_t a = ts->S1val[pos]; int j = ts->S1col[pos];
    int m = md8(-(r + j));
    uint32_t d = subp(a, 1);
    if (d == 0) { int id = Didx[r][P - 1]; if (id >= 0) bs[id >> 6] |= 1ULL << (id & 63); return; }
    uint32_t ld = lg[d]; int e = ld % 8;
    int s = md8(-r - e), t = md8(m - e);
    if (Zzero[s][t]) { int id = Didx[r][P - 1]; if (id >= 0) bs[id >> 6] |= 1ULL << (id & 63); }
    const uint32_t *zl = Zlog[s][t]; int zn = Zn[s][t];
    for (int q = 0; q < zn; q++) {
        uint32_t y = ex[ld + zl[q]];
        uint32_t b = subp(y, 1);
        int id = Didx[r][b];
        bs[id >> 6] |= 1ULL << (id & 63);
    }
}

static void report(TS *ts, int lvl) {
    uint32_t al[8], be[8];
    al[0] = 1; be[0] = 0;
    for (int i = 1; i < 8; i++) be[i] = ts->b[i];
    for (int j = 1; j < 8; j++) al[j] = ts->S1val[ts->S[lvl][j][0]];
    if (!full_check(al, be)) { fprintf(stderr, "BUG: witness failed verification\n"); exit(3); }
    int expected = 0;
    if (atomic_compare_exchange_strong(&found, &expected, 1)) {
        pthread_mutex_lock(&outmx);
        printf("FEASIBLE k=8 p=%d g=%d beta=", P, G);
        for (int i = 0; i < 8; i++) printf("%u%s", be[i], i < 7 ? "," : "");
        printf(" alpha=");
        for (int j = 0; j < 8; j++) printf("%u%s", al[j], j < 7 ? "," : "");
        printf("\n"); fflush(stdout);
        pthread_mutex_unlock(&outmx);
    }
}

/* filter S[r-1][j] -> S[r][j] for the new row r with value b; returns 0 if some S empties */
static int filter_row(TS *ts, int r, uint32_t b) {
    uint32_t v = ts->v;
    int id = Didx[r][b];
    uint64_t wbit = 1ULL << (id & 63); int widx = id >> 6;
    uint32_t bp = ts->b[r - 1];           /* previous row value (row r-1), b_0 = 0 */
    uint32_t onepb = addp(1, b);
    /* order: process the column with the smallest set first */
    int ord[7]; for (int j = 1; j <= 7; j++) ord[j - 1] = j;
    for (int x = 1; x < 7; x++) { int y = ord[x], k = x; while (k > 0 && ts->Sn[r - 1][ord[k - 1]] > ts->Sn[r - 1][y]) { ord[k] = ord[k - 1]; k--; } ord[k] = y; }
    for (int q = 0; q < 7; q++) {
        int j = ord[q];
        int *src = ts->S[r - 1][j], n = ts->Sn[r - 1][j], k = 0;
        int *dst = ts->S[r][j];
        for (int u = 0; u < n; u++) {
            int pos = src[u];
            const uint64_t *bs = ts->T + ((size_t)r * ts->nS1 + pos) * ts->WMAX;
            if (!(bs[widx] & wbit)) continue;
            if (v) {
                uint32_t a = ts->S1val[pos];
                uint32_t cur = addp(a, b);            /* M_{r,j} */
                if (!rat_ok(cur, addp(a, bp), v)) continue;          /* R(r-1,j) */
                if (r == 7 && !rat_ok(a, cur, v)) continue;           /* R(7,j) = M_0j / M_7j */
                if (j == 1 && !rat_ok(cur, onepb, v)) continue;       /* C(r,0) = M_r1 / M_r0 */
                if (j == 7 && !rat_ok(onepb, cur, v)) continue;       /* C(r,7) = M_r0 / M_r7 */
            }
            dst[k++] = pos;
        }
        ts->Sn[r][j] = k;
        if (!k) return 0;
    }
    return 1;
}

static void rec(TS *ts, int r) {
    /* candidates for row r given S[r-1] */
    if (atomic_load_explicit(&found, memory_order_relaxed) || atomic_load_explicit(&stopflag, memory_order_relaxed)) return;
    int W = Wn[r];
    uint64_t *cand = ts->cand[r];
    uint64_t tmp[1024];
    int ord[7]; for (int j = 1; j <= 7; j++) ord[j - 1] = j;
    for (int x = 1; x < 7; x++) { int y = ord[x], k = x; while (k > 0 && ts->Sn[r - 1][ord[k - 1]] > ts->Sn[r - 1][y]) { ord[k] = ord[k - 1]; k--; } ord[k] = y; }
    for (int q = 0; q < 7; q++) {
        int j = ord[q];
        int *src = ts->S[r - 1][j], n = ts->Sn[r - 1][j];
        memset(tmp, 0, W * 8);
        for (int u = 0; u < n; u++) {
            const uint64_t *bs = ts->T + ((size_t)r * ts->nS1 + src[u]) * ts->WMAX;
            for (int w = 0; w < W; w++) tmp[w] |= bs[w];
        }
        uint64_t any = 0;
        if (q == 0) { for (int w = 0; w < W; w++) { cand[w] = tmp[w]; any |= tmp[w]; } }
        else { for (int w = 0; w < W; w++) { cand[w] &= tmp[w]; any |= cand[w]; } }
        if (!any) return;
    }
    uint32_t v = ts->v;
    uint32_t onepprev = addp(1, ts->b[r - 1]);
    for (int w = 0; w < W; w++) {
        uint64_t x = cand[w];
        while (x) {
            int bit = __builtin_ctzll(x); x &= x - 1;
            uint32_t b = Dl[r][(w << 6) | bit];
            uint32_t onepb = addp(1, b);
            if (v) {
                if (!rat_ok(onepb, onepprev, v)) continue;            /* R(r-1,0) */
                if (r == 7 && !rat_ok(1, onepb, v)) continue;         /* R(7,0) = M_00 / M_70 */
            }
            ts->b[r] = b;
            if (!filter_row(ts, r, b)) continue;
            ts->nodes++;
            if (r == 7) { report(ts, 7); return; }
            rec(ts, r + 1);
            if (atomic_load_explicit(&found, memory_order_relaxed) || atomic_load_explicit(&stopflag, memory_order_relaxed)) return;
        }
    }
}

static void *worker(void *arg) {
    TS *ts = (TS *)arg;
    int maxpool = 7 * (P / 8 + 2);
    ts->S1val = malloc(maxpool * sizeof(uint16_t)); ts->S1col = malloc(maxpool * sizeof(int));
    for (int l = 0; l < 8; l++) for (int j = 0; j < 8; j++) ts->S[l][j] = malloc((P / 8 + 2) * sizeof(int));
    ts->WMAX = 0; for (int r = 1; r < 8; r++) if (Wn[r] > ts->WMAX) ts->WMAX = Wn[r];
    for (int r = 0; r < 8; r++) ts->cand[r] = malloc(ts->WMAX * 8);
    size_t Tcap = 0; ts->T = NULL;
    for (;;) {
        if (atomic_load(&found) || atomic_load(&stopflag)) break;
        int ri = atomic_fetch_add(&next_root, 1);
        if (ri >= nroots) break;
        uint32_t b1 = root_order[ri];
        ts->b[0] = 0; ts->b[1] = b1;
        uint32_t v = nosym ? 0 : addp(b1, 1);
        ts->v = v;
        uint64_t n0 = ts->nodes;
        /* level 1: alpha pool */
        int np = 0, ok = 1;
        for (int j = 1; j <= 7 && ok; j++) {
            int m = md8(-(1 + j)), k = 0;
            for (int u = 0; u < An[j]; u++) {
                uint32_t a = Al[j][u];
                uint32_t cur = addp(a, b1);
                if (!inA(cur, m)) continue;
                if (v) {
                    if (!rat_ok(cur, a, v)) continue;                       /* R(0,j) = M_1j / M_0j */
                    if (j == 1 && a < v) continue;                          /* C(0,0) = M_01 / M_00 */
                    if (j == 7 && !rat_ok(1, a, v)) continue;               /* C(0,7) = M_00 / M_07 */
                    if (j == 1 && !rat_ok(cur, v, v)) continue;             /* C(1,0) = M_11 / M_10 */
                    if (j == 7 && !rat_ok(v, cur, v)) continue;             /* C(1,7) = M_10 / M_17 */
                }
                ts->S1val[np] = (uint16_t)a; ts->S1col[np] = j; ts->S[1][j][k++] = np; np++;
            }
            ts->Sn[1][j] = k;
            if (!k) ok = 0;
        }
        if (ok) {
            ts->nodes++;
            ts->nS1 = np;
            size_t need = (size_t)8 * np * ts->WMAX;
            if (need > Tcap) { free(ts->T); Tcap = need + need / 4; ts->T = malloc(Tcap * 8); }
            for (int r = 2; r <= 7; r++) for (int pos = 0; pos < np; pos++) build_T(ts, r, pos);
            rec(ts, 2);
        }
        atomic_fetch_add(&total_nodes, ts->nodes - n0);
        unsigned long long rd = atomic_fetch_add(&roots_done, 1) + 1;
        double el = now() - t0;
        if (tcap > 0 && el > tcap) atomic_store(&stopflag, 1);
        if (rd % 64 == 0 || rd == (unsigned long long)nroots) {
            pthread_mutex_lock(&outmx);
            fprintf(stderr, "PROGRESS p=%d roots=%llu/%d nodes=%llu secs=%.1f\n", P, rd, nroots, (unsigned long long)atomic_load(&total_nodes), el);
            pthread_mutex_unlock(&outmx);
        }
    }
    return NULL;
}

static int self_test(void) {
    /* check T_{r,a} against brute force for a sample of a */
    TS ts; memset(&ts, 0, sizeof ts);
    int np = 0; ts.S1val = malloc(7 * (P / 8 + 2) * 2); ts.S1col = malloc(7 * (P / 8 + 2) * sizeof(int));
    for (int j = 1; j <= 7; j++) for (int u = 0; u < An[j]; u += 37) { ts.S1val[np] = Al[j][u]; ts.S1col[np] = j; np++; }
    /* include a = 1 and a = 0 where legal */
    for (int j = 1; j <= 7; j++) for (int u = 0; u < An[j] && u < 2; u++) { ts.S1val[np] = Al[j][u]; ts.S1col[np] = j; np++; }
    ts.nS1 = np; ts.WMAX = 0; for (int r = 1; r < 8; r++) if (Wn[r] > ts.WMAX) ts.WMAX = Wn[r];
    ts.T = calloc((size_t)8 * np * ts.WMAX, 8);
    long bad = 0, tot = 0;
    for (int r = 2; r <= 7; r++) for (int pos = 0; pos < np; pos++) {
        build_T(&ts, r, pos);
        uint64_t *bs = ts.T + ((size_t)r * np + pos) * ts.WMAX;
        int j = ts.S1col[pos]; uint32_t a = ts.S1val[pos];
        for (int id = 0; id < Dn[r]; id++) {
            uint32_t b = Dl[r][id];
            int want = inA(addp(a, b), md8(-(r + j)));
            int got = (bs[id >> 6] >> (id & 63)) & 1;
            if (want != got) bad++;
            tot++;
        }
    }
    printf("selftest p=%d: %ld mismatches out of %ld\n", P, bad, tot);
    return bad != 0;
}

int main(int argc, char **argv) {
    if (argc < 2) return 1;
    P = atoi(argv[1]);
    int selft = 0; uint64_t seed = 0;
    for (int a = 2; a < argc; a++) {
        if (!strcmp(argv[a], "-j")) nthreads = atoi(argv[++a]);
        else if (!strcmp(argv[a], "-u")) nosym = 1;
        else if (!strcmp(argv[a], "-T")) tcap = atof(argv[++a]);
        else if (!strcmp(argv[a], "-t")) selft = 1;
        else if (!strcmp(argv[a], "-s")) seed = strtoull(argv[++a], 0, 10);
    }
    if (P % 8 != 1 || P >= 65536) { fprintf(stderr, "need p = 1 mod 8, p < 65536\n"); return 1; }
    PM1 = P - 1;
    G = least_primroot(P);
    mask = calloc(P, 1); inv_ = calloc(P, 4); lg = calloc(P, 4); ex = calloc(2 * P, 4);
    { uint64_t y = 1; for (int e = 0; e < P - 1; e++) { mask[y] = (uint8_t)(1u << (e % 8)); lg[y] = e; ex[e] = (uint32_t)y; ex[e + P - 1] = (uint32_t)y; y = y * G % P; } }
    mask[0] = 0xFF;
    for (int x = 1; x < P; x++) inv_[x] = ex[(P - 1 - lg[x]) % (P - 1)];
    for (int x = 1; x < P; x++) if (mulp(x, inv_[x]) != 1) { fprintf(stderr, "inv bug\n"); return 2; }
    for (int r = 1; r <= 7; r++) {
        Dl[r] = malloc(P * 2); Didx[r] = malloc(P * 4); Dn[r] = 0;
        for (int b = 0; b < P; b++) { Didx[r][b] = -1; if (inA(addp(1, b), md8(-r))) { Didx[r][b] = Dn[r]; Dl[r][Dn[r]++] = b; } }
        Wn[r] = (Dn[r] + 63) / 64;
        if (Wn[r] > 1024) { fprintf(stderr, "too big\n"); return 1; }
    }
    for (int j = 1; j <= 7; j++) { Al[j] = malloc(P * 2); An[j] = 0; for (int a = 0; a < P; a++) if (inA(a, md8(-j))) Al[j][An[j]++] = a; }
    for (int s = 0; s < 8; s++) for (int t = 0; t < 8; t++) {
        Zlog[s][t] = malloc(P * 4); Zn[s][t] = 0; Zzero[s][t] = 0;
        for (int z = 0; z < P; z++) if (inA(z, s) && inA(addp(z, 1), t)) { if (z == 0) Zzero[s][t] = 1; else Zlog[s][t][Zn[s][t]++] = lg[z]; }
    }
    if (selft) return self_test();
    nroots = Dn[1]; root_order = malloc(nroots * 2);
    for (int i = 0; i < nroots; i++) root_order[i] = Dl[1][i];
    if (seed) { uint64_t x = seed * 0x9E3779B97F4A7C15ULL + 1; for (int i = nroots - 1; i > 0; i--) { x ^= x << 13; x ^= x >> 7; x ^= x << 17; int k = x % (i + 1); uint16_t t = root_order[i]; root_order[i] = root_order[k]; root_order[k] = t; } }
    t0 = now();
    pthread_t th[64]; TS *tss = calloc(nthreads, sizeof(TS));
    for (int k = 0; k < nthreads; k++) pthread_create(&th[k], NULL, worker, &tss[k]);
    for (int k = 0; k < nthreads; k++) pthread_join(th[k], NULL);
    double el = now() - t0;
    unsigned long long nn = atomic_load(&total_nodes);
    if (atomic_load(&found)) fprintf(stderr, "found after nodes~%llu secs=%.1f\n", nn, el);
    else if (atomic_load(&stopflag)) printf("OPEN k=8 p=%d nodes_so_far=%llu secs=%.1f roots_done=%llu/%d%s\n", P, nn, el, (unsigned long long)atomic_load(&roots_done), nroots, nosym ? " (nosym)" : "");
    else printf("INFEASIBLE k=8 p=%d nodes=%llu secs=%.1f%s\n", P, nn, el, nosym ? " (nosym)" : "");
    fflush(stdout);
    return 0;
}
```

## (4) Soundness of each prune

The prunes matter only for INFEASIBLE claims: every FEASIBLE line stands on its own as a checked witness.

1. **Domains from row 0 and column 0.** Since beta_0 = 0 and alpha_0 = 1, those constraints read exactly alpha_j ∈ A_{-j} and 1 + beta_i ∈ A_{-i}. Nothing is lost.
2. **Rows first, empty column set means no solution.** Each constraint ties one alpha to one beta. So once all betas are fixed, the columns are independent, and S_j only shrinks as rows are added. A partial row assignment with some S_j empty has no extension. With every S_j nonempty, any pick from each S_j is a solution.
3. **Candidate generation is exact.** Writing 1 + beta = (a − 1)·z turns the cell test into a lookup in a precomputed table, with no loss. A brute-force self-test (`-t`) gave 0 mismatches over about 4.7e7 checks at p = 9473, 9697, 22921 and 43177.
4. **Symmetry.** The full proof is in the header comment.
   - Recentring at a nonzero cell maps solutions to solutions (I checked the step you suggested).
   - The multiset of all 128 ratios M_{s+1,t}/M_st and M_{s,t+1}/M_st, over nonzero denominators, is the same for the whole orbit under recentring and transposition.
   - Recentring at the smallest ratio gives a solution with 1 + beta_1 = that minimum.
   - The search imposes only a subset of the resulting inequalities and skips any with a zero denominator, so it cannot lose a whole orbit.
   - The 9473 result agrees with this prune off (`-u`) and with the second solver.

## (5) Wall time and cores

- **Hardware:** 4 cores (Intel Xeon @ 2.10 GHz), 4 threads per prime, primes run one after another, smallest first. Most primes took under 10 s.
- **The 29-prime run:** about 2 minutes wall, 05:35–05:37 (17 s for 22937, then about 107 s for the other 28).
- **Validation and cross-checks:** about 4 minutes wall with the new solver. The first solver (the 9473 cross-check and 9697) used roughly 10 core-minutes.
- **Whole session, including development:** roughly 1–1.5 hours.

Everything is in `/tmp/claude-0/-home-user-qsearch/4840ea79-7bdb-5830-bbdc-914889fdf0f7/scratchpad/e2k8/`. The 29 result lines are in `results.txt`, and the per-prime logs are `out_<p>.txt` and `err_<p>.txt`. You can paste the lines above into `research/audits/reviews/2026-11-04-rees-cloud-e2k8-hard.md` as they are.
