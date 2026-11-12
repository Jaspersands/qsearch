/* e2dfs.c -- independent decision procedure for E_2(kappa) (harsh referee, 2026-11-12).
 *
 * Problem (my reformulation, see the report section 2):
 *   p prime, kappa | p-1, Q_m = g^m (F_p^*)^kappa for a primitive root g, Qo_m = Q_m u {0}.
 *   A two-level contraction exists  <=>  there are x_0..x_{k-1}, y_0..y_{k-1} in F_p, not all
 *   2k values equal, with  x_j - y_i in Qo_{-(i+j)}  for all i,j in Z_k.
 *   (x_j = alpha_j, y_i = -beta_i.)  After an index shift, a translation and a Q_0-scaling
 *   one may assume x_0 = 1, y_0 = 0.  This program decides whether such a normalised solution
 *   exists by a complete depth-first search with forward checking on bitset domains
 *   (smallest domain first).  It prints one certificate (x,y) or "MEMBER".
 *
 * Usage: e2dfs kappa pmin pmax [nodelimit]
 *   nodelimit = 0 means exhaustive; otherwise the search gives up after that many nodes and
 *   prints "UNDECIDED" (only used for non-member certificate hunting).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef uint64_t u64;
static int K, P, W;              /* kappa, prime, words per bitset */
static unsigned char *ind;       /* ind[x] in 0..K-1, 255 for x = 0 */
static u64 **Bo;                 /* Bo[m]  = Qo_m,  doubled length 2P bits */
static u64 **Ro;                 /* Ro[m]  = -Qo_m, doubled length 2P bits */
static long long nodes, nodelimit;
static int NV;                   /* 2K-2 variables: 0..K-2 -> x_1..x_{K-1}; K-1.. -> y_1..y_{K-1} */
static int val[64];
static u64 *dom[40][40];         /* dom[level][var] */

static u64 mulmod(u64 a, u64 b, u64 m) { return (unsigned __int128)a * b % m; }
static u64 powmod(u64 a, u64 e, u64 m) { u64 r = 1; a %= m; while (e) { if (e & 1) r = mulmod(r, a, m); a = mulmod(a, a, m); e >>= 1; } return r; }
static int isprime(long n) { if (n < 2) return 0; for (long d = 2; d * d <= n; d++) if (n % d == 0) return 0; return 1; }

static int primroot(int p) {
  int f[32], nf = 0; int n = p - 1;
  for (int d = 2; (long)d * d <= n; d++) if (n % d == 0) { f[nf++] = d; while (n % d == 0) n /= d; }
  if (n > 1) f[nf++] = n;
  for (int g = 2; g < p; g++) { int ok = 1; for (int i = 0; i < nf; i++) if (powmod(g, (p - 1) / f[i], p) == 1) { ok = 0; break; } if (ok) return g; }
  return -1;
}
static inline int getbit(const u64 *b, long i) { return (b[i >> 6] >> (i & 63)) & 1; }
static inline void setbit(u64 *b, long i) { b[i >> 6] |= (u64)1 << (i & 63); }

/* out[x] &= S[(x - w) mod P] for x in [0,P), S doubled (bits t and t+P equal). */
static void and_shift(u64 *out, const u64 *S2, int w) {
  long off = (long)P - w; if (off >= P) off -= P;   /* bit index of x=0 in S2 is off = (0-w) mod P */
  long wo = off >> 6; int bo = off & 63;
  for (int k = 0; k < W; k++) {
    u64 lo = S2[wo + k] >> bo;
    u64 hi = bo ? (S2[wo + k + 1] << (64 - bo)) : 0;
    out[k] &= (lo | hi);
  }
  int r = P & 63; if (r) out[W - 1] &= (((u64)1 << r) - 1);
}
static int popc(const u64 *b) { int c = 0; for (int k = 0; k < W; k++) c += __builtin_popcountll(b[k]); return c; }
static inline int md(int a) { a %= K; if (a < 0) a += K; return a; }

