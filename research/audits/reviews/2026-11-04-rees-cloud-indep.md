# Rees cloud harvest: indep

- Session: `session_01B1JoCjwms3zJNWmwiJDVJW` (claude.ai/code cloud session; AI-only, pending human review)
- Started: 2026-11-04 04:47 UTC; final message: 2026-11-04 06:59 UTC (last event 2026-11-05 01:23)
- Asked: Independent implementation, written from the definition only, re-deciding 9769 and 9473 (κ=8) and 17623 (κ=9), which the paper otherwise rests on single dfs2b runs.
- Harvested 2026-11-05 from the session event stream; nothing in the session was committed or pushed.

## Cross-check against local results (2026-11-05)

- Verdict claims parsed (verdict lines plus verdicts stated in prose or as whole ranges): 6.
- Complete FEASIBLE/FOUND witnesses re-verified locally with `wcheck.py` (least primitive root, all κ² cells by the power test): 0 distinct primes, 0 bad.
- The witness for p=9697 printed in the final message (its own convention, alpha=(1,5305,...), beta=(0,237,...)) passes `wcheck.py`; it is the transpose-shift of the dfs2b witness.
- Against `k8dec.txt` / `k9dec.txt`: 6 agree, 0 conflict, 0 not in the local decided files.

## Extracted verdict lines

Regex over the whole event stream (tool outputs and messages), deduplicated to one line per (verdict, κ, p); where a line appeared several times the longest copy is kept, and `</event>` debris was stripped. Lines cut short in the transcript are kept as found.

```
(none: this session printed no dfs2b-format verdict lines; its verdicts are in the final message below)
```

## Final result message (verbatim)

My independent solver agrees with the reported verdicts on all three targets: **9769 and 9473 are in E_2(8), and 17623 is in E_2(9)**. Every validation case also matched. Nothing was committed or pushed.

## (1) Solver source

I wrote this from the definition in the brief only. I did not look at or reuse any solver in the repository.

Build with `gcc -O2 -march=native -fopenmp -o e2ind e2ind.c`. Usage: `./e2ind K p [g]`, or `./e2ind scan K maxp` to list E_2(K) ∩ primes < maxp.

