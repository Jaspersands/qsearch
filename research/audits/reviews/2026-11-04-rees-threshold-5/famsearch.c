/* famsearch.c -- randomized witness search for STRICT two-level contractions,
 * in the full problem or in the half-shift family H (section 2 of the note).
 *
 * Problem: p prime, p = 1 (mod K), Q_m = {y != 0 : log_g(y) = m (mod K)}.
 * Find alpha, beta in F_p^K with alpha_j + beta_i in Q_{-(i+j)} for all i, j
 * (every cell nonzero).  A witness certifies p notin E_2(K) and N > 0.  The search
 * is INCOMPLETE: it never claims infeasibility; it prints FOUND (with witness) or
 * NOTFOUND.
 *
 * Modes
 *   full : beta_0 = 0, alpha_0 = 1.  Rows beta_1..beta_{K-1} are assigned in a random
 *          order; column sets S_j = {x : x + beta_i in Q_{-(i+j)}, assigned i} are kept
 *          as explicit lists.  Row candidates b come from the coset list of column 0
 *          (1 + b in Q_{-r}), scanned cyclically from a random offset.
 *   half : K even, -1 in Q_0 (h = (p-1)/K even).  Ansatz alpha_{j+m} = -alpha_j,
 *          beta_{i+m} = -beta_i, m = K/2.  With a_j = alpha_j, b_i = beta_i (i,j < m):
 *              a_j + b_i in Q_{-(i+j)}  and  a_j - b_i in Q_{m-(i+j)}.
 *          (The other two quadrants follow since -1 in Q_0.)  Normalisation
 *          a_0 + b_0 = 1; b_0 random.  Output translated to beta_0 = 0, alpha_0 = 1.
 * Each restart has a node budget.  Every witness is re-checked on all K^2 cells by an
 * independent coset test (y^h compared with powers of g^h, no table) before printing.
 *
 * Build: cc -O2 -o famsearch famsearch.c
 * Usage: ./famsearch K P0 P1 full|half|auto budget restarts seed
 *   auto = half when K even and h even, else full.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

typedef uint64_t u64;
typedef uint32_t u32;
static u64 P, K, H;
static unsigned char *idx;
static u32 *Qlist;               /* Qlist[m*H + t], t < H: the elements of Q_m */
static u64 rng = 88172645463325252ULL;
static inline u64 xr(void) { rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; }
static inline u64 mulm(u64 a, u64 b) { return a * b % P; }
static u64 powm(u64 a, u64 e) { u64 r = 1; a %= P; while (e) { if (e & 1) r = mulm(r, a); a = mulm(a, a); e >>= 1; } return r; }
static u64 primroot(u64 p) {
    u64 n = p - 1, f[64]; int nf = 0;
    for (u64 q = 2; q * q <= n; q++) if (n % q == 0) { f[nf++] = q; while (n % q == 0) n /= q; }
    if (n > 1) f[nf++] = n;
    for (u64 g = 2;; g++) { int ok = 1; for (int i = 0; i < nf; i++) if (powm(g, (p - 1) / f[i]) == 1) { ok = 0; break; } if (ok) return g; }
}
static inline long md(long m) { m %= (long)K; if (m < 0) m += K; return m; }
static inline u64 ad(u64 a, u64 b) { u64 s = a + b; return s >= P ? s - P : s; }
static inline u64 sb(u64 a, u64 b) { return a >= b ? a - b : a + P - b; }
static inline int inQ(u64 y, long m) { return y != 0 && idx[y] == (unsigned char)md(m); }

static int half;
static long R, C, M;             /* number of row variables, columns, K/2 */
static long rowid[64];           /* row index of the k-th row variable */
static u64 col0;                 /* alpha_0 (full) or a_0 (half) */
static u64 rowv[64];
static u32 *Sbuf; static u64 cap;
static long Scnt[66][64];
static long nodes, budget;
static long ord[64];
static u64 half_b0;

static inline int ok_cell(u64 x, u64 b, long i, long j) {
    if (!inQ(ad(x, b), -(i + j))) return 0;
    if (half && !inQ(sb(x, b), M - (i + j))) return 0;
    return 1;
}
static inline u32 *LIST(long lev, long j) { return Sbuf + ((u64)lev * C + (u64)j) * cap; }

static int viable(long lev, long r, u64 b) {
    for (long j = 1; j < C; j++) {
        u32 *L = LIST(lev, j); long n = Scnt[lev][j], q;
        for (q = 0; q < n; q++) if (ok_cell(L[q], b, r, j)) break;
        if (q == n) return 0;
    }
    return 1;
}

