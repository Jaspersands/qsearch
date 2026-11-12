/* wcheck.c -- own definition-level checker for stored two-level contraction witnesses,
 * plus coverage of a prime range (harsh referee, 2026-11-12).
 *
 * Reads lines on stdin.  Two formats are accepted:
 *   repo:  "... k=K p=P g=G ... beta=b0,..,b{K-1} alpha=a0,..,a{K-1}"  (FOUND / FEASIBLE lines)
 *   own :  "P NONMEMBER nodes=.. x=x0,.. y=y0,.."   (e2dfs output; g = least primitive root)
 * Check (definition, with Q_m = g^m (F_p^*)^K, zeta = g^h, h = (p-1)/K):
 *   p prime, K | p-1, zeta has exact order K;  alpha_0 + beta_0 != 0;
 *   for all i,j: v = alpha_j + beta_i;  v == 0 or v^h == zeta^((-(i+j)) mod K).
 * (own format: alpha = x, beta = -y.)
 * Usage: wcheck K LO HI < lines     -> counts, and the primes p = 1 mod K in (LO,HI] with no
 * verified witness (count, and the first 60).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint64_t u64;
static u64 mulm(u64 a, u64 b, u64 m) { return (unsigned __int128)a * b % m; }
static u64 powm(u64 a, u64 e, u64 m) { u64 r = 1; a %= m; while (e) { if (e & 1) r = mulm(r, a, m); a = mulm(a, a, m); e >>= 1; } return r; }
static int isprime(u64 n) { if (n < 2) return 0; for (u64 d = 2; d * d <= n; d++) if (n % d == 0) return 0; return 1; }
static u64 primroot(u64 p) {
  u64 f[64]; int nf = 0; u64 n = p - 1;
  for (u64 d = 2; d * d <= n; d++) if (n % d == 0) { f[nf++] = d; while (n % d == 0) n /= d; }
  if (n > 1) f[nf++] = n;
  for (u64 g = 2; g < p; g++) { int ok = 1; for (int i = 0; i < nf; i++) if (powm(g, (p - 1) / f[i], p) == 1) { ok = 0; break; } if (ok) return g; }
  return 0;
}
static int parse_list(const char *s, long long *v, int K) {
  int n = 0; while (n < K) { char *e; v[n++] = strtoll(s, &e, 10); if (*e != ',') break; s = e + 1; }
  return n;
}
static int check(int K, u64 p, u64 g, long long *al, long long *be) {
  if ((p - 1) % K || !isprime(p)) return 0;
  u64 h = (p - 1) / K, z = powm(g, h, p);
  for (int d = 1; d < K; d++) if (K % d == 0 && powm(z, d, p) == 1) return 0;   /* exact order K */
  if (powm(z, K, p) != 1) return 0;
  u64 zp[64]; zp[0] = 1; for (int m = 1; m < K; m++) zp[m] = mulm(zp[m - 1], z, p);
  long long a0 = ((al[0] + be[0]) % (long long)p + p) % p; if (a0 == 0) return 0;
  for (int i = 0; i < K; i++) for (int j = 0; j < K; j++) {
    long long v = ((al[j] + be[i]) % (long long)p + p) % p;
    if (v == 0) continue;
    int m = ((-(i + j)) % K + K) % K;
    if (powm(v, h, p) != zp[m]) return 0;
  }
  return 1;
}
int main(int argc, char **argv) {
  int K = atoi(argv[1]); u64 LO = strtoull(argv[2], 0, 10), HI = strtoull(argv[3], 0, 10);
  unsigned char *cov = calloc(HI / K + 2, 1);
  char line[1 << 16]; long ok = 0, bad = 0, other = 0;
  while (fgets(line, sizeof line, stdin)) {
    long long al[64], be[64]; u64 p = 0, g = 0; int k = K;
    char *pk = strstr(line, "k="), *pp = strstr(line, " p="), *pg = strstr(line, " g="), *pb = strstr(line, "beta="), *pa = strstr(line, "alpha=");
    char *px = strstr(line, " x="), *py = strstr(line, " y=");
    if (pk && pp && pg && pb && pa) {
      k = atoi(pk + 2); if (k != K) { other++; continue; }
      p = strtoull(pp + 3, 0, 10); g = strtoull(pg + 3, 0, 10);
      if (parse_list(pb + 5, be, K) != K || parse_list(pa + 6, al, K) != K) { bad++; continue; }
    } else if (strstr(line, "NONMEMBER") && px && py) {
      p = strtoull(line, 0, 10); g = primroot(p);
      long long x[64], y[64];
      if (parse_list(px + 3, x, K) != K || parse_list(py + 3, y, K) != K) { bad++; continue; }
      for (int i = 0; i < K; i++) { al[i] = x[i]; be[i] = -y[i]; }
    } else continue;
    if (check(K, p, g, al, be)) { ok++; if (p <= HI) cov[p / K] = 1; }
    else { bad++; fprintf(stderr, "BAD k=%d p=%llu\n", K, (unsigned long long)p); }
  }
  /* coverage via segmented trial: sieve primes up to HI */
  unsigned char *comp = calloc(HI + 1, 1);
  for (u64 i = 2; i * i <= HI; i++) if (!comp[i]) for (u64 j = i * i; j <= HI; j += i) comp[j] = 1;
  long tot = 0, miss = 0;
  printf("K=%d verified=%ld bad=%ld (other-kappa lines %ld)\n", K, ok, bad, other);
  printf("missing primes p=1 mod %d in (%llu,%llu]:", K, (unsigned long long)LO, (unsigned long long)HI);
  for (u64 p = LO + 1; p <= HI; p++) if (p > 2 && !comp[p] && (p - 1) % K == 0) {
    tot++; if (!cov[p / K]) { miss++; if (miss <= (argc > 4 ? atol(argv[4]) : 60)) printf(" %llu", (unsigned long long)p); }
  }
  printf("\ntotal=%ld covered=%ld missing=%ld\n", tot, tot - miss, miss);
  return 0;
}
