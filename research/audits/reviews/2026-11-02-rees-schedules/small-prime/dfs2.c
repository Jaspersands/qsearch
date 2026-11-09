/* Complete DFS for the universal two-level contraction (general form), in C.
 * Same search as two_level.py feasible_general: beta_0 = 0, alpha_0 = 1,
 * beta_i ranges over A_{-i} - 1, S_j = A_{-j} cap_i (A_{-(i+j)} - beta_i),
 * feasible iff some beta leaves every S_j (j >= 1) nonempty.
 * Output per prime: FEASIBLE (witness re-checked), INFEASIBLE (search
 * complete), or LIMIT (node budget exhausted; no conclusion).
 * Build: cc -O2 -o dfs2 dfs2.c      Usage: ./dfs2 k P0 P1 node_limit
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef uint64_t u64;
static u64 P, K, W;            /* prime, kappa, words per bitset */
static unsigned char *idx;     /* discrete log mod K, idx[0] = 255 */
static u64 **D;                /* doubled bitsets of A_m, 2p bits */
static u64 *S;                 /* stack: depth x K x W */
static long nodes, limit;
static u64 beta[64];

static u64 mulm(u64 a, u64 b) { return (u64)((unsigned __int128)a * b % P); }
static u64 powm(u64 a, u64 e) { u64 r = 1; a %= P; while (e) { if (e & 1) r = mulm(r, a); a = mulm(a, a); e >>= 1; } return r; }
static u64 primroot(u64 p) {
    u64 n = p - 1, f[64]; int nf = 0;
    for (u64 q = 2; q * q <= n; q++) if (n % q == 0) { f[nf++] = q; while (n % q == 0) n /= q; }
    if (n > 1) f[nf++] = n;
    for (u64 g = 2;; g++) { int ok = 1; for (int i = 0; i < nf; i++) if (powm(g, (p - 1) / f[i]) == 1) { ok = 0; break; } if (ok) return g; }
}
static int inA(u64 y, long m) { m %= (long)K; if (m < 0) m += K; return y == 0 || idx[y] == m; }

/* out = S_in & {x : x + b in A_m}; returns nonzero iff out nonempty */
static int and_rot(u64 *out, const u64 *in, long m, u64 b) {
    m %= (long)K; if (m < 0) m += K;
    const u64 *d = D[m];
    u64 any = 0;
    for (u64 w = 0; w < W; w++) {
        u64 pos = b + 64 * w, q = pos >> 6, r = pos & 63;
        u64 v = d[q] >> r;
        if (r) v |= d[q + 1] << (64 - r);
        if (w == W - 1 && (P & 63)) v &= (1ULL << (P & 63)) - 1;
        out[w] = in[w] & v;
        any |= out[w];
    }
    return any != 0;
}

static int dfs(long i) {
    if (i == (long)K) return 1;
    if (++nodes > limit) return -1;
    u64 *cur = S + (u64)i * K * W, *nxt = S + (u64)(i + 1) * K * W;
    /* candidates b with 1 + b in A_{-i}: y in A_{-i}, b = y - 1 */
    for (u64 y = 0; y < P; y++) {
        if (!inA(y, -i)) continue;
        u64 b = (y + P - 1) % P;
        int ok = 1;
        for (long j = 1; j < (long)K && ok; j++)
            ok = and_rot(nxt + j * W, cur + j * W, -(i + j), b);
        if (!ok) continue;
        beta[i] = b;
        int r = dfs(i + 1);
        if (r) return r;
    }
    return 0;
}

int main(int argc, char **argv) {
    K = strtoull(argv[1], 0, 10);
    u64 P0 = strtoull(argv[2], 0, 10), P1 = strtoull(argv[3], 0, 10);
    limit = atol(argv[4]);
    char *comp = calloc(P1 + 1, 1);
    for (u64 i = 2; i * i <= P1; i++) if (!comp[i]) for (u64 j = i * i; j <= P1; j += i) comp[j] = 1;
    idx = malloc(P1 + 1);
    u64 Wmax = (P1 >> 6) + 2;
    D = malloc(K * sizeof(u64 *));
    for (u64 m = 0; m < K; m++) D[m] = malloc((2 * Wmax + 2) * sizeof(u64));
    S = malloc((K + 1) * K * Wmax * sizeof(u64));
    long nf = 0, ni = 0, nl = 0;
    for (u64 p = (P0 < 3 ? 3 : P0); p <= P1; p++) {
        if (comp[p] || (p - 1) % K) continue;
        P = p; W = (p >> 6) + 1;
        u64 g = primroot(p), x = 1;
        idx[0] = 255;
        for (u64 e = 0; e < p - 1; e++) { idx[x] = (unsigned char)(e % K); x = mulm(x, g); }
        for (u64 m = 0; m < K; m++) {
            memset(D[m], 0, (2 * W + 2) * sizeof(u64));
            for (u64 y = 0; y < 2 * p; y++) {
                u64 yy = y % p;
                if (yy == 0 || idx[yy] == m) D[m][y >> 6] |= 1ULL << (y & 63);
            }
        }
        /* depth 1 state: S_j = A_{-j} */
        u64 *s1 = S + 1 * K * W;
        for (u64 j = 1; j < K; j++) {
            u64 m = (K - j % K) % K;
            for (u64 w = 0; w < W; w++) s1[j * W + w] = D[m][w];
            if (P & 63) s1[j * W + W - 1] &= (1ULL << (P & 63)) - 1;
        }
        nodes = 0; beta[0] = 0;
        int r = dfs(1);
        if (r == 1) {
            /* reconstruct alpha_j and re-check all K^2 conditions */
            u64 alpha[64]; alpha[0] = 1;
            for (u64 j = 1; j < K; j++) {
                alpha[j] = P;
                for (u64 xx = 0; xx < P && alpha[j] == P; xx++) {
                    int ok = inA(xx, -(long)j);
                    for (u64 i = 1; i < K && ok; i++) ok = inA((xx + beta[i]) % P, -(long)(i + j));
                    if (ok) alpha[j] = xx;
                }
                if (alpha[j] == P) { printf("BUG p=%llu\n", (unsigned long long)p); return 2; }
            }
            for (u64 i = 0; i < K; i++) for (u64 j = 0; j < K; j++)
                if (!inA((alpha[j] + beta[i]) % P, -(long)(i + j))) { printf("BUG2 p=%llu\n", (unsigned long long)p); return 2; }
            nf++;
        } else if (r == 0) { ni++; printf("INFEASIBLE k=%llu p=%llu nodes=%ld\n", (unsigned long long)K, (unsigned long long)p, nodes); }
        else { nl++; printf("LIMIT k=%llu p=%llu\n", (unsigned long long)K, (unsigned long long)p); }
        fflush(stdout);
    }
    printf("DONE k=%llu range=[%llu,%llu] feasible=%ld infeasible=%ld limit=%ld\n",
           (unsigned long long)K, (unsigned long long)P0, (unsigned long long)P1, nf, ni, nl);
    return 0;
}