/* lev = number of row variables assigned so far beyond the initial ones; rows ord[k] */
static int dfs(long lev, long k) {
    if (k == R) return 1;
    if (++nodes > budget) return -1;
    long r = rowid[ord[k]];
    long cm = md(-r);                      /* column-0 cell (r,0): col0 + b in Q_{-r} */
    u64 off = xr() % H;
    for (u64 t = 0; t < H; t++) {
        u64 y = Qlist[(u64)cm * H + (off + t) % H];
        u64 b = sb(y, col0);
        if (half && (b == 0 || !inQ(sb(col0, b), M - r))) continue;
        if (half && (b == half_b0 || ad(b, half_b0) == 0)) continue;
        int dup = 0;
        for (long s = 0; s < k; s++) { u64 v = rowv[ord[s]]; if (v == b || (half && ad(v, b) == 0)) { dup = 1; break; } }
        if (dup) continue;
        if (!viable(lev, r, b)) continue;
        for (long j = 1; j < C; j++) {
            u32 *L = LIST(lev, j), *L2 = LIST(lev + 1, j); long n = Scnt[lev][j], c2 = 0;
            for (long s = 0; s < n; s++) if (ok_cell(L[s], b, r, j)) L2[c2++] = L[s];
            Scnt[lev + 1][j] = c2;
        }
        rowv[ord[k]] = b;
        int res = dfs(lev + 1, k + 1);
        if (res) return res;
    }
    return 0;
}

static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }

static int check(const u64 *alpha, const u64 *beta, u64 g) {
    u64 z = powm(g, H), zp[64]; zp[0] = 1;
    for (u64 e = 1; e < K; e++) zp[e] = mulm(zp[e - 1], z);
    for (u64 i = 0; i < K; i++) for (u64 j = 0; j < K; j++) {
        u64 v = ad(alpha[j], beta[i]);
        if (v == 0) return 0;
        if (powm(v, H) != zp[md(-(long)(i + j))]) return 0;
    }
    return 1;
}

