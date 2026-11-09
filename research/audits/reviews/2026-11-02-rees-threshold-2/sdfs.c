/* Sparse complete DFS for the universal two-level contraction (general form).
 *
 * Same problem and normalisation as dfs2.c (2026-11-02-rees-schedules/small-prime):
 * beta_0 = 0, alpha_0 = 1, alpha_j + beta_i in A_{-(i+j)} = Q_{-(i+j)} U {0}.
 * dfs2 keeps the candidate sets X_j as dense bitsets and tries every y in F_p
 * at every node, which costs O(p^2/64) per node and is too slow for p ~ 10^6.
 * Here X_j is a sorted list of surviving alpha_j values, a candidate beta_i is
 * accepted only if every X_j keeps an element (early exit), and the surviving
 * lists are built only for accepted candidates.  Candidates at each level are
 * tried in cyclic order from a random offset; the search is still complete
 * (every candidate is tried unless the node limit is hit).
 *
 * Output per prime: FEASIBLE (only counted; the witness is re-checked on all
 * K^2 cells), INFEASIBLE (complete search), LIMIT (node budget exhausted).
 * With argv[6] = 1 every FEASIBLE witness is printed.
 * Build: cc -O2 -o sdfs sdfs.c      Usage: ./sdfs K P0 P1 node_limit seed [print]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef uint64_t u64;
typedef uint32_t u32;
static u64 P, K;
static unsigned char *idx;          /* idx[y] = discrete log of y mod K; idx[0] = 255 */
static u32 *cos_[64];               /* elements of A_m (Q_m plus 0) */
static u64 ncos[64];
static u32 *X[64][64];              /* X[level][j] */
static u64 nX[64][64], capX[64][64];
static void ensure(long l, long j, u64 n) {
    if (capX[l][j] >= n) return;
    capX[l][j] = n + 16;
    X[l][j] = realloc(X[l][j], capX[l][j] * sizeof(u32));
    if (!X[l][j]) { fprintf(stderr, "oom\n"); exit(3); }
}
static long nodes, limit;
static u64 beta[64];
static u64 rng;
static u64 rnd(void) { rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; }

static u64 mulm(u64 a, u64 b) { return a * b % P; }   /* P < 2^32 */
static u64 powm(u64 a, u64 e) { u64 r = 1; a %= P; while (e) { if (e & 1) r = mulm(r, a); a = mulm(a, a); e >>= 1; } return r; }
static u64 primroot(u64 p) {
    u64 n = p - 1, f[64]; int nf = 0;
    for (u64 q = 2; q * q <= n; q++) if (n % q == 0) { f[nf++] = q; while (n % q == 0) n /= q; }
    if (n > 1) f[nf++] = n;
    for (u64 g = 2;; g++) { int ok = 1; for (int i = 0; i < nf; i++) if (powm(g, (p - 1) / f[i]) == 1) { ok = 0; break; } if (ok) return g; }
}
static inline long md(long m) { m %= (long)K; if (m < 0) m += K; return m; }
static inline int inA(u64 y, long m) { return y == 0 || idx[y] == (unsigned char)md(m); }

