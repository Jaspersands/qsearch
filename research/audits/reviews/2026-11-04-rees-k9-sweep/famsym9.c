/* famsym9.c -- ../2026-11-04-rees-t1-sweep-hi/famsym_direct.c with two additions for the
 * kappa = 9 sweep.  famsym_direct.c itself is generic in K (2 <= K <= 60; no K = 8 is
 * hard-coded) and is copied unchanged next to this file.
 *
 * T1 family (default, fam=T1): alpha_j = gamma_j, beta_i = gamma_{i+b}; conditions
 *   gamma_j + gamma_k in Q_{b-(j+k)} for all j, k in Z_K (j = k included).  STRICT.
 *
 * Changes relative to famsym_direct.c, and nothing else:
 *  (5) Montgomery arithmetic and batching in the coset test only.  inQ(y, m) is still
 *      "y != 0 and y^H == zeta^m"; y^H is computed in Montgomery form (R = 2^32,
 *      needs p < 2^31), and up to NB = 8 independent tests are evaluated together.
 *      Montgomery form is a bijection x -> xR mod p, so comparing the Montgomery forms
 *      of y^H and zeta^m is the same test.  Every loop that used inQ (level-0 list
 *      build, DFS filter) still visits the same elements in the same order and appends
 *      the hits in the same order, and the window break happens at the same element, so
 *      the lists, the rng stream and therefore the whole search are unchanged: exact
 *      mode is still step-for-step famsym.c.  The final K^2 check() is famsym.c's, with
 *      plain (non-Montgomery) powm.
 *  (6) Option fam=P: the Paley transpose family P of 2026-11-04-rees-threshold-5.md,
 *      Theorem 2.4 (lambda = -1, s = 0), which needs -1 in Q_0; for K odd this holds for
 *      every p (h is even since p - 1 = K h is even).  Ansatz M_ij = alpha_j - alpha_{i+b},
 *      b in {1..K-1} (b = 0 would make cell (0,0) zero); conditions
 *          alpha_j - alpha_k in Q_{b-(j+k)}  for j != k
 *      (symmetric in j, k because -1 in Q_0).  The K cells with j = i + b are ZERO, so a
 *      P witness is a NON-STRICT two-level contraction: it shows p notin E_2(K), not the
 *      strict N > 0.  Normalisation: translation gives alpha_0 = 0, and Q_0-scaling gives
 *      alpha_1 = g^((b-1) mod K) (any fixed element of Q_{b-1}); so with "complete" (all
 *      b = 1..K-1, branch on every candidate) the search decides whether P is empty.
 *      Output: beta_i = -alpha_{i+b}, translated to beta_0 = 0 and scaled to alpha_0 = 1
 *      (alpha_0 - alpha_b in Q_0), re-checked on all K^2 cells by checkP(): every
 *      nonzero cell in the right coset, cell (0,0) nonzero, zero cells counted (zeros=).
 *      Requires K odd (so that -1 in Q_0); the program refuses fam=P for K even.
 *  (7) Option ints=N (T1 only, needs 4N < p): a different sub-search of T1.  The unknowns
 *      gamma_j are restricted to residues of integers n with |n| <= N, and gamma_0 is not
 *      normalised: each restart draws gamma_0 = a random integer in [-N, N] \ {0} and sets
 *      b := ind(2 gamma_0), which is allowed because b ranges over all of Z_K.  For
 *      integers 0 < |n| <= 2N < p the coset index ind(n) = log_g(n) mod K is read from a
 *      table built per prime by a smallest-prime-factor sieve: ind(q) is computed for each
 *      prime q <= 2N from q^H (= zeta^ind(q)), ind is additive over factorisations, and
 *      ind(-n) = ind(-1) + ind(n) with ind(-1) also computed from (p-1)^H.  Sums of two
 *      list elements are integers with |n| <= 2N < p/2, so the residue determines n and
 *      inQ(y, m) = (y != 0 and ind(n) == m) is the same predicate as before; any y outside
 *      the table range falls back to the Montgomery test.  The level-0 list of gamma_k is
 *      { v in [-N, N] : v != gamma_0, v + gamma_0 in Q_{b-k}, 2v in Q_{b-2k} }.  The DFS
 *      and the final strict check() are unchanged, so every witness is a T1 witness
 *      re-checked on all K^2 cells by exponentiation; NOTFOUND means only "not found".
 *  (8) Option tab: famsym.c's full index table idx[y] = log_g(y) mod K (one byte per
 *      residue, built per prime by walking the powers of g, O(p)), and inQ(y, m) =
 *      (y != 0 and idx[y] == m).  Same predicate as (5); it is just faster when p is
 *      small (used for p <= 3.2e6).  With tab and without win=/ints= the T1 search is
 *      famsym.c's (same lists, same rng, same table).
 * Build: cc -O2 -o famsym9 famsym9.c
 * Usage: ./famsym9 K P0 P1 budget restarts seed [hodd] [complete] [win=W] [fam=T1|fam=P] [ints=N] [tab]
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

/* ---- (5) Montgomery coset test, R = 2^32, p < 2^31 ---- */
static u32 MPN;            /* -p^{-1} mod 2^32 */
static u64 MR2, MONE;      /* R^2 mod p, R mod p */
static u64 zpm[64];        /* Montgomery form of zeta^m */
static int HB;             /* top bit of H */
static inline u64 redc(u64 T) { u32 m = (u32)T * MPN; u64 t = (T + (u64)m * P) >> 32; return t >= P ? t - P : t; }
static inline u64 mm(u64 a, u64 b) { return redc(a * b); }
static void mont_setup(void) {
    u32 p32 = (u32)P, inv = p32;                       /* Newton: inv = p^{-1} mod 2^32 */
    for (int i = 0; i < 5; i++) inv *= 2 - p32 * inv;
    MPN = (u32)(0u - inv);
    MONE = ((u64)1 << 32) % P; MR2 = MONE * MONE % P;
    for (u64 e = 0; e < K; e++) zpm[e] = mm(zp[e], MR2);
    HB = 63; while (HB > 0 && !((H >> HB) & 1)) HB--;
}
#define NB 8
/* ok[l] = (y[l] != 0 && y[l]^H == zeta^m[l]) for l < n; m[l] already reduced mod K */
static void inQ_mont(const u64 *y, const long *m, int n, int *ok) {
    u64 r[NB], b[NB];
    for (int l = 0; l < n; l++) { b[l] = mm(y[l], MR2); r[l] = MONE; }
    for (int bit = HB; bit >= 0; bit--) {
        for (int l = 0; l < n; l++) r[l] = mm(r[l], r[l]);
        if ((H >> bit) & 1) for (int l = 0; l < n; l++) r[l] = mm(r[l], b[l]);
    }
    for (int l = 0; l < n; l++) ok[l] = y[l] != 0 && r[l] == zpm[m[l]];
}