int main(int argc, char **argv) {
    if (argc < 8) { fprintf(stderr, "usage: famsearch K P0 P1 full|half|auto budget restarts seed\n"); return 1; }
    K = strtoull(argv[1], 0, 10);
    u64 P0 = strtoull(argv[2], 0, 10), P1 = strtoull(argv[3], 0, 10);
    const char *mode = argv[4];
    long bud = atol(argv[5]), restarts = atol(argv[6]);
    rng ^= strtoull(argv[7], 0, 10) * 0x9E3779B97F4A7C15ULL; if (!rng) rng = 1;
    if (K < 2 || K > 40 || P1 >= (1ULL << 32)) { fprintf(stderr, "bad args\n"); return 1; }
    char *comp = calloc(P1 + 1, 1);
    for (u64 i = 2; i * i <= P1; i++) if (!comp[i]) for (u64 j = i * i; j <= P1; j += i) comp[j] = 1;
    idx = malloc(P1 + 1);
    u64 Hmax = P1 / K + 2;
    Qlist = malloc(K * Hmax * sizeof(u32));
    cap = Hmax;
    Sbuf = malloc((K + 2) * K * cap * sizeof(u32));
    if (!idx || !Qlist || !Sbuf) { fprintf(stderr, "out of memory\n"); return 1; }
    long nfound = 0, nnot = 0;
    for (u64 p = P0 < 3 ? 3 : P0; p <= P1; p++) {
        if (comp[p] || (p - 1) % K) continue;
        P = p; H = (p - 1) / K;
        int want_half = !strcmp(mode, "half") || (!strcmp(mode, "auto") && K % 2 == 0 && H % 2 == 0);
        if (want_half && (K % 2 || H % 2)) { printf("SKIP k=%llu p=%llu\n", (unsigned long long)K, (unsigned long long)p); continue; }
        half = want_half; M = (long)K / 2;
        double t0 = now();
        u64 g = primroot(p), x = 1;
        long fill[64] = {0};
        idx[0] = 255;
        for (u64 e = 0; e < p - 1; e++) { long m = (long)(e % K); idx[x] = (unsigned char)m; Qlist[(u64)m * H + fill[m]++] = (u32)x; x = mulm(x, g); }
        int found = 0; long tries = 0;
        u64 alpha[64], beta[64];
        for (long rs = 0; rs < restarts && !found; rs++) {
            tries++; nodes = 0; budget = bud;
            if (!half) {
                R = (long)K - 1; C = (long)K; col0 = 1;
                for (long s = 0; s < R; s++) { rowid[s] = s + 1; ord[s] = s; }
                for (long s = R - 1; s > 0; s--) { long w = (long)(xr() % (u64)(s + 1)); long t = ord[s]; ord[s] = ord[w]; ord[w] = t; }
                for (long j = 1; j < C; j++) {            /* row 0 (beta_0 = 0): x in Q_{-j} */
                    u32 *L = LIST(0, j); u64 cm = (u64)md(-j);
                    memcpy(L, Qlist + cm * H, H * sizeof(u32)); Scnt[0][j] = (long)H;
                }
                if (dfs(0, 0) == 1) {
                    beta[0] = 0; alpha[0] = 1;
                    for (long s = 0; s < R; s++) beta[rowid[s]] = rowv[s];
                    for (long j = 1; j < C; j++) alpha[j] = LIST(R, j)[0];
                    found = check(alpha, beta, g) ? 1 : -1;
                }
            } else {
                R = M - 1; C = M;                         /* row variables b_1..b_{m-1}; b_0 fixed first */
                u64 b0, a0; long guard = 0;
                do { b0 = xr() % P; a0 = sb(1, b0); guard++; }
                while ((b0 == 0 || a0 == 0 || !inQ(sb(a0, b0), M)) && guard < 100000000);
                col0 = a0; half_b0 = b0;
                for (long s = 0; s < R; s++) { rowid[s] = s + 1; ord[s] = s; }
                for (long s = R - 1; s > 0; s--) { long w = (long)(xr() % (u64)(s + 1)); long t = ord[s]; ord[s] = ord[w]; ord[w] = t; }
                for (long j = 1; j < C; j++) {            /* row 0: a_j + b_0 in Q_{-j}, a_j - b_0 in Q_{m-j} */
                    u32 *L = LIST(0, j); long c2 = 0; u64 cm = (u64)md(-j);
                    for (u64 t = 0; t < H; t++) { u64 y = Qlist[cm * H + t]; u64 aj = sb(y, b0); if (inQ(sb(aj, b0), M - j)) L[c2++] = (u32)aj; }
                    Scnt[0][j] = c2;
                }
                if (dfs(0, 0) == 1) {
                    u64 a[64], b[64];
                    a[0] = a0; b[0] = b0;
                    for (long j = 1; j < C; j++) a[j] = LIST(R, j)[0];
                    for (long s = 0; s < R; s++) b[rowid[s]] = rowv[s];
                    u64 al[64], be[64];
                    for (long j = 0; j < M; j++) { al[j] = a[j]; al[j + M] = sb(0, a[j]); }
                    for (long i = 0; i < M; i++) { be[i] = b[i]; be[i + M] = sb(0, b[i]); }
                    for (long t = 0; t < (long)K; t++) { alpha[t] = ad(al[t], b0); beta[t] = sb(be[t], b0); }
                    found = check(alpha, beta, g) ? 1 : -1;
                }
            }
        }
        double dt = now() - t0;
        if (found == 1) {
            nfound++;
            printf("FOUND k=%llu p=%llu g=%llu mode=%s tries=%ld secs=%.3f beta=", (unsigned long long)K, (unsigned long long)p,
                   (unsigned long long)g, half ? "half" : "full", tries, dt);
            for (u64 i = 0; i < K; i++) printf("%llu%s", (unsigned long long)beta[i], i + 1 < K ? "," : "");
            printf(" alpha=");
            for (u64 j = 0; j < K; j++) printf("%llu%s", (unsigned long long)alpha[j], j + 1 < K ? "," : "");
            printf("\n");
        } else if (found == -1) {
            printf("BUG k=%llu p=%llu witness failed check\n", (unsigned long long)K, (unsigned long long)p); return 2;
        } else { nnot++; printf("NOTFOUND k=%llu p=%llu mode=%s tries=%ld secs=%.3f\n", (unsigned long long)K, (unsigned long long)p, half ? "half" : "full", tries, dt); }
        fflush(stdout);
    }
    printf("DONE k=%llu range=[%llu,%llu] mode=%s found=%ld notfound=%ld\n", (unsigned long long)K, (unsigned long long)P0, (unsigned long long)P1, mode, nfound, nnot);
    return 0;
}
