/* Independent exact decision of p in E_2(kappa): C port of e2dfs.py
 * (threshold-8 checker, 2026-11-05). Same algorithm as e2dfs.py, no code shared with
 * dfs2b, rcdfs.c or the threshold-8 folder.
 *
 * Normal form beta_0 = 0, alpha_0 = 1; beta_i in Qc[-i] - 1; column sets
 * C_j = {x in Qc[-j] : x + beta_i in Qc[-(i+j)] for assigned i}. DFS over rows with
 * forward checking: domain of an unassigned row i = base n /\_j (Qc[-(i+j)] - C_j),
 * smallest domain first, empty domain prunes, empty C_j prunes. Leaf: all C_j nonempty
 * -> FEASIBLE (alpha_j = least element of C_j). Witness re-checked with modpow.
 * T[m][x] = Qc[m] - x is precomputed (kappa * p bitsets of p bits).
 *
 * usage: e2dfs_c kappa pmin pmax          output one line per prime p = 1 mod kappa
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef uint64_t u64;
static int P, K, H, W;
static u64 *T;              /* T[(m*P + x)*W .. ] */
static int *IND;
static long long NODES;
#define TB(m, x) (T + ((size_t)(m) * P + (x)) * W)

static long long mpow(long long b, long long e, long long m) {
    long long r = 1; b %= m;
    while (e) { if (e & 1) r = r * b % m; b = b * b % m; e >>= 1; }
    return r;
}
static int is_prime(int n) { if (n < 2) return 0; for (int d = 2; (long)d * d <= n; d++) if (n % d == 0) return 0; return 1; }
static int coset_gen(int p, int k, int start, int dir) {
    int h = (p - 1) / k;
    for (int x = start; x > 1 && x < p; x += dir) {
        long long z = mpow(x, h, p); int ok = 1;
        for (int q = 2; q <= k; q++) if (k % q == 0 && is_prime(q) && mpow(z, k / q, p) == 1) { ok = 0; break; }
        if (ok) return x;
    }
    return -1;
}
static int popc(const u64 *a) { int c = 0; for (int w = 0; w < W; w++) c += __builtin_popcountll(a[w]); return c; }
static int nonempty(const u64 *a) { for (int w = 0; w < W; w++) if (a[w]) return 1; return 0; }
static int inter_nonempty(const u64 *a, const u64 *b) { for (int w = 0; w < W; w++) if (a[w] & b[w]) return 1; return 0; }
static int mod(int a, int m) { a %= m; return a < 0 ? a + m : a; }

/* per-depth storage */
static u64 *Cst;   /* [depth][j][W], depth 0..K-1 */
static u64 *Dst;   /* [depth][i][W] */
static int *assigned; static int *beta;
#define CS(d, j) (Cst + ((size_t)(d) * K + (j)) * W)
#define DS(d, i) (Dst + ((size_t)(d) * K + (i)) * W)
static u64 *tmpU;

static void domain(int d, int i, const u64 *base, u64 *out) {
    /* out = {b in base : for all j>=1, C_j n (Qc[-(i+j)] - b) != 0} */
    long tot = 0; int nb = popc(base);
    for (int j = 1; j < K; j++) tot += popc(CS(d, j));
    if (tot <= (long)nb * (K - 1)) {
        memcpy(out, base, W * 8);
        for (int j = 1; j < K; j++) {
            int m = mod(-(i + j), K);
            memset(tmpU, 0, W * 8);
            const u64 *c = CS(d, j);
            for (int w = 0; w < W; w++) { u64 v = c[w]; while (v) { int x = w * 64 + __builtin_ctzll(v); v &= v - 1;
                const u64 *t = TB(m, x); for (int u = 0; u < W; u++) tmpU[u] |= t[u]; } }
            int any = 0;
            for (int u = 0; u < W; u++) { out[u] &= tmpU[u]; any |= out[u] != 0; }
            if (!any) return;
        }
        return;
    }
    memset(out, 0, W * 8);
    for (int w = 0; w < W; w++) { u64 v = base[w]; while (v) { int b = w * 64 + __builtin_ctzll(v); v &= v - 1;
        int ok = 1;
        for (int j = 1; j < K && ok; j++) if (!inter_nonempty(CS(d, j), TB(mod(-(i + j), K), b))) ok = 0;
        if (ok) out[w] |= 1ULL << (b & 63); } }
}

static int rec(int d) {   /* d = number of assigned rows i >= 1 */
    NODES++;
    if (d == K - 1) return 1;
    int best = -1, bestc = 1 << 30;
    for (int i = 1; i < K; i++) if (!assigned[i]) {
        u64 *o = DS(d + 1, i);
        domain(d, i, DS(d, i), o);
        int c = popc(o);
        if (c == 0) return 0;
        if (c < bestc) { bestc = c; best = i; }
    }
    int i = best;
    assigned[i] = 1;
    u64 *dom = DS(d + 1, i);
    for (int w = 0; w < W; w++) { u64 v = dom[w]; while (v) { int b = w * 64 + __builtin_ctzll(v); v &= v - 1;
        int ok = 1;
        for (int j = 1; j < K; j++) {
            const u64 *c = CS(d, j), *t = TB(mod(-(i + j), K), b); u64 *o = CS(d + 1, j); int any = 0;
            for (int u = 0; u < W; u++) { o[u] = c[u] & t[u]; any |= o[u] != 0; }
            if (!any) { ok = 0; break; }
        }
        if (!ok) continue;
        /* domains of other unassigned rows at depth d+1 are recomputed from DS(d+1,.) in rec(d+1):
           copy the filtered domains down one level so rec(d+1) reads DS(d+1, r) as base */
        beta[i] = b;
        if (rec(d + 1)) return 1;
    } }
    assigned[i] = 0;
    return 0;
}