/* ---- (7) small-integer index table ---- */
static long INTN = 0;            /* N; 0 = off */
static unsigned char *itab;      /* itab[n] = ind(n) mod K for 1 <= n <= 2N */
static u32 *spf;                 /* smallest prime factor, n <= 2N */
static long indm1;               /* ind(-1) */
static long ind_of_res(u64 y) {  /* -1 if y = 0 or y not the residue of an integer 0<|n|<=2N */
    u64 T = 2 * (u64)INTN;
    if (y == 0) return -1;
    if (y <= T) return itab[y];
    if (y >= P - T) return md(indm1 + itab[P - y]);
    return -2;
}
static u32 *plist_small; static long nplist;   /* primes <= 2N (fixed for the run) */
static void index_batch(const u64 *y, int n, long *e) {   /* e[l] = ind(y[l]); y[l] != 0 */
    u64 b[NB], r[NB];
    for (int l = 0; l < n; l++) { b[l] = mm(y[l], MR2); r[l] = MONE; }
    for (int bit = HB; bit >= 0; bit--) { for (int l = 0; l < n; l++) r[l] = mm(r[l], r[l]); if ((H >> bit) & 1) for (int l = 0; l < n; l++) r[l] = mm(r[l], b[l]); }
    for (int l = 0; l < n; l++) { e[l] = -1; for (u64 m = 0; m < K; m++) if (r[l] == zpm[m]) { e[l] = (long)m; break; }
        if (e[l] < 0) { fprintf(stderr, "index failure at y=%llu p=%llu\n", (unsigned long long)y[l], (unsigned long long)P); exit(3); } }
}
static void itab_build(void) {   /* per prime: pass 1 primes q <= 2N by exponentiation, pass 2 composites */
    u64 T = 2 * (u64)INTN; u64 y[NB]; long e[NB];
    for (long s0 = 0; s0 < nplist; s0 += NB) {
        int nb = (int)((nplist - s0) < NB ? (nplist - s0) : NB);
        for (int l = 0; l < nb; l++) y[l] = plist_small[s0 + l];
        index_batch(y, nb, e);
        for (int l = 0; l < nb; l++) itab[plist_small[s0 + l]] = (unsigned char)e[l];
    }
    itab[1] = 0;
    for (u64 n = 4; n <= T; n++) if (spf[n] != n) itab[n] = (unsigned char)md((long)itab[spf[n]] + (long)itab[n / spf[n]]);
    y[0] = P - 1; index_batch(y, 1, e); indm1 = e[0];
}
static void ints_setup(void) {   /* once per run: spf sieve and prime list up to 2N */
    u64 T = 2 * (u64)INTN;
    spf = calloc(T + 1, sizeof(u32)); itab = malloc(T + 1); plist_small = malloc((T + 1) * sizeof(u32)); nplist = 0;
    for (u64 n = 2; n <= T; n++) if (!spf[n]) { for (u64 j = n; j <= T; j += n) if (!spf[j]) spf[j] = (u32)n; plist_small[nplist++] = (u32)n; }
}
static unsigned char *idx = 0; static int TAB = 0;
static void inQ_batch(const u64 *y, const long *m, int n, int *ok) {
    if (TAB) { for (int l = 0; l < n; l++) ok[l] = y[l] != 0 && idx[y[l]] == (unsigned char)m[l]; return; }
    if (!INTN) { inQ_mont(y, m, n, ok); return; }
    for (int l = 0; l < n; l++) { long e = ind_of_res(y[l]);
        if (e == -2) inQ_mont(y + l, m + l, 1, ok + l); else ok[l] = (e >= 0 && e == m[l]); }
}
static u32 *Sbuf; static u64 cap; static long Scnt[66][64];
static inline u32 *LIST(long lev, long k) { return Sbuf + ((u64)lev * K + (u64)k) * cap; }
static int complete = 0; static u64 WIN = 0; static int famP = 0;
static int asg[64]; static u64 gam[64]; static long nodes, budget;

