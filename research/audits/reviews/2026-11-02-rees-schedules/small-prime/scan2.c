/* Feasibility scan for the universal two-level contraction (general form).
 *
 * For each prime p = 1 mod k in [P0, P1] find alpha, beta in F_p^k with
 * beta_0 = 0, alpha_0 = 1 and alpha_j + beta_i in A_{-(i+j)} = Q_{-(i+j)} U {0}
 * for all i, j (Q_m = g^m H, H = k-th powers).  beta_i = g^{-i} - 1 first
 * (then 1 + beta_i = g^{-i} in Q_{-i}); random admissible beta if that fails.
 * alpha_j sampled as g^{-j} r^k (uniform on Q_{-j}), exhaustive fallback.
 * A found witness is a PROOF of feasibility (every condition tested exactly).
 * Primes where nothing is found are printed as UNRESOLVED for the exact DFS
 * in two_level.py.  Build: cc -O2 -o scan2 scan2.c
 * Usage: ./scan2 k P0 P1 seed
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef uint64_t u64;
static u64 P, H, K, G, OM[64];

static u64 mulm(u64 a, u64 b) { return (u64)((unsigned __int128)a * b % P); }
static u64 powm(u64 a, u64 e) {
    u64 r = 1; a %= P;
    while (e) { if (e & 1) r = mulm(r, a); a = mulm(a, a); e >>= 1; }
    return r;
}
/* y in Q_m U {0}?  (m taken mod K) */
static int inA(u64 y, long m) {
    if (y == 0) return 1;
    m %= (long)K; if (m < 0) m += K;
    return powm(y, H) == OM[m];
}
static u64 rng = 88172645463325252ULL;
static u64 rnd(void) { rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; }

static u64 primroot(u64 p) {
    u64 n = p - 1, f[64]; int nf = 0;
    for (u64 q = 2; q * q <= n; q++) if (n % q == 0) { f[nf++] = q; while (n % q == 0) n /= q; }
    if (n > 1) f[nf++] = n;
    for (u64 g = 2;; g++) {
        int ok = 1;
        for (int i = 0; i < nf; i++) if (powm(g, (p - 1) / f[i]) == 1) { ok = 0; break; }
        if (ok) return g;
    }
}

static int alpha_ok(u64 x, long j, const u64 *beta) {
    for (long i = 1; i < (long)K; i++)
        if (!inA((x + beta[i]) % P, -(i + j))) return 0;
    return 1;
}

/* find alpha_j for given beta; returns 1 and sets *out */
static int find_alpha(long j, const u64 *beta, u64 *out, long trials) {
    u64 gj = powm(powm(G, P - 2), (u64)j);       /* g^{-j} */
    if (alpha_ok(0, j, beta)) { *out = 0; return 1; }
    for (long t = 0; t < trials; t++) {
        u64 r = 1 + rnd() % (P - 1);
        u64 x = mulm(gj, powm(r, K));
        if (alpha_ok(x, j, beta)) { *out = x; return 1; }
    }
    for (u64 x = 1; x < P; x++)
        if (inA(x, -j) && alpha_ok(x, j, beta)) { *out = x; return 1; }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: k P0 P1 seed\n"); return 1; }
    K = strtoull(argv[1], 0, 10);
    u64 P0 = strtoull(argv[2], 0, 10), P1 = strtoull(argv[3], 0, 10);
    rng ^= strtoull(argv[4], 0, 10) * 0x9E3779B97F4A7C15ULL;
    char *comp = calloc(P1 + 1, 1);
    for (u64 i = 2; i * i <= P1; i++) if (!comp[i]) for (u64 j = i * i; j <= P1; j += i) comp[j] = 1;
    long nprimes = 0, nfeas = 0, nunres = 0, nexh = 0;
    long kk = 1; for (u64 i = 0; i < K; i++) kk *= K;     /* k^k */
    for (u64 p = (P0 < 3 ? 3 : P0); p <= P1; p++) {
        if (comp[p] || (p - 1) % K) continue;
        nprimes++;
        P = p; H = (p - 1) / K; G = primroot(p);
        u64 w = powm(G, H); OM[0] = 1; for (u64 m = 1; m < K; m++) OM[m] = mulm(OM[m - 1], w);
        u64 beta[64], alpha[64];
        int found = 0;
        for (int attempt = 0; attempt < 40 && !found; attempt++) {
            beta[0] = 0;
            u64 ginv = powm(G, P - 2);
            for (u64 i = 1; i < K; i++) {
                u64 base = powm(ginv, i);                    /* in Q_{-i} */
                u64 y = attempt == 0 ? base : mulm(base, powm(1 + rnd() % (P - 1), K));
                beta[i] = (y + P - 1) % P;                   /* 1 + beta_i = y */
            }
            int ok = 1;
            alpha[0] = 1;
            for (long j = 1; j < (long)K && ok; j++) {
                long trials = 20 * kk / (long)K + 1000;
                if (!find_alpha(j, beta, &alpha[j], trials)) ok = 0;
            }
            if (ok) found = 1; else nexh++;
        }
        if (found) {
            nfeas++;
            /* full re-check of all k^2 conditions */
            for (u64 i = 0; i < K; i++) for (u64 j = 0; j < K; j++) {
                u64 v = (alpha[j] + beta[i]) % P;
                if (!inA(v, -(long)(i + j))) { printf("BUG p=%llu\n", (unsigned long long)p); return 2; }
            }
            if ((alpha[0] + beta[0]) % P == 0) { printf("BUG00 p=%llu\n", (unsigned long long)p); return 2; }
        } else { nunres++; printf("UNRESOLVED k=%llu p=%llu\n", (unsigned long long)K, (unsigned long long)p); fflush(stdout); }
    }
    printf("DONE k=%llu range=[%llu,%llu] primes=%ld feasible=%ld unresolved=%ld failed_beta_attempts=%ld\n",
           (unsigned long long)K, (unsigned long long)P0, (unsigned long long)P1, nprimes, nfeas, nunres, nexh);
    return 0;
}