/* variable v: isx = v < K-1, index = (v % (K-1)) + 1 */
static int dfs(int lev, unsigned assigned) {
  if (nodelimit && nodes > nodelimit) return -1;
  nodes++;
  /* choose MRV */
  int best = -1, bc = 1 << 30;
  for (int v = 0; v < NV; v++) if (!(assigned >> v & 1)) { int c = popc(dom[lev][v]); if (c == 0) return 0; if (c < bc) { bc = c; best = v; } }
  if (best < 0) return 1;  /* all assigned */
  int isx = best < K - 1, idx = best % (K - 1) + 1;
  u64 *D = dom[lev][best];
  for (int k = 0; k < W; k++) {
    u64 wd = D[k];
    while (wd) {
      int b = __builtin_ctzll(wd); wd &= wd - 1;
      int a = k * 64 + b;
      val[best] = a;
      /* propagate */
      int dead = 0;
      for (int v = 0; v < NV; v++) {
        if ((assigned >> v & 1) || v == best) continue;
        memcpy(dom[lev + 1][v], dom[lev][v], W * sizeof(u64));
        int visx = v < K - 1, vidx = v % (K - 1) + 1;
        if (visx == isx) continue;      /* no x-x or y-y constraints */
        if (isx) { /* x_idx = a; y_vidx must satisfy a - y in Qo_{-(vidx+idx)}: y in a + Ro */
          and_shift(dom[lev + 1][v], Ro[md(-(vidx + idx))], a);
        } else {   /* y_idx = a; x_vidx in a + Qo_{-(idx+vidx)} */
          and_shift(dom[lev + 1][v], Bo[md(-(idx + vidx))], a);
        }
        if (popc(dom[lev + 1][v]) == 0) { dead = 1; break; }
      }
      if (dead) continue;
      int r = dfs(lev + 1, assigned | (1u << best));
      if (r != 0) return r;
    }
  }
  return 0;
}

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage\n"); return 1; }
  K = atoi(argv[1]); long pmin = atol(argv[2]), pmax = atol(argv[3]);
  nodelimit = argc > 4 ? atoll(argv[4]) : 0;
  NV = 2 * K - 2;
  for (long p = pmin; p <= pmax; p++) {
    if ((p - 1) % K || !isprime(p) || p < 3) continue;
    P = (int)p; W = (P + 63) / 64;
    int g = primroot(P);
    ind = malloc(P); ind[0] = 255;
    u64 x = 1; for (int e = 0; e < P - 1; e++) { ind[x] = e % K; x = x * g % P; }
    Bo = malloc(K * sizeof(u64 *)); Ro = malloc(K * sizeof(u64 *));
    int W2 = (2 * P + 63) / 64 + 2;
    for (int m = 0; m < K; m++) {
      Bo[m] = calloc(W2, 8); Ro[m] = calloc(W2, 8);
      for (int t = 0; t < 2 * P; t++) {
        int y = t % P;
        if (y == 0 || ind[y] == m) setbit(Bo[m], t);
        int ny = (P - y) % P;
        if (ny == 0 || ind[ny] == m) setbit(Ro[m], t);
      }
    }
    for (int l = 0; l <= NV + 1; l++) for (int v = 0; v < NV; v++) { dom[l][v] = calloc(W, 8); }
    /* initial domains: x_j in Qo_{-j} (constraint with y_0 = 0); y_i with 1 - y_i in Qo_{-i} (x_0 = 1),
       i.e. y in 1 + Ro_{-i}. Also x_0=1,y_0=0 themselves: 1 - 0 = 1 in Q_0, fine. */
    for (int v = 0; v < NV; v++) {
      int isx = v < K - 1, idx = v % (K - 1) + 1;
      memset(dom[0][v], 0xff, W * 8);
      int r = P & 63; if (r) dom[0][v][W - 1] = (((u64)1 << r) - 1);
      if (isx) and_shift(dom[0][v], Bo[md(-idx)], 0);
      else and_shift(dom[0][v], Ro[md(-idx)], 1);
    }
    nodes = 0;
    int res = dfs(0, 0);
    if (res == 1) {
      printf("%ld NONMEMBER nodes=%lld x=1", p, nodes);
      for (int j = 1; j < K; j++) printf(",%d", val[j - 1]);
      printf(" y=0");
      for (int i = 1; i < K; i++) printf(",%d", val[K - 1 + i - 1]);
      printf("\n");
    } else if (res == 0) printf("%ld MEMBER nodes=%lld\n", p, nodes);
    else printf("%ld UNDECIDED nodes=%lld\n", p, nodes);
    fflush(stdout);
    for (int l = 0; l <= NV + 1; l++) for (int v = 0; v < NV; v++) free(dom[l][v]);
    for (int m = 0; m < K; m++) { free(Bo[m]); free(Ro[m]); }
    free(Bo); free(Ro); free(ind);
  }
  return 0;
}
