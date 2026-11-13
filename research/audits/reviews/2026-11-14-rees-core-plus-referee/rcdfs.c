/* rcdfs.c -- exhaustive search for RC(D; Delta -> Omega) contractions (Definition plus-rc of
 * main-core.tex, sec:plus), written from the text only (2026-11-14 referee, AI).
 *
 * Contraction: alpha in F_p^{Z_D}, beta in F_p^{Delta}, alpha_0+beta_0 in P_D, and for all
 * i in Delta, j in Z_D: alpha_j+beta_i = 0 or cl_D(alpha_j+beta_i)+i+j in Omega.
 * WLOG (translation, then scaling by an element of P_D): beta_0 = 0, alpha_0 = 1.
 * cl_D(x) = dlog_g(x) mod D for the given primitive root g.
 *
 * stdin, one query per line:  p g D r d_1..d_r w o_1..o_w cap
 *   (Delta = {d_1..d_r} must contain 0; Omega = {o_1..o_w} must contain 0)
 * stdout per query: FOUND a_0..a_{D-1} B b_{d_1}..b_{d_r} nodes   |  NONE nodes  |  CAP nodes
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXW 1024           /* p <= 65536 */
typedef uint64_t u64;

static int P, Dm, R, Wn, NW;
static int delta[16], omega_[16], inom[16];
static int *cl;
static u64 *DG[16];        /* doubled bitsets of G_k, k in Z_D */
static u64 colbuf[16][16][MAXW];  /* level x column x words */
static long long nodes, cap;
static int beta_val[16];
static int found;

static inline int getbit(const u64 *b, int x) { return (b[x >> 6] >> (x & 63)) & 1; }

/* out[x] = DG_k[x+s], x in [0,P) */
static void window(const u64 *dg, int s, u64 *out) {
  for (int w = 0; w < NW; w++) {
    int o = s + 64 * w;
    int src = o >> 6, sh = o & 63;
    u64 v = dg[src] >> sh;
    if (sh) v |= dg[src + 1] << (64 - sh);
    out[w] = v;
  }
  int rem = P & 63;
  if (rem) out[NW - 1] &= ((u64)1 << rem) - 1;
}

static int empty(const u64 *b) { for (int w = 0; w < NW; w++) if (b[w]) return 0; return 1; }

static u64 tmpw[MAXW];

/* level t: assigning beta for delta index t (t = 1..R-1; delta[0] = 0) */
static void dfs(int t) {
  if (found) return;
  if (nodes > cap) return;
  if (t == R) { found = 1; return; }
  int i = delta[t];
  u64 dom[MAXW];
  window(DG[i % Dm], 1, dom);           /* column 0: 1 + beta_i in G_i */
  for (int w = 0; w < NW && !found; w++) {
    u64 v = dom[w];
    while (v && !found) {
      int b = __builtin_ctzll(v); v &= v - 1;
      int beta = 64 * w + b;
      nodes++;
      if (nodes > cap) return;
      int ok = 1;
      for (int j = 1; j < Dm && ok; j++) {
        window(DG[(i + j) % Dm], beta, tmpw);
        u64 any = 0;
        for (int x = 0; x < NW; x++) { colbuf[t + 1][j][x] = colbuf[t][j][x] & tmpw[x]; any |= colbuf[t + 1][j][x]; }
        if (!any) ok = 0;
      }
      if (ok) {
        beta_val[t] = beta;
        dfs(t + 1);
        if (found) return;
      }
    }
  }
}

static long long mulmod(long long a, long long b, long long m) { return (a * b) % m; }