int main(int argc, char **argv) {
    K = atoi(argv[1]); int pmin = atoi(argv[2]), pmax = atoi(argv[3]);
    for (int p = pmin; p <= pmax; p++) {
        if (p % K != 1 || !is_prime(p)) continue;
        P = p; H = (p - 1) / K; W = (p + 63) / 64;
        int xi = coset_gen(p, K, 2, 1);
        long long zeta = mpow(xi, H, p);
        long long zp[64]; long long z = 1; for (int e = 0; e < K; e++) { zp[e] = z; z = z * zeta % p; }
        IND = malloc(sizeof(int) * p);
        for (int x = 1; x < p; x++) { long long y = mpow(x, H, p); int e; for (e = 0; e < K; e++) if (zp[e] == y) break; IND[x] = e; }
        u64 *Qc = calloc((size_t)K * W, 8);
        for (int m = 0; m < K; m++) Qc[(size_t)m * W] |= 1ULL;
        for (int x = 1; x < p; x++) Qc[(size_t)IND[x] * W + x / 64] |= 1ULL << (x % 64);
        T = calloc((size_t)K * p * W, 8);
        if (!T) { fprintf(stderr, "oom\n"); return 1; }
        for (int m = 0; m < K; m++) {
            memcpy(TB(m, 0), Qc + (size_t)m * W, W * 8);
            for (int x = 1; x < p; x++) {   /* T[m][x] = T[m][x-1] - 1: out bit y = in bit y+1 mod p */
                const u64 *a = TB(m, x - 1); u64 *t = TB(m, x);
                for (int w = 0; w < W; w++) t[w] = (a[w] >> 1) | (w + 1 < W ? a[w + 1] << 63 : 0);
                int top = p - 1; t[top / 64] &= ~(1ULL << (top % 64));
                if (a[0] & 1ULL) t[top / 64] |= 1ULL << (top % 64);
            }
        }
        /* spot check of the table against the definition */
        for (int m = 0; m < K; m += 3) for (int x = 0; x < p; x += 97) for (int y = 0; y < p; y += 7) {
            int s = (y + x) % p; int in = (Qc[(size_t)m * W + s / 64] >> (s % 64)) & 1;
            int got = (TB(m, x)[y / 64] >> (y % 64)) & 1;
            if (in != got) { fprintf(stderr, "table error\n"); return 3; }
        }
        Cst = calloc((size_t)K * K * W, 8); Dst = calloc((size_t)(K + 1) * K * W, 8);
        tmpU = calloc(W, 8); assigned = calloc(K, sizeof(int)); beta = calloc(K, sizeof(int));
        for (int j = 1; j < K; j++) memcpy(CS(0, j), Qc + (size_t)mod(-j, K) * W, W * 8);
        for (int i = 1; i < K; i++) memcpy(DS(0, i), TB(mod(-i, K), 1), W * 8);   /* Qc[-i] - 1 */
        /* rec(d) reads base domains DS(d, i); after choosing row i at depth d it writes
           the filtered domains into DS(d+1, .), which are the bases at depth d+1. */
        NODES = 0;
        int f = rec(0);
        if (!f) printf("k=%d p=%d INFEASIBLE nodes=%lld\n", K, p, NODES);
        else {
            int alpha[64]; alpha[0] = 1; beta[0] = 0;
            for (int j = 1; j < K; j++) { const u64 *c = CS(K - 1, j); int w = 0; while (!c[w]) w++; alpha[j] = w * 64 + __builtin_ctzll(c[w]); }
            /* re-check every cell with modpow, generator xi */
            int ok = (alpha[0] + beta[0]) % p != 0;
            for (int i = 0; i < K && ok; i++) for (int j = 0; j < K && ok; j++) {
                long long c = ((long long)alpha[j] + beta[i]) % p;
                if (c && mpow(c, H, p) != zp[mod(-(i + j), K)]) ok = 0;
            }
            if (!ok) { printf("k=%d p=%d WITNESS_CHECK_FAILED\n", K, p); return 2; }
            printf("k=%d p=%d FEASIBLE nodes=%lld xi=%d alpha=", K, p, NODES, xi);
            for (int j = 0; j < K; j++) printf("%d%c", alpha[j], j + 1 < K ? ',' : ' ');
            printf("beta="); for (int i = 0; i < K; i++) printf("%d%c", beta[i], i + 1 < K ? ',' : ' ');
            printf("powcheck=OK\n");
        }
        fflush(stdout);
        free(IND); free(Qc); free(T); free(Cst); free(Dst); free(tmpU); free(assigned); free(beta);
    }
    return 0;
}