/* filter Lk (n entries) against x: keep s with (Lk[s] +/- x) in Q_m and Lk[s] != x, in order */
static long filt(const u32 *Lk, long n, u64 x, long m, u32 *L2) {
    long c2 = 0; u64 y[NB]; long mv[NB]; int ok[NB]; long mr = md(m);
    for (int l = 0; l < NB; l++) mv[l] = mr;
    for (long s0 = 0; s0 < n; s0 += NB) {
        int nb = (int)((n - s0) < NB ? (n - s0) : NB);
        for (int l = 0; l < nb; l++) y[l] = famP ? sb(Lk[s0 + l], x) : ad(Lk[s0 + l], x);
        inQ_batch(y, mv, nb, ok);
        for (int l = 0; l < nb; l++) if (ok[l] && Lk[s0 + l] != x) L2[c2++] = Lk[s0 + l];
    }
    return c2;
}

static int dfs(long lev, long nas) {                     /* famsym.c's, filter batched */
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
            long c2 = filt(LIST(lev, k), Scnt[lev][k], x, (long)B - (best + k), LIST(lev + 1, k));
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
static int check(const u64 *al, const u64 *be, u64 g) {   /* identical to famsym.c (strict) */
    u64 z = powm(g, H), zq[64]; zq[0] = 1; for (u64 e = 1; e < K; e++) zq[e] = mulm(zq[e - 1], z);
    for (u64 i = 0; i < K; i++) for (u64 j = 0; j < K; j++) { u64 v = ad(al[j], be[i]); if (!v || powm(v, H) != zq[md(-(long)(i + j))]) return 0; }
    return 1;
}
static int checkP(const u64 *al, const u64 *be, u64 g, int *nz) {  /* non-strict: zeros allowed off (0,0) */
    u64 z = powm(g, H), zq[64]; zq[0] = 1; for (u64 e = 1; e < K; e++) zq[e] = mulm(zq[e - 1], z);
    *nz = 0;
    for (u64 i = 0; i < K; i++) for (u64 j = 0; j < K; j++) { u64 v = ad(al[j], be[i]);
        if (!v) { if (i == 0 && j == 0) return 0; (*nz)++; continue; }
        if (powm(v, H) != zq[md(-(long)(i + j))]) return 0; }
    return 1;
}
int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "usage: famsym9 K P0 P1 budget restarts seed [hodd] [complete] [win=W] [fam=T1|fam=P]\n"); return 1; }
    K = strtoull(argv[1], 0, 10); u64 P0 = strtoull(argv[2], 0, 10), P1 = strtoull(argv[3], 0, 10);
    if (P1 >= (1ULL << 31) || K < 3 || K > 60) { fprintf(stderr, "need P1 < 2^31, 3 <= K <= 60\n"); return 1; }
    long bud = atol(argv[4]), restarts = atol(argv[5]); rng ^= strtoull(argv[6], 0, 10) * 0x9E3779B97F4A7C15ULL; if (!rng) rng = 1;
    int hodd = 0; for (int a = 7; a < argc; a++) { if (!strcmp(argv[a], "hodd")) hodd = 1; if (!strcmp(argv[a], "complete")) complete = 1; if (!strncmp(argv[a], "win=", 4)) WIN = strtoull(argv[a] + 4, 0, 10);
        if (!strcmp(argv[a], "fam=P")) famP = 1; if (!strncmp(argv[a], "ints=", 5)) INTN = atol(argv[a] + 5); if (!strcmp(argv[a], "tab")) TAB = 1; }
    if (TAB && INTN) { fprintf(stderr, "tab and ints= are exclusive\n"); return 1; }
    if (TAB) { idx = malloc(P1 + 1); if (!idx) { fprintf(stderr, "out of memory\n"); return 1; } }
    if (INTN && (famP || WIN || complete || (u64)(4 * INTN) >= P0)) { fprintf(stderr, "ints=N: T1 random mode only, no win=, and 4N < P0\n"); return 1; }
    if (INTN) ints_setup();
    if (famP && K % 2 == 0) { fprintf(stderr, "fam=P implemented for K odd only (-1 in Q_0 for every p)\n"); return 1; }
    if (P0 < 3) P0 = 3;
    /* segmented sieve of [P0, P1] */
    u64 L = P1 >= P0 ? P1 - P0 + 1 : 0; char *comp = calloc(L + 1, 1);
    { u64 r = 1; while ((r + 1) * (r + 1) <= P1) r++; char *sm = calloc(r + 2, 1);
      for (u64 i = 2; i <= r; i++) if (!sm[i]) { for (u64 j = i * i; j <= r; j += i) sm[j] = 1;
          u64 st = (P0 + i - 1) / i * i; if (st < i * i) st = i * i; for (u64 j = st; j <= P1; j += i) comp[j - P0] = 1; }
      free(sm); }
    u64 Hmax = P1 / K + 2; cap = WIN ? WIN : (INTN ? (u64)(2 * INTN / 27 + 1024) : Hmax);
    Sbuf = malloc((K + 2) * K * cap * sizeof(u32));
    long nf = 0, nn = 0;
    const char *mname = famP ? (WIN ? "Pw" : "P") : (INTN ? "symi" : (WIN ? "symw" : "sym"));
    for (u64 p = P0; p <= P1; p++) {
        if (comp[p - P0] || (p - 1) % K) continue;
        P = p; H = (p - 1) / K;
        if (hodd && H % 2 == 0) continue;
        double t0 = now(); u64 g = primroot(p);
        { u64 z = powm(g, H); zp[0] = 1; for (u64 e = 1; e < K; e++) zp[e] = mulm(zp[e - 1], z); }
        mont_setup();
        if (INTN) itab_build();
        if (TAB) { u64 x = 1; idx[0] = 255; for (u64 e = 0; e < p - 1; e++) { idx[x] = (unsigned char)(e % K); x = mulm(x, g); } }
        GK = powm(g, K);
        u64 inv2 = (p + 1) / 2; int found = 0; int hitlim = 0; long tries = 0; u64 al[64], be[64]; int nzero = 0;
        long nrs = famP ? (long)K - 1 : (long)K;               /* number of b values */
        for (long rs = 0; rs < restarts && !found; rs++) {
            tries++; nodes = 0; budget = bud;
            long v0 = 0;
            if (INTN) { do { v0 = (long)(xr() % (u64)(2 * INTN + 1)) - INTN; } while (v0 == 0);
                        B = (u64)ind_of_res(v0 > 0 ? (u64)(2 * v0) : P - (u64)(-2 * v0)); }
            else if (!famP) B = complete ? (u64)rs : xr() % K;
            else B = complete ? (u64)rs + 1 : 1 + xr() % (K - 1);
            if (complete && rs >= nrs) break;
            memset(asg, 0, sizeof asg);
            long kfirst;
            if (INTN) { gam[0] = v0 > 0 ? (u64)v0 : P - (u64)(-v0); asg[0] = 1; kfirst = 1; }   /* 2 gamma_0 in Q_B by choice of B */
            else if (!famP) { gam[0] = mulm(powm(g, B), inv2); asg[0] = 1; kfirst = 1; }   /* 2 gamma_0 in Q_B */
            else { gam[0] = 0; gam[1] = powm(g, (u64)md((long)B - 1)); asg[0] = asg[1] = 1; kfirst = 2; } /* alpha_0 = 0, alpha_1 in Q_{b-1} */
            if (INTN) {   /* one pass over v in [-N, N]: v + gamma_0 in Q_{B-k} decides k, then test 2v in Q_{B-2k} */
                for (long k = 1; k < (long)K; k++) Scnt[0][k] = 0;
                for (long v = -INTN; v <= INTN; v++) {
                    if (v == 0 || v == v0 || v + v0 == 0) continue;
                    long sv = v + v0; long f = sv > 0 ? itab[sv] : md(indm1 + itab[-sv]);
                    long k = md((long)B - f); if (k == 0) continue;
                    long e2 = v > 0 ? itab[2 * v] : md(indm1 + itab[-2 * v]);
                    if (e2 != md((long)B - 2 * k)) continue;
                    if ((u64)Scnt[0][k] < cap) LIST(0, k)[Scnt[0][k]++] = (u32)(v > 0 ? (u64)v : P - (u64)(-v));
                }
            }
            else for (long k = kfirst; k < (long)K; k++) {
                /* T1: gamma_k = y - gamma_0 with y in Q_{B-k}; keep if 2 gamma_k in Q_{B-2k} and gamma_k != gamma_0.
                 * P : alpha_k = y in Q_{B-k} (alpha_0 = 0);  keep if y - alpha_1 in Q_{B-1-k}.            */
                u32 *Lk = LIST(0, k); long c2 = 0; u64 cm = (u64)md((long)B - k);
                long mtest = famP ? md((long)B - 1 - k) : md((long)B - 2 * k);
                u64 tst = WIN ? xr() % H : 0;
                u64 y = powm(g, cm + K * tst);                       /* = Qlist[cm*H + tst] */
                u64 vb[NB], tb[NB]; long mv[NB]; int okb[NB]; for (int l = 0; l < NB; l++) mv[l] = mtest;
                int stop = 0;
                for (u64 s0 = 0; s0 < H && !stop; s0 += NB) {
                    int nb = (int)((H - s0) < NB ? (H - s0) : NB);
                    for (int l = 0; l < nb; l++) {
                        u64 s = s0 + l;
                        if (!famP) { vb[l] = sb(y, gam[0]); tb[l] = ad(vb[l], vb[l]); }
                        else { vb[l] = y; tb[l] = sb(y, gam[1]); }
                        y = mulm(y, GK); if (WIN && tst + s + 1 == H) y = powm(g, cm); /* wrap t = H -> 0 */
                    }
                    inQ_batch(tb, mv, nb, okb);
                    for (int l = 0; l < nb; l++) if (okb[l] && vb[l] != gam[0]) { Lk[c2++] = (u32)vb[l]; if (WIN && (u64)c2 >= WIN) { stop = 1; break; } }
                }
                Scnt[0][k] = c2;
            }
            int dr = dfs(0, kfirst); if (dr == -1) hitlim = 1;
            if (dr == 1) {
                if (!famP) for (long j = 0; j < (long)K; j++) { al[j] = gam[j]; be[j] = gam[md(j + (long)B)]; }
                else for (long j = 0; j < (long)K; j++) { al[j] = gam[j]; be[j] = sb(0, gam[md(j + (long)B)]); }
                u64 s = be[0];
                for (long t = 0; t < (long)K; t++) { al[t] = ad(al[t], s); be[t] = sb(be[t], s); }
                u64 sc = powm(al[0], P - 2);
                for (long t = 0; t < (long)K; t++) { al[t] = mulm(al[t], sc); be[t] = mulm(be[t], sc); }
                found = famP ? (checkP(al, be, g, &nzero) ? 1 : -1) : (check(al, be, g) ? 1 : -1);
            }
        }
        double dt = now() - t0;
        if (found == 1) { nf++; printf("FOUND k=%llu p=%llu g=%llu mode=%s tries=%ld secs=%.3f ", (unsigned long long)K, (unsigned long long)p, (unsigned long long)g, mname, tries, dt);
            if (famP) printf("b=%llu zeros=%d ", (unsigned long long)B, nzero);
            printf("beta=");
            for (u64 i = 0; i < K; i++) printf("%llu%s", (unsigned long long)be[i], i + 1 < K ? "," : "");
            printf(" alpha="); for (u64 j = 0; j < K; j++) printf("%llu%s", (unsigned long long)al[j], j + 1 < K ? "," : ""); printf("\n"); }
        else if (found == -1) { printf("BUG p=%llu\n", (unsigned long long)p); return 2; }
        else { nn++; printf("NOTFOUND k=%llu p=%llu mode=%s tries=%ld secs=%.3f %s\n", (unsigned long long)K, (unsigned long long)p, mname, tries, dt, complete ? (hitlim ? "LIMIT" : (WIN ? "WINDOW_EMPTY" : "COMPLETE_EMPTY")) : ""); }
        fflush(stdout);
    }
    printf("DONE k=%llu range=[%llu,%llu] mode=%s%s found=%ld notfound=%ld\n", (unsigned long long)K, (unsigned long long)P0, (unsigned long long)P1, mname, hodd ? "(hodd)" : "", nf, nn);
    return 0;
}