```c
/*
 * e2ind.c -- independent exact solver for the "universal two-level
 * contraction" problem, written from the definition only.
 *
 * DEFINITION.  K >= 2, p prime, p = 1 (mod K), g a primitive root mod p.
 *   Q_m = { y in F_p^* : log_g y = m (mod K) },  A_m = Q_m u {0}.
 *   Question: do alpha, beta in F_p^K exist with alpha_0 = 1, beta_0 = 0 and
 *       alpha_j + beta_i in A_{-(i+j) mod K}   for all i, j in Z_K ?
 *   FEASIBLE  <=> p not in E_2(K);  INFEASIBLE <=> p in E_2(K).
 *
 * REFORMULATION (exact, no loss).
 *   Cell (0,0): 1 + 0 = 1 in A_0 always holds (log 1 = 0).
 *   Row i = 0 (beta_0 = 0):  alpha_j in A_{-j}            for j >= 1.
 *   Col j = 0 (alpha_0 = 1): beta_i in A_{-i} - 1          for i >= 1.
 *   Cells i, j >= 1:         alpha_j + beta_i in A_{-(i+j)}.
 *   So the free variables are beta_1..beta_{K-1} with static domains
 *   D_i = A_{-i} - 1, and alpha_1..alpha_{K-1}.  There are NO constraints
 *   between two alphas.  Hence, once beta_1..beta_d are fixed, the set of
 *   values of alpha_j consistent with every constraint that involves only
 *   fixed betas is exactly
 *       S_j(d) = A_{-j}  n  ∩_{i=1..d} ( A_{-(i+j)} - beta_i ),
 *   and the instance is feasible iff there is a choice of all betas
 *   (beta_i in D_i) with S_j(K-1) nonempty for every j >= 1 (then take
 *   alpha_j = any element of S_j(K-1); the alphas are independent).
 *
 * SEARCH.  Depth-first over beta_1, beta_2, ..., beta_{K-1} in that fixed
 *   order.  The state at depth d is the list S_j(d) for each j >= 1.
 *
 * PRUNE 1 (forward checking; the only prune).  At a node of depth d the
 *   candidate values for beta_{d+1} = b are restricted to
 *       V = D_{d+1} n ∩_{j>=1} U_j,   U_j = { b : exists x in S_j(d) with
 *                                             x + b in A_{-(d+1+j)} }.
 *   Soundness: if b is not in U_j then S_j(d+1) = {x in S_j(d) :
 *   x + b in A_{-(d+1+j)}} is empty, and since S_j only shrinks as further
 *   betas are fixed (it is an intersection), S_j(K-1) is empty for every
 *   completion, so no solution extends (beta_1..beta_d, b).  If b is not in
 *   D_{d+1} the column-0 constraint fails.  Every b in V is explored.  So the
 *   search is exhaustive: it reports INFEASIBLE only if every assignment
 *   of all betas in their domains leaves some S_j empty, which by the
 *   reformulation means no (alpha, beta) exists.
 *   Implementation detail (not a prune): U_j is computed either as a bitset
 *   (OR of shifted copies of the indicator of A_m) or, once V is small, by
 *   testing each surviving b against S_j directly.  Both compute the same
 *   set exactly; which one is used only changes speed.
 *
 * PARALLELISM.  The values of beta_1 in V (depth 0) are distributed over
 *   OpenMP threads; each subtree is searched completely and independently.
 *   This partitions the search space, so it changes nothing logically.
 *
 * NO symmetry reductions are used.
 *
 * WITNESS CHECK.  Every FEASIBLE answer is re-checked on all K^2 cells by
 *   a separate routine that does NOT use the discrete-log table: it tests
 *   y in A_m via y == 0 or y^((p-1)/K) == g^(m(p-1)/K) (mod p) with modpow.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <omp.h>

typedef uint64_t u64;
typedef uint32_t u32;

static int K, P, G, W, LW;
static uint16_t *msk;      /* msk[t]: bit m set iff t in A_m (t=0: all bits) */
static u64 *PS;            /* PS[(m*64+s)*LW + w] = bits [64w+s, 64w+s+63] of
                              the doubled indicator Dbl_m(t) = [t mod p in A_m] */
static u64 *Dset;          /* Dset[i*W+w]: indicator of D_i = A_{-i} - 1 */
static int CAP;            /* max list length */
static volatile int found = 0;
static int sol_alpha[32], sol_beta[32];
static long long top_done = 0;
static int top_total = 0;
static double t0;
static int verbose = 1;

static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }
static inline int md(int a, int n) { a %= n; return a < 0 ? a + n : a; }
static inline int MIDX(int i, int j) { return md(-(i + j), K); }

static u64 powmod(u64 b, u64 e, u64 m) { u64 r = 1; b %= m; while (e) { if (e & 1) r = r * b % m; b = b * b % m; e >>= 1; } return r; }
static int isprime(int n) { if (n < 2) return 0; for (int d = 2; (long)d * d <= n; d++) if (n % d == 0) return 0; return 1; }
static int is_primroot(int g, int p) {
    int n = p - 1;
    for (int q = 2; q <= n; q++) if (n % q == 0 && isprime(q)) { if (powmod(g, (p - 1) / q, p) == 1) return 0; }
    return 1;
}
static int primroot(int p) { for (int g = 2; g < p; g++) if (is_primroot(g, p)) return g; return 1; /* p=2 */ }

typedef struct {
    u32 *lst;          /* lst[(d*K + j)*CAP + k] */
    int *len;          /* len[d*K + j] */
    u64 *V, *tmp;      /* per-depth bitset, scratch */
    u32 *cand;         /* per-depth candidate lists */
    long long nodes[32];
    long long bitops, sparse;
    int beta[32];
} WS;

static WS *ws_new(void) {
    WS *w = calloc(1, sizeof(WS));
    w->lst = malloc(sizeof(u32) * (size_t)K * K * CAP);
    w->len = calloc((size_t)K * K, sizeof(int));
    w->V = aligned_alloc(64, sizeof(u64) * ((size_t)K * W + 8));
    w->tmp = aligned_alloc(64, sizeof(u64) * ((size_t)W + 8));
    w->cand = malloc(sizeof(u32) * (size_t)K * (P + 1));
    return w;
}
static void ws_free(WS *w) { free(w->lst); free(w->len); free(w->V); free(w->tmp); free(w->cand); free(w); }

#define L(w, d, j) ((w)->lst + ((size_t)(d) * K + (j)) * CAP)
#define LEN(w, d, j) ((w)->len[(d) * K + (j)])

/* Compute the candidate list for beta_i (i = d+1) at depth d, i.e. the set
 * V of PRUNE 1, exactly.  Returns number of candidates written to out. */
static int candidates(WS *w, int d, u32 *out) {
    int i = d + 1;
    int ord[32], n = 0;
    for (int j = 1; j < K; j++) ord[n++] = j;
    for (int a = 1; a < n; a++) { int v = ord[a], b = a - 1; while (b >= 0 && LEN(w, d, ord[b]) > LEN(w, d, v)) { ord[b + 1] = ord[b]; b--; } ord[b + 1] = v; }
    u64 *V = w->V + (size_t)d * W, *tmp = w->tmp;
    memcpy(V, Dset + (size_t)i * W, sizeof(u64) * W);
    int t = 0, pop = P;
    for (; t < n; t++) {
        int j = ord[t];
        if (t >= 1 && pop < W) break;           /* switch to direct testing */
        int m = MIDX(i, j);
        const u32 *S = L(w, d, j); int ls = LEN(w, d, j);
        memset(tmp, 0, sizeof(u64) * W);
        for (int a = 0; a < ls; a++) {
            u32 x = S[a];
            const u64 *src = PS + ((size_t)m * 64 + (x & 63)) * LW + (x >> 6);
            for (int k = 0; k < W; k++) tmp[k] |= src[k];  /* bit b <-> x+b in A_m */
        }
        w->bitops += (long long)ls * W;
        pop = 0;
        for (int k = 0; k < W; k++) { V[k] &= tmp[k]; pop += __builtin_popcountll(V[k]); }
        if (pop == 0) return 0;
    }
    int nc = 0;
    for (int k = 0; k < W; k++) { u64 v = V[k]; while (v) { int b = __builtin_ctzll(v); v &= v - 1; out[nc++] = (u32)(k * 64 + b); } }
    if (t == n) return nc;
    /* direct test of remaining j's */
    int r = 0;
    for (int c = 0; c < nc; c++) {
        u32 b = out[c]; int ok = 1;
        for (int tt = t; tt < n && ok; tt++) {
            int j = ord[tt]; uint16_t bit = (uint16_t)(1u << MIDX(i, j));
            const u32 *S = L(w, d, j); int ls = LEN(w, d, j), hit = 0;
            for (int a = 0; a < ls; a++) { u32 s = S[a] + b; if (s >= (u32)P) s -= P; if (msk[s] & bit) { hit = 1; break; } }
            w->sparse++;
            ok = hit;
        }
        if (ok) out[r++] = b;
    }
    return r;
}

/* Build S_j(d+1) from S_j(d) given beta_{d+1} = b.  Returns 0 if some list is
 * empty (cannot happen for b from candidates(); kept as a safety check). */
static int child(WS *w, int d, u32 b) {
    int i = d + 1;
    for (int j = 1; j < K; j++) {
        uint16_t bit = (uint16_t)(1u << MIDX(i, j));
        const u32 *S = L(w, d, j); int ls = LEN(w, d, j);
        u32 *T = L(w, i, j); int lt = 0;
        for (int a = 0; a < ls; a++) { u32 s = S[a] + b; if (s >= (u32)P) s -= P; if (msk[s] & bit) T[lt++] = S[a]; }
        LEN(w, i, j) = lt;
        if (!lt) return 0;
    }
    return 1;
}

static int search(WS *w, int d) {
    if (found) return 0;
    if (d == K - 1) {
        #pragma omp critical
        {
            if (!found) {
                sol_alpha[0] = 1; sol_beta[0] = 0;
                for (int j = 1; j < K; j++) sol_alpha[j] = (int)L(w, d, j)[0];
                for (int i = 1; i < K; i++) sol_beta[i] = w->beta[i];
                found = 1;
            }
        }
        return 1;
    }
    u32 *cand = w->cand + (size_t)d * (P + 1);
    int nc = candidates(w, d, cand);
    for (int c = 0; c < nc; c++) {
        u32 b = cand[c];
        if (!child(w, d, b)) { fprintf(stderr, "internal error: FC candidate died\n"); exit(2); }
        w->beta[d + 1] = (int)b;
        w->nodes[d + 1]++;
        if (search(w, d + 1)) return 1;
        if (found) return 0;
    }
    return 0;
}

/* Independent witness check: no log table; character via modpow. */
static int in_A(long y, int m) {
    y = md((int)(y % P), P);
    if (y == 0) return 1;
    u64 e = (u64)(P - 1) / K;
    return powmod((u64)y, e, P) == powmod((u64)G, (u64)m * e, P);
}
static int verify(const int *al, const int *be) {
    if (al[0] != 1 || be[0] != 0) return 0;
    for (int i = 0; i < K; i++) for (int j = 0; j < K; j++)
        if (!in_A((long)al[j] + be[i], md(-(i + j), K))) return 0;
    return 1;
}

static void setup(int k, int p, int g) {
    K = k; P = p; G = g;
    W = (P + 63) / 64;
    LW = W + (P >> 6) + 4;
    CAP = P + 1;
    msk = malloc(sizeof(uint16_t) * P);
    int *lg = malloc(sizeof(int) * P);
    for (int t = 0; t < P; t++) lg[t] = -1;
    u64 y = 1;
    for (int e = 0; e < P - 1; e++) { if (lg[y] != -1) { fprintf(stderr, "g not primitive\n"); exit(1); } lg[y] = e; y = y * G % P; }
    msk[0] = 0xFFFF;
    for (int t = 1; t < P; t++) msk[t] = (uint16_t)(1u << (lg[t] % K));
    free(lg);
    /* doubled indicator, pre-shifted by s = 0..63 */
    int nbits = 64 * (LW + 1);
    PS = aligned_alloc(64, sizeof(u64) * (size_t)K * 64 * LW);
    u64 *Dbl = calloc(LW + 2, sizeof(u64));
    for (int m = 0; m < K; m++) {
        memset(Dbl, 0, sizeof(u64) * (LW + 2));
        for (int t = 0; t < nbits; t++) if (msk[t % P] & (1u << m)) Dbl[t >> 6] |= 1ULL << (t & 63);
        for (int s = 0; s < 64; s++) {
            u64 *o = PS + ((size_t)m * 64 + s) * LW;
            for (int w = 0; w < LW; w++) o[w] = s ? (Dbl[w] >> s) | (Dbl[w + 1] << (64 - s)) : Dbl[w];
        }
    }
    free(Dbl);
    Dset = calloc((size_t)K * W, sizeof(u64));
    for (int i = 1; i < K; i++) {
        uint16_t bit = (uint16_t)(1u << md(-i, K));
        for (int b = 0; b < P; b++) if (msk[(b + 1) % P] & bit) Dset[(size_t)i * W + (b >> 6)] |= 1ULL << (b & 63);
    }
}
static void teardown(void) { free(msk); free(PS); free(Dset); }

/* returns 1 feasible, 0 infeasible; fills node count and time */
static int solve(int k, int p, int g, long long *nodes_out, long long *perdepth, double *secs) {
    setup(k, p, g);
    found = 0; top_done = 0;
    double ts = now(); t0 = ts;
    WS *w0 = ws_new();
    for (int j = 1; j < K; j++) {
        uint16_t bit = (uint16_t)(1u << md(-j, K)); int l = 0; u32 *S = L(w0, 0, j);
        for (int y = 0; y < P; y++) if (msk[y] & bit) S[l++] = y;
        LEN(w0, 0, j) = l;
    }
    long long tot[32] = {0};
    int res;
    {
        u32 *top = malloc(sizeof(u32) * (P + 1));
        int nt = candidates(w0, 0, top);
        top_total = nt;
        tot[0] = 1;
        #pragma omp parallel
        {
            WS *w = ws_new();
            memcpy(w->lst, w0->lst, sizeof(u32) * (size_t)K * CAP);
            memcpy(w->len, w0->len, sizeof(int) * K);
            double last = now();
            #pragma omp for schedule(dynamic, 1)
            for (int c = 0; c < nt; c++) {
                if (found) continue;
                u32 b = top[c];
                if (!child(w, 0, b)) { fprintf(stderr, "internal error top\n"); exit(2); }
                w->beta[1] = (int)b; w->nodes[1]++;
                search(w, 1);
                long long dn;
                #pragma omp atomic capture
                dn = ++top_done;
                if (verbose && omp_get_thread_num() == 0 && now() - last > 60) {
                    last = now();
                    fprintf(stderr, "[K=%d p=%d] progress %lld/%d top values, %.0f s\n", K, P, dn, nt, now() - ts);
                }
            }
            #pragma omp critical
            { for (int d = 0; d < 32; d++) tot[d] += w->nodes[d]; }
            ws_free(w);
        }
        free(top);
        res = found;
    }
    *secs = now() - ts;
    long long s = 0; for (int d = 0; d < 32; d++) { s += tot[d]; if (perdepth) perdepth[d] = tot[d]; }
    *nodes_out = s;
    ws_free(w0);
    return res;
}

static void report(int k, int p, int g) {
    long long nodes, pd[32]; double secs;
    int r = solve(k, p, g, &nodes, pd, &secs);
    printf("K=%d p=%d g=%d : %s  nodes=%lld  secs=%.2f  threads=%d\n", k, p, g, r ? "FEASIBLE (p NOT in E_2)" : "INFEASIBLE (p IN E_2)", nodes, secs, omp_get_max_threads());
    printf("  nodes per depth:"); for (int d = 0; d < k; d++) printf(" %lld", pd[d]); printf("\n");
    if (r) {
        int ok = verify(sol_alpha, sol_beta);
        printf("  alpha ="); for (int j = 0; j < k; j++) printf(" %d", sol_alpha[j]); printf("\n");
        printf("  beta  ="); for (int i = 0; i < k; i++) printf(" %d", sol_beta[i]); printf("\n");
        printf("  witness re-check on all %d cells (modpow character): %s\n", k * k, ok ? "PASS" : "FAIL");
        if (!ok) exit(3);
    }
    fflush(stdout);
    teardown();
}

int main(int argc, char **argv) {
    if (argc >= 3 && !strcmp(argv[1], "scan")) {
        /* scan K maxp : print E_2(K) n primes < maxp */
        int k = atoi(argv[2]), mx = atoi(argv[3]);
        verbose = 0;
        printf("E_2(%d) n primes < %d = {", k, mx); int first = 1;
        for (int p = 2; p < mx; p++) if (isprime(p) && p % k == 1) {
            long long nodes; double secs; int g = primroot(p);
            int r = solve(k, p, g, &nodes, NULL, &secs);
            if (r && !verify(sol_alpha, sol_beta)) { printf("\nWITNESS FAIL p=%d\n", p); exit(3); }
            if (!r) { printf("%s%d", first ? "" : ", ", p); first = 0; }
            teardown();
        }
        printf("}\n");
        return 0;
    }
    if (argc < 3) { fprintf(stderr, "usage: %s K p [g] | scan K maxp\n", argv[0]); return 1; }
    int k = atoi(argv[1]), p = atoi(argv[2]);
    if (!isprime(p) || p % k != 1 || k < 2 || k > 15) { fprintf(stderr, "need prime p = 1 mod K, 2<=K<=15\n"); return 1; }
    int g = argc > 3 ? atoi(argv[3]) : primroot(p);
    if (!is_primroot(g, p)) { fprintf(stderr, "g=%d not a primitive root mod %d\n", g, p); return 1; }
    report(k, p, g);
    return 0;
}
```

