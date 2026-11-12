/* e2scan.c -- second-moment sampler of prop:app-s2-TA(iii), used as a certificate finder
 * (harsh referee, 2026-11-12).  For each prime p = 1 mod K in [pmin,pmax]: draw y_1..y_{K-1}
 * uniformly (y_0 = 0), scan all x in F_p^* and record, for each j, the first x with
 * x + y_i in Q_{-(i+j)} for all i (strict cosets, Q_m = g^m (F_p^*)^K, g least primitive root).
 * If all K columns are filled, print a witness "FOUND k= p= g= beta=y alpha=x" (alpha_j = x_j,
 * beta_i = y_i); otherwise redraw y, up to TRIES times, then print NOTFOUND.
 * Witnesses are checked afterwards by wcheck.c.  Usage: e2scan K pmin pmax TRIES seed
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint64_t u64;
static u64 powm(u64 a, u64 e, u64 m) { u64 r = 1; a %= m; while (e) { if (e & 1) r = r * a % m; a = a * a % m; e >>= 1; } return r; }
static int isprime(long n) { if (n < 2) return 0; for (long d = 2; d * d <= n; d++) if (n % d == 0) return 0; return 1; }
static long primroot(long p) {
  long f[32]; int nf = 0; long n = p - 1;
  for (long d = 2; d * d <= n; d++) if (n % d == 0) { f[nf++] = d; while (n % d == 0) n /= d; }
  if (n > 1) f[nf++] = n;
  for (long g = 2; g < p; g++) { int ok = 1; for (int i = 0; i < nf; i++) if (powm(g, (p - 1) / f[i], p) == 1) { ok = 0; break; } if (ok) return g; }
  return -1;
}
static u64 rs = 88172645463325252ULL;
static u64 rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
int main(int argc, char **argv) {
  int K = atoi(argv[1]); long pmin = atol(argv[2]), pmax = atol(argv[3]); int TR = atoi(argv[4]);
  rs ^= (u64)atoll(argv[5]) * 0x9E3779B97F4A7C15ULL;
  unsigned char *ind = malloc(pmax + 1);
  for (long p = pmin; p <= pmax; p++) {
    if ((p - 1) % K || !isprime(p)) continue;
    long g = primroot(p);
    ind[0] = 255; u64 x = 1;
    for (long e = 0; e < p - 1; e++) { ind[x] = (unsigned char)(e % K); x = x * g % p; }
    long y[64], ax[64]; int found = 0, t;
    for (t = 0; t < TR && !found; t++) {
      y[0] = 0; for (int i = 1; i < K; i++) y[i] = (long)(rnd() % (u64)p);
      int nfill = 0; for (int j = 0; j < K; j++) ax[j] = -1;
      for (long xx = 1; xx < p && nfill < K; xx++) {
        int c0 = ind[xx]; int j = (K - c0) % K;     /* x in Q_{-j} */
        if (ax[j] >= 0) continue;
        int ok = 1;
        for (int i = 1; i < K; i++) {
          long v = xx + y[i]; if (v >= p) v -= p;
          int want = ((-(i + j)) % K + K) % K;
          if (v == 0 || ind[v] != want) { ok = 0; break; }
        }
        if (ok) { ax[j] = xx; nfill++; }
      }
      if (nfill == K) found = 1;
    }
    if (found) {
      printf("FOUND k=%d p=%ld g=%ld mode=scan tries=%d beta=", K, p, g, t);
      for (int i = 0; i < K; i++) printf(i ? ",%ld" : "%ld", y[i]);
      printf(" alpha=");
      for (int j = 0; j < K; j++) printf(j ? ",%ld" : "%ld", ax[j]);
      printf("\n");
    } else printf("NOTFOUND k=%d p=%ld tries=%d\n", K, p, TR);
    fflush(stdout);
  }
  return 0;
}