int main(void) {
  long long p, g;
  while (scanf("%lld %lld", &p, &g) == 2) {
    int D, r, w;
    if (scanf("%d %d", &D, &r) != 2) return 1;
    for (int k = 0; k < r; k++) scanf("%d", &delta[k]);
    scanf("%d", &w);
    for (int k = 0; k < w; k++) scanf("%d", &omega_[k]);
    scanf("%lld", &cap);
    P = (int)p; Dm = D; R = r; Wn = w; NW = (P + 63) / 64;
    if (NW + 2 > MAXW) { printf("ERR p too large\n"); fflush(stdout); continue; }
    /* put 0 first in delta */
    for (int k = 0; k < r; k++) if (delta[k] == 0) { int tt = delta[0]; delta[0] = 0; delta[k] = tt; break; }
    if (delta[0] != 0) { printf("ERR delta lacks 0\n"); fflush(stdout); continue; }
    memset(inom, 0, sizeof inom);
    for (int k = 0; k < w; k++) inom[omega_[k] % D] = 1;
    if (!inom[0]) { printf("ERR omega lacks 0\n"); fflush(stdout); continue; }
    cl = (int *)malloc(sizeof(int) * P);
    cl[0] = -1;
    long long x = 1;
    for (int k = 0; k < P - 1; k++) { cl[x] = k % D; x = mulmod(x, g, p); }
    if (x != 1) { printf("ERR g\n"); fflush(stdout); free(cl); continue; }
    /* check g primitive: g^k != 1 for 0<k<p-1 is implied if all cl assigned distinct ... check orbit */
    {
      long long y = g % p; int ord = 1; while (y != 1) { y = mulmod(y, g, p); ord++; }
      if (ord != P - 1) { printf("ERR g not primitive\n"); fflush(stdout); free(cl); continue; }
    }
    for (int k = 0; k < D; k++) {
      DG[k] = (u64 *)calloc(2 * NW + 4, sizeof(u64));
      for (int y = 0; y < 2 * P; y++) {
        int yy = y % P;
        int in = (yy == 0) ? 1 : inom[(cl[yy] + k) % D];
        if (in) DG[k][y >> 6] |= (u64)1 << (y & 63);
      }
    }
    /* columns j != 0: alpha_j in G_j (i = 0, beta_0 = 0) */
    for (int j = 1; j < D; j++) window(DG[j], 0, colbuf[1][j]);
    /* note: level index t uses colbuf[t]; start at t=1 with colbuf[1] */
    nodes = 0; found = 0;
    int okstart = 1;
    for (int j = 1; j < D; j++) if (empty(colbuf[1][j])) okstart = 0;
    /* column 0: alpha_0 = 1, needs (i=0): cl(1)+0 = 0 in Omega: fine */
    if (okstart) {
      if (R == 1) found = 1; else dfs(1);
    }
    if (found) {
      /* pick alphas and verify fully */
      int alpha[16]; alpha[0] = 1;
      for (int j = 1; j < D; j++) {
        u64 *b = colbuf[R][j]; int a = -1;
        for (int ww = 0; ww < NW && a < 0; ww++) if (b[ww]) a = 64 * ww + __builtin_ctzll(b[ww]);
        alpha[j] = a;
      }
      beta_val[0] = 0;
      int bad = 0;
      for (int ii = 0; ii < R; ii++) for (int j = 0; j < D; j++) {
        int s = (alpha[j] + beta_val[ii]) % P;
        if (s == 0) { if (ii == 0 && j == 0) bad = 1; continue; }
        if (!inom[(cl[s] + delta[ii] + j) % D]) bad = 1;
      }
      if (cl[(alpha[0] + beta_val[0]) % P] != 0) bad = 1;
      if (bad) printf("ERR verify\n");
      else {
        printf("FOUND");
        for (int j = 0; j < D; j++) printf(" %d", alpha[j]);
        printf(" B");
        for (int ii = 0; ii < R; ii++) printf(" %d:%d", delta[ii], beta_val[ii]);
        printf(" %lld\n", nodes);
      }
    } else if (nodes > cap) printf("CAP %lld\n", nodes);
    else printf("NONE %lld\n", nodes);
    fflush(stdout);
    for (int k = 0; k < D; k++) free(DG[k]);
    free(cl);
  }
  return 0;
}
