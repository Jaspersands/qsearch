/* Per-prime second-moment certificate Phi(p, kappa) < 1 (see second_moment.py).
 *
 *   R   = E[n^2]/E[n]^2 = p^(k-1)/h^k + sum_c (r_c/h) prod_{b != -c} (m_b p / h^2)
 *   Phi = k (1 - 1/R)
 * with m_b = #{v in Q_b : v+1 in Q_b}, r_c = #{w in Q_0, w != 1 : w-1 in Q_c}.
 * Phi < 1 certifies a universal two-level contraction at p (proved in the report).
 *
 * Usage: phiscan KAPPA PMIN PMAX
 * Prints every prime p = 1 mod KAPPA in [PMIN, PMAX] with Phi >= 1 - 1e-9
 * ("UNCERT"), then a summary line with the largest uncertified prime and the
 * smallest margin 1 - Phi among certified primes (floating point, long double).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static int is_prime(uint64_t n) {
    if (n < 2) return 0;
    for (uint64_t d = 2; d * d <= n; d++) if (n % d == 0) return 0;
    return 1;
}

static uint64_t powmod(uint64_t b, uint64_t e, uint64_t m) {
    uint64_t r = 1; b %= m;
    while (e) { if (e & 1) r = r * b % m; b = b * b % m; e >>= 1; }
    return r;
}

static uint64_t primroot(uint64_t p) {
    uint64_t f[64]; int nf = 0; uint64_t n = p - 1;
    for (uint64_t d = 2; d * d <= n; d++)
        if (n % d == 0) { f[nf++] = d; while (n % d == 0) n /= d; }
    if (n > 1) f[nf++] = n;
    for (uint64_t g = 2;; g++) {
        int ok = 1;
        for (int i = 0; i < nf && ok; i++) if (powmod(g, (p - 1) / f[i], p) == 1) ok = 0;
        if (ok) return g;
    }
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: phiscan KAPPA PMIN PMAX\n"); return 1; }
    int k = atoi(argv[1]);
    uint64_t pmin = strtoull(argv[2], 0, 10), pmax = strtoull(argv[3], 0, 10);
    uint8_t *idx = malloc(pmax + 2);
    long ncert = 0, nunc = 0; uint64_t last_unc = 0, minp = 0;
    long double minmargin = 1e30L;
    uint64_t start = pmin - (pmin - 1) % k; if (start < pmin) start += k;
    for (uint64_t p = start; p <= pmax; p += k) {
        if (p < 3 || !is_prime(p)) continue;
        uint64_t g = primroot(p), v = 1;
        for (uint64_t e = 0; e < p - 1; e++) { idx[v] = (uint8_t)(e % k); v = v * g % p; }
        long m[64] = {0}, r[64] = {0};
        for (uint64_t x = 1; x + 1 < p; x++) if (idx[x] == idx[x + 1]) m[idx[x]]++;
        for (uint64_t w = 2; w < p; w++) if (idx[w] == 0) r[idx[w - 1]]++;
        long double h = (long double)((p - 1) / k), P = (long double)p;
        long double R = 1.0L / h;  /* p^(k-1)/h^k = (1/h) (p/h)^(k-1) */
        for (int i = 0; i < k - 1; i++) R *= P / h;
        for (int c = 0; c < k; c++) {
            long double t = (long double)r[c] / h;
            for (int b = 0; b < k; b++) if (b != (k - c) % k) t *= (long double)m[b] * P / (h * h);
            R += t;
        }
        long double phi = k * (1.0L - 1.0L / R);
        if (phi >= 1.0L - 1e-9L) { nunc++; last_unc = p; printf("UNCERT p=%llu Phi=%.6Lf\n", (unsigned long long)p, phi); }
        else { ncert++; if (1.0L - phi < minmargin) { minmargin = 1.0L - phi; minp = p; } }
    }
    printf("SUMMARY k=%d range=[%llu,%llu] certified=%ld uncertified=%ld largest_uncertified=%llu "
           "min_margin=%.3Le at p=%llu\n", k, (unsigned long long)pmin, (unsigned long long)pmax,
           ncert, nunc, (unsigned long long)last_unc, minmargin, (unsigned long long)minp);
    return 0;
}
