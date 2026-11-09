/* famsym.c -- randomized witness search in the symmetric (transpose, lambda = 1) family T1
 * of section 2 of the note.  Valid for every p = 1 (mod K) (no condition on h).
 *
 * Ansatz: gamma in F_p^K, b in Z_K, alpha_j = gamma_j, beta_i = gamma_{i+b}.  Then
 * cell (i,j) = gamma_j + gamma_{i+b}, and the conditions alpha_j + beta_i in Q_{-(i+j)}
 * become, with k = i + b,
 *        gamma_j + gamma_k in Q_{b-(j+k)}    for all j, k in Z_K  (j = k: 2 gamma_j),
 * i.e. K(K+1)/2 conditions on K unknowns (the symmetric form of the appendix, Phase 0,
 * after relabelling).  Scaling by Q_0 lets gamma_0 be a fixed element with
 * 2 gamma_0 in Q_b.  The search assigns gamma_0, then the unknown with the fewest
 * surviving candidates (MRV), trying values in random order, with a node budget per
 * restart and a fresh random b per restart.  Output is translated to beta_0 = 0 and
 * scaled to alpha_0 = 1, then re-checked on all K^2 cells by exponentiation.
 * Build: cc -O2 -o famsym famsym.c
 * Usage: ./famsym K P0 P1 budget restarts seed [hodd]   (hodd: only primes with h odd)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
typedef uint64_t u64; typedef uint32_t u32;
static u64 P, K, H, B;
static unsigned char *idx; static u32 *Qlist;
static u64 rng = 0x2545F4914F6CDD1DULL;
static inline u64 xr(void) { rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; }
static inline u64 mulm(u64 a, u64 b) { return a * b % P; }
static u64 powm(u64 a, u64 e) { u64 r = 1; a %= P; while (e) { if (e & 1) r = mulm(r, a); a = mulm(a, a); e >>= 1; } return r; }
static u64 primroot(u64 p) { u64 n = p - 1, f[64]; int nf = 0;
    for (u64 q = 2; q * q <= n; q++) if (n % q == 0) { f[nf++] = q; while (n % q == 0) n /= q; }
    if (n > 1) f[nf++] = n;
    for (u64 g = 2;; g++) { int ok = 1; for (int i = 0; i < nf; i++) if (powm(g, (p - 1) / f[i]) == 1) { ok = 0; break; } if (ok) return g; } }
static inline long md(long m) { m %= (long)K; if (m < 0) m += K; return m; }
static inline u64 ad(u64 a, u64 b) { u64 s = a + b; return s >= P ? s - P : s; }
static inline u64 sb(u64 a, u64 b) { return a >= b ? a - b : a + P - b; }
static inline int inQ(u64 y, long m) { return y != 0 && idx[y] == (unsigned char)md(m); }
static u32 *Sbuf; static u64 cap; static long Scnt[66][64];
static inline u32 *LIST(long lev, long k) { return Sbuf + ((u64)lev * K + (u64)k) * cap; }
static int complete = 0;
static int asg[64]; static u64 gam[64]; static long nodes, budget;

static int dfs(long lev, long nas) {
    if (nas == (long)K) return 1;
    if (++nodes > budget) return -1;
    long best = -1; long bn = 0;
    for (long k = 0; k < (long)K; k++) if (!asg[k]) { if (best < 0 || Scnt[lev][k] < bn) { best = k; bn = Scnt[lev][k]; } }
    if (bn == 0) return 0;
    u32 *L = LIST(lev, best);
    long off = (long)(xr() % (u64)bn);
    for (long t = 0; t < bn; t++) {
        u64 x = L[(off + t) % bn];
        int ok = 1;
        for (long k = 0; k < (long)K && ok; k++) {
            if (asg[k] || k == best) continue;
            u32 *Lk = LIST(lev, k), *L2 = LIST(lev + 1, k); long n = Scnt[lev][k], c2 = 0; long m = (long)B - (best + k);
            for (long s = 0; s < n; s++) if (inQ(ad(Lk[s], x), m) && Lk[s] != x) L2[c2++] = Lk[s];
            Scnt[lev + 1][k] = c2; if (!c2) ok = 0;
        }
        if (!ok) continue;
        asg[best] = 1; gam[best] = x;
        int r = dfs(lev + 1, nas + 1);
        if (r) return r;
        asg[best] = 0;
    }
    return 0;
}
static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }
static int check(const u64 *al, const u64 *be, u64 g) {
    u64 z = powm(g, H), zp[64]; zp[0] = 1; for (u64 e = 1; e < K; e++) zp[e] = mulm(zp[e - 1], z);
    for (u64 i = 0; i < K; i++) for (u64 j = 0; j < K; j++) { u64 v = ad(al[j], be[i]); if (!v || powm(v, H) != zp[md(-(long)(i + j))]) return 0; }
    return 1;
}
int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "usage: famsym K P0 P1 budget restarts seed [hodd]\n"); return 1; }
    K = strtoull(argv[1], 0, 10); u64 P0 = strtoull(argv[2], 0, 10), P1 = strtoull(argv[3], 0, 10);
    long bud = atol(argv[4]), restarts = atol(argv[5]); rng ^= strtoull(argv[6], 0, 10) * 0x9E3779B97F4A7C15ULL; if (!rng) rng = 1;
    int hodd = 0; for (int a = 7; a < argc; a++) { if (!strcmp(argv[a], "hodd")) hodd = 1; if (!strcmp(argv[a], "complete")) complete = 1; }
    char *comp = calloc(P1 + 1, 1);
    for (u64 i = 2; i * i <= P1; i++) if (!comp[i]) for (u64 j = i * i; j <= P1; j += i) comp[j] = 1;
    idx = malloc(P1 + 1); u64 Hmax = P1 / K + 2; Qlist = malloc(K * Hmax * sizeof(u32)); cap = Hmax;
    Sbuf = malloc((K + 2) * K * cap * sizeof(u32));
    long nf = 0, nn = 0;
    for (u64 p = P0 < 3 ? 3 : P0; p <= P1; p++) {
        if (comp[p] || (p - 1) % K) continue;
        P = p; H = (p - 1) / K;
        if (hodd && H % 2 == 0) continue;
        double t0 = now(); u64 g = primroot(p), x = 1; long fill[64] = {0}; idx[0] = 255;
        for (u64 e = 0; e < p - 1; e++) { long m = (long)(e % K); idx[x] = (unsigned char)m; Qlist[(u64)m * H + fill[m]++] = (u32)x; x = mulm(x, g); }
        u64 inv2 = (p + 1) / 2; int found = 0; int hitlim = 0; long tries = 0; u64 al[64], be[64];
        for (long rs = 0; rs < restarts && !found; rs++) {
            tries++; nodes = 0; budget = bud; B = complete ? (u64)rs : xr() % K;
            if (complete && rs >= (long)K) break;
            memset(asg, 0, sizeof asg);
            gam[0] = mulm(Qlist[B * H], inv2); asg[0] = 1;          /* 2 gamma_0 in Q_B */
            for (long k = 1; k < (long)K; k++) {                     /* gamma_k + gamma_0 in Q_{B-k}, 2 gamma_k in Q_{B-2k} */
                u32 *L = LIST(0, k); long c2 = 0; u64 cm = (u64)md((long)B - k);
                for (u64 t = 0; t < H; t++) { u64 y = Qlist[cm * H + t]; u64 v = sb(y, gam[0]); if (v != gam[0] && inQ(ad(v, v), (long)B - 2 * k)) L[c2++] = (u32)v; }
                Scnt[0][k] = c2;
            }
            int dr = dfs(0, 1); if (dr == -1) hitlim = 1;
            if (dr == 1) {
                for (long j = 0; j < (long)K; j++) { al[j] = gam[j]; be[j] = gam[md(j + (long)B)]; }
                u64 s = be[0];
                for (long t = 0; t < (long)K; t++) { al[t] = ad(al[t], s); be[t] = sb(be[t], s); }
                u64 sc = powm(al[0], P - 2);
                for (long t = 0; t < (long)K; t++) { al[t] = mulm(al[t], sc); be[t] = mulm(be[t], sc); }
                found = check(al, be, g) ? 1 : -1;
            }
        }
        double dt = now() - t0;
        if (found == 1) { nf++; printf("FOUND k=%llu p=%llu g=%llu mode=sym tries=%ld secs=%.3f beta=", (unsigned long long)K, (unsigned long long)p, (unsigned long long)g, tries, dt);
            for (u64 i = 0; i < K; i++) printf("%llu%s", (unsigned long long)be[i], i + 1 < K ? "," : "");
            printf(" alpha="); for (u64 j = 0; j < K; j++) printf("%llu%s", (unsigned long long)al[j], j + 1 < K ? "," : ""); printf("\n"); }
        else if (found == -1) { printf("BUG p=%llu\n", (unsigned long long)p); return 2; }
        else { nn++; printf("NOTFOUND k=%llu p=%llu mode=sym tries=%ld secs=%.3f %s\n", (unsigned long long)K, (unsigned long long)p, tries, dt, complete ? (hitlim ? "LIMIT" : "COMPLETE_EMPTY") : ""); }
        fflush(stdout);
    }
    printf("DONE k=%llu range=[%llu,%llu] mode=sym%s found=%ld notfound=%ld\n", (unsigned long long)K, (unsigned long long)P0, (unsigned long long)P1, hodd ? "(hodd)" : "", nf, nn);
    return 0;
}