## (2) Results

All runs used 4 OpenMP threads, the smallest primitive root g, and no symmetry reductions. Times are wall-clock seconds. A node is one partial assignment (beta_1..beta_d) that survived forward checking, counting the root as 1.

| Case | Verdict | Nodes | Seconds | Nodes per depth d = 0..K-1 |
|---|---|---|---|---|
| K=4 scan, p < 200 | {5, 13, 17, 29, 37, 53} ✅ | — | <1 | — |
| K=5 scan, p < 400 | {11, 31, 41, 61, 71, 101, 131, 151, 181} ✅ | — | <1 | — |
| K=8, p=9697 (g=10) | **FEASIBLE** ✅ | 24,511,357 | 18.7 | 1 28 32642 20958898 3511284 8481 22 1 |
| K=8, p=6073 (g=10) | **INFEASIBLE** ✅ | 73,092,055 | 29.4 | 1 760 577347 71366766 1145999 1182 0 0 |
| K=9, p=6067 (g=2) | **INFEASIBLE** ✅ | 6,407,153 | 3.4 | 1 675 454450 5935133 16874 20 0 0 0 |
| **K=8, p=9769** (g=13) | **INFEASIBLE**, so 9769 is in E_2(8) | 1,076,959,024 | 738.9 | 1 1222 1493283 929681974 145583969 198399 176 0 |
| **K=8, p=9473** (g=3) | **INFEASIBLE**, so 9473 is in E_2(8) | 935,954,837 | 584.2 | 1 1185 1404224 812448644 121852538 247366 879 0 |
| **K=9, p=17623** (g=3) | **INFEASIBLE**, so 17623 is in E_2(9) | 4,551,060,165 | 6189.5 | 1 1959 3837680 4286831157 260353618 35741 9 0 0 |