static int dfs(long i) {
    if (i == (long)K) return 1;
    if (++nodes > limit) return -1;
    long mi = md(-i);
    u64 n = ncos[mi], off = rnd() % n;
    for (u64 t = 0; t < n; t++) {
        u64 y = cos_[mi][(off + t) % n];
        u64 b = (y + P - 1) % P;            /* 1 + b = y in A_{-i} */
        int ok = 1;
        for (long j = 1; j < (long)K && ok; j++) {
            long m = md(-(i + j));
            const u32 *xs = X[i][j]; u64 nx = nX[i][j], q;
            for (q = 0; q < nx; q++) { u64 v = xs[q] + b; if (v >= P) v -= P; if (inA(v, m)) break; }
            ok = (q < nx);
        }
        if (!ok) continue;
        for (long j = 1; j < (long)K; j++) {
            long m = md(-(i + j));
            const u32 *xs = X[i][j]; u64 nx = nX[i][j], c = 0;
            ensure(i + 1, j, nx);
            u32 *out = X[i + 1][j];
            for (u64 q = 0; q < nx; q++) { u64 v = xs[q] + b; if (v >= P) v -= P; if (inA(v, m)) out[c++] = xs[q]; }
            nX[i + 1][j] = c;
        }
        beta[i] = b;
        int r = dfs(i + 1);
        if (r) return r;
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage: sdfs K P0 P1 node_limit seed [print]\n"); return 1; }
    K = strtoull(argv[1], 0, 10);
    u64 P0 = strtoull(argv[2], 0, 10), P1 = strtoull(argv[3], 0, 10);
    limit = atol(argv[4]);
    rng = strtoull(argv[5], 0, 10) * 2654435761ULL + 88172645463325252ULL;
    int print = argc > 6 ? atoi(argv[6]) : 0;
    char *comp = calloc(P1 + 1, 1);
    for (u64 i = 2; i * i <= P1; i++) if (!comp[i]) for (u64 j = i * i; j <= P1; j += i) comp[j] = 1;
    idx = malloc(P1 + 1);
    u64 hmax = P1 / K + 2;
    for (u64 m = 0; m < K; m++) cos_[m] = malloc(hmax * sizeof(u32));
    long nf = 0, ni = 0, nl = 0;
    for (u64 p = (P0 < 3 ? 3 : P0); p <= P1; p++) {
        if (comp[p] || (p - 1) % K) continue;
        P = p;
        u64 g = primroot(p), x = 1;
        idx[0] = 255;
        for (u64 e = 0; e < p - 1; e++) { idx[x] = (unsigned char)(e % K); x = mulm(x, g); }
        for (u64 m = 0; m < K; m++) ncos[m] = 0;
        for (u64 y = 1; y < p; y++) { u64 m = idx[y]; cos_[m][ncos[m]++] = (u32)y; }
        for (u64 m = 0; m < K; m++) cos_[m][ncos[m]++] = 0;   /* A_m = Q_m U {0} */
        /* level 1: X_j = A_{-j} (row 0, beta_0 = 0) */
        for (u64 j = 1; j < K; j++) {
            u64 m = md(-(long)j);
            ensure(1, j, ncos[m]);
            memcpy(X[1][j], cos_[m], ncos[m] * sizeof(u32));
            nX[1][j] = ncos[m];
        }
        nodes = 0; beta[0] = 0;
        int r = dfs(1);
        if (r == 1) {
            u64 alpha[64]; alpha[0] = 1;
            for (u64 j = 1; j < K; j++) alpha[j] = X[K][j][0];
            for (u64 i = 0; i < K; i++) for (u64 j = 0; j < K; j++)
                if (!inA((alpha[j] + beta[i]) % P, -(long)(i + j)) || (i == 0 && j == 0 && (alpha[0] + beta[0]) % P == 0)) {
                    printf("BUG k=%llu p=%llu\n", (unsigned long long)K, (unsigned long long)p); return 2;
                }
            nf++;
            if (print) {
                printf("FEASIBLE k=%llu p=%llu g=%llu nodes=%ld beta=", (unsigned long long)K, (unsigned long long)p, (unsigned long long)g, nodes);
                for (u64 i = 0; i < K; i++) printf("%llu%s", (unsigned long long)beta[i], i + 1 < K ? "," : "");
                printf(" alpha=");
                for (u64 j = 0; j < K; j++) printf("%llu%s", (unsigned long long)alpha[j], j + 1 < K ? "," : "");
                printf("\n");
            }
        } else if (r == 0) { ni++; printf("INFEASIBLE k=%llu p=%llu nodes=%ld\n", (unsigned long long)K, (unsigned long long)p, nodes); }
        else { nl++; printf("LIMIT k=%llu p=%llu\n", (unsigned long long)K, (unsigned long long)p); }
        fflush(stdout);
    }
    printf("DONE k=%llu range=[%llu,%llu] feasible=%ld infeasible=%ld limit=%ld\n",
           (unsigned long long)K, (unsigned long long)P0, (unsigned long long)P1, nf, ni, nl);
    return 0;
}
