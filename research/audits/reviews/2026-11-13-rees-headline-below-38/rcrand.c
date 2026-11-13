/* Randomized search for RC(D; R -> K) contractions (2026-11-13, AI-written, pending human review).
   Cells: alpha_j + beta_i, i in R (beta_0 = 0), j in Z_D.  Cell (0,0) must lie in Q_0 (nonzero, class 0);
   every other cell must be 0 or have class c with (c + i + j) mod D in K.  Classes w.r.t. generator g.
   Search: random beta_i (i in R \ 0), then for each column j a scan of x in F_p from a random start.
   Returns 1 and a witness, or 0 after `trials` beta draws.  A witness is only a candidate: the caller
   re-checks it with an independent pow()-based checker. */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

static uint64_t rs;
static inline uint64_t rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }

int rc_random(int p, int g, int D, const int *R, int r, const int *K, int k,
              long long trials, unsigned long long seed, int *alpha_out, int *beta_out) {
    int *cls = malloc(sizeof(int) * (size_t)p);
    if (!cls) return -2;
    cls[0] = -1;
    long long x = 1;
    for (long long e = 0; e < p - 1; e++) { cls[x] = (int)(e % D); x = x * g % p; }
    int inK[64]; memset(inK, 0, sizeof inK);
    for (int a = 0; a < k; a++) inK[((K[a] % D) + D) % D] = 1;
    int beta[64];
    rs = seed * 2654435761ULL + 88172645463325252ULL;
    int found = 0;
    for (long long t = 0; t < trials && !found; t++) {
        beta[0] = 0;
        for (int a = 1; a < r; a++) beta[a] = (int)(rnd() % (uint64_t)p);
        int ok = 1;
        for (int j = 0; j < D && ok; j++) {
            long long start = (long long)(rnd() % (uint64_t)p);
            int got = 0;
            for (long long s = 0; s < p; s++) {
                long long xx = start + s; if (xx >= p) xx -= p;
                int good = 1;
                for (int a = 0; a < r && good; a++) {
                    int i = R[a];
                    long long v = xx + beta[a]; if (v >= p) v -= p;
                    if (i == 0 && j == 0) { if (v == 0 || cls[v] != 0) good = 0; }
                    else if (v != 0 && !inK[(cls[v] + i + j) % D]) good = 0;
                }
                if (good) { alpha_out[j] = (int)xx; got = 1; break; }
            }
            if (!got) ok = 0;
        }
        if (ok) { found = 1; for (int a = 0; a < r; a++) beta_out[a] = beta[a]; }
    }
    free(cls);
    return found;
}
