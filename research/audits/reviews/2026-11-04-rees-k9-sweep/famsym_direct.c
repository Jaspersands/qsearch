/* famsym_direct.c -- table-free version of ../2026-11-04-rees-threshold-5/famsym.c
 * (T1 family: alpha_j = gamma_j, beta_i = gamma_{i+b}; conditions
 *  gamma_j + gamma_k in Q_{b-(j+k)} for all j, k in Z_K).
 *
 * Differences from famsym.c, and nothing else:
 *  (1) No index table.  famsym.c's table idx[y] = log_g(y) mod K is used only through
 *      inQ(y, m) <=> y != 0 and idx[y] = m (mod K).  Since y = g^e gives
 *      y^h = (g^h)^e = zeta^(e mod K), with zeta = g^h of exact order K, this is
 *      y != 0 and y^h == zeta^m, computed here by fast exponentiation (O(log p)).
 *  (2) No coset list.  famsym.c's Qlist[m*H + t] = g^(m + K t) (t = 0..H-1, in that
 *      order) is used only to enumerate Q_m when the level-0 candidate lists are built.
 *      Here Q_m is walked directly: y = g^m, then y *= g^K.
 *  (3) Optional window W (argument "win=W"): the level-0 list for each unknown keeps only
 *      the first W candidates of the walk, which starts at a random t0 in [0, H).  With
 *      W = 0 ("exact" mode) the full coset is walked from t0 = 0, no extra random draws
 *      are made, and the program's search is step-for-step that of famsym.c (same rng
 *      stream, same lists in the same order), so FOUND/NOTFOUND lines agree except for the
 *      secs= field.  W > 0 is a sub-search of the same tree: every witness it returns is a
 *      T1 witness and is re-checked on all K^2 cells; NOTFOUND means only "not found".
 *  (4) Segmented prime sieve on [P0, P1] instead of a full sieve to P1.
 * Requires P1 < 2^32 so that a*b < 2^64 (plain 64-bit modmul).
 * Build: cc -O2 -o famsym_direct famsym_direct.c
 * Usage: ./famsym_direct K P0 P1 budget restarts seed [hodd] [complete] [win=W]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
typedef uint64_t u64; typedef uint32_t u32;
static u64 P, K, H, B, GK;
static u64 zp[64];
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
/* table-free coset test: y in Q_m  <=>  y != 0 and y^H = zeta^m */
static inline int inQ(u64 y, long m) { return y != 0 && powm(y, H) == zp[md(m)]; }
static u32 *Sbuf; static u64 cap; static long Scnt[66][64];
static inline u32 *LIST(long lev, long k) { return Sbuf + ((u64)lev * K + (u64)k) * cap; }
static int complete = 0; static u64 WIN = 0;
static int asg[64]; static u64 gam[64]; static long nodes, budget;