- **Witness for p=9697, K=8:**
  - alpha = (1, 5305, 3119, 3938, 1417, 5810, 7996, 7177)
  - beta = (0, 237, 6887, 5668, 8279, 8042, 1392, 2611)
  - It passes the check on all 64 cells. That check tests y^((p-1)/K) = g^(m(p-1)/K) with modpow and does not use the log table. The scans also checked a witness for every feasible prime, and none failed.
- **Brute-force cross-check:** I also wrote a naive Python search straight from the definition (`brute.py`), with no pruning. It agrees with the solver on K=3 for p < 60 (empty set), K=4 for p < 110, and K=5 for p < 45.
- **Node counts:** mine are about 14×, 14× and 12.6× the reported pruned counts (7.8e7, 6.6e7, 3.6e8). That fits the expected ~10× for a search without symmetry pruning. The two programs may also count nodes differently, so only the order of magnitude is comparable.

## (3) Disagreements

None. All validation cases match, and all three targets come out INFEASIBLE, as reported. One limit: I ran each prime with one primitive root only, so I did not test the claim that the answer does not depend on g.

## (4) Why each prune is sound

1. **Reformulation (exact).** Row 0 forces alpha_j ∈ A_{−j}, and column 0 forces beta_i ∈ D_i = A_{−i} − 1. Cell (0,0) always holds. No constraint links two alphas, so once all betas are fixed the instance is feasible exactly when every S_j(K−1) is nonempty. Here S_j(d) = A_{−j} ∩ ⋂_{i≤d} (A_{−(i+j)} − beta_i) is precisely the set of values of alpha_j that satisfy every fixed row.
2. **Forward checking (the only prune).** A value b for beta_{d+1} is skipped only when either:
   - b ∉ D_{d+1}, which breaks the column-0 constraint; or
   - some j has no x ∈ S_j(d) with x + b ∈ A_{−(d+1+j)}. Then S_j(d+1) is empty, and since S_j can only shrink as more betas are fixed, every completion fails.

   Every other value of b is explored, so an INFEASIBLE answer means no (alpha, beta) exists.
3. **Two ways to compute the candidate set.** Switching between the bitset union and direct per-candidate testing computes the same set exactly; it only changes speed. A runtime check aborts if any explored child ever has an empty S_j, and it never fired.
4. **Parallel split over beta_1.** This partitions the search space and is logically neutral.
5. **No symmetry reductions** are used.

The files (`e2ind.c`, `brute.py`, and `targets.out` with the raw output) are in /tmp/claude-0/-home-user-qsearch/fe126f0f-30e5-56bf-a958-735e0eb2fa1d/scratchpad/e2ind.