static int dfs(long lev, long nas) {                     /* identical to famsym.c */
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
static int check(const u64 *al, const u64 *be, u64 g) {   /* identical to famsym.c */
    u64 z = powm(g, H), zq[64]; zq[0] = 1; for (u64 e = 1; e < K; e++) zq[e] = mulm(zq[e - 1], z);
    for (u64 i = 0; i < K; i++) for (u64 j = 0; j < K; j++) { u64 v = ad(al[j], be[i]); if (!v || powm(v, H) != zq[md(-(long)(i + j))]) return 0; }
    return 1;
}
int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "usage: famsym_direct K P0 P1 budget restarts seed [hodd] [complete] [win=W]\n"); return 1; }
    K = strtoull(argv[1], 0, 10); u64 P0 = strtoull(argv[2], 0, 10), P1 = strtoull(argv[3], 0, 10);
    if (P1 >= (1ULL << 32) || K < 2 || K > 60) { fprintf(stderr, "need P1 < 2^32, 2 <= K <= 60\n"); return 1; }
    long bud = atol(argv[4]), restarts = atol(argv[5]); rng ^= strtoull(argv[6], 0, 10) * 0x9E3779B97F4A7C15ULL; if (!rng) rng = 1;
    int hodd = 0; for (int a = 7; a < argc; a++) { if (!strcmp(argv[a], "hodd")) hodd = 1; if (!strcmp(argv[a], "complete")) complete = 1; if (!strncmp(argv[a], "win=", 4)) WIN = strtoull(argv[a] + 4, 0, 10); }
    if (P0 < 3) P0 = 3;
    /* segmented sieve of [P0, P1] */
    u64 L = P1 >= P0 ? P1 - P0 + 1 : 0; char *comp = calloc(L + 1, 1);
    { u64 r = 1; while ((r + 1) * (r + 1) <= P1) r++; char *sm = calloc(r + 2, 1);
      for (u64 i = 2; i <= r; i++) if (!sm[i]) { for (u64 j = i * i; j <= r; j += i) sm[j] = 1;
          u64 st = (P0 + i - 1) / i * i; if (st < i * i) st = i * i; for (u64 j = st; j <= P1; j += i) comp[j - P0] = 1; }
      free(sm); }
    u64 Hmax = P1 / K + 2; cap = WIN ? WIN : Hmax;
    Sbuf = malloc((K + 2) * K * cap * sizeof(u32));
    long nf = 0, nn = 0;
    for (u64 p = P0; p <= P1; p++) {
        if (comp[p - P0] || (p - 1) % K) continue;
        P = p; H = (p - 1) / K;
        if (hodd && H % 2 == 0) continue;
        double t0 = now(); u64 g = primroot(p);
        { u64 z = powm(g, H); zp[0] = 1; for (u64 e = 1; e < K; e++) zp[e] = mulm(zp[e - 1], z); }
        GK = powm(g, K);
        u64 inv2 = (p + 1) / 2; int found = 0; int hitlim = 0; long tries = 0; u64 al[64], be[64];
        for (long rs = 0; rs < restarts && !found; rs++) {
            tries++; nodes = 0; budget = bud; B = complete ? (u64)rs : xr() % K;
            if (complete && rs >= (long)K) break;
            memset(asg, 0, sizeof asg);
            gam[0] = mulm(powm(g, B), inv2); asg[0] = 1;          /* Qlist[B*H] = g^B; 2 gamma_0 in Q_B */
            for (long k = 1; k < (long)K; k++) {                     /* gamma_k + gamma_0 in Q_{B-k}, 2 gamma_k in Q_{B-2k} */
                u32 *Lk = LIST(0, k); long c2 = 0; u64 cm = (u64)md((long)B - k);
                u64 tst = WIN ? xr() % H : 0;
                u64 y = powm(g, cm + K * tst);                       /* = Qlist[cm*H + tst] */
                for (u64 s = 0; s < H; s++) {
                    u64 v = sb(y, gam[0]);
                    if (v != gam[0] && inQ(ad(v, v), (long)B - 2 * k)) { Lk[c2++] = (u32)v; if (WIN && (u64)c2 >= WIN) break; }
                    y = mulm(y, GK); if (WIN && tst + s + 1 == H) y = powm(g, cm); /* wrap t = H -> 0 */
                }
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
        const char *mname = WIN ? "symw" : "sym";
        if (found == 1) { nf++; printf("FOUND k=%llu p=%llu g=%llu mode=%s tries=%ld secs=%.3f beta=", (unsigned long long)K, (unsigned long long)p, (unsigned long long)g, mname, tries, dt);
            for (u64 i = 0; i < K; i++) printf("%llu%s", (unsigned long long)be[i], i + 1 < K ? "," : "");
            printf(" alpha="); for (u64 j = 0; j < K; j++) printf("%llu%s", (unsigned long long)al[j], j + 1 < K ? "," : ""); printf("\n"); }
        else if (found == -1) { printf("BUG p=%llu\n", (unsigned long long)p); return 2; }
        else { nn++; printf("NOTFOUND k=%llu p=%llu mode=%s tries=%ld secs=%.3f %s\n", (unsigned long long)K, (unsigned long long)p, mname, tries, dt, complete ? (hitlim ? "LIMIT" : (WIN ? "WINDOW_EMPTY" : "COMPLETE_EMPTY")) : ""); }
        fflush(stdout);
    }
    printf("DONE k=%llu range=[%llu,%llu] mode=%s%s found=%ld notfound=%ld\n", (unsigned long long)K, (unsigned long long)P0, (unsigned long long)P1, WIN ? "symw" : "sym", hodd ? "(hodd)" : "", nf, nn);
    return 0;
}
