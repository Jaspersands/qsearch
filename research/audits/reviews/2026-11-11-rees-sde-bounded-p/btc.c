/* C port of bt.py (same encoding, same search): decide d-feasibility with weak nondegeneracy of a
 * P-closed label set, S = P u {0}, P = kappa-th powers in F_p.  Input on stdin:
 *     p kappa k d n  then n label representatives (k integers each), one per P-class.
 * Output: "SAT nodes" + the solution (phi index per label, gamma index per slot) or "UNSAT nodes".
 * SAT answers are re-verified in Python (btc_run.py); UNSAT answers are [computed], not certified.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXW 8          /* up to 512 gamma values */
#define MAXL 128
#define MAXS 64
#define MAXF 64
typedef struct { uint64_t w[MAXW]; } bs;

static int p, kap, k, d, n, W, G, nS, nslot, nphi;
static int Sv[64], inS[64], Pv[64], nP, creps[64], ncr;
static int dirs[64][4], ndir, alpha[MAXS][4], slotD[MAXS], slotC[MAXS], fixed_[MAXS];
static int lab[MAXL][8], phis[MAXF][4];
static bs A[MAXS][MAXL][MAXF], NZ[MAXS][MAXL][MAXF];
static int assign_[MAXL];
static long long nodes = 0, node_limit = 0;
static int sol_gamma[MAXS];

static int bs_and_nz(const bs *a, const bs *b) { for (int i = 0; i < W; i++) if (a->w[i] & b->w[i]) return 1; return 0; }
static int bs_nz(const bs *a) { for (int i = 0; i < W; i++) if (a->w[i]) return 1; return 0; }
static int bs_first(const bs *a) { for (int i = 0; i < W; i++) if (a->w[i]) return i * 64 + __builtin_ctzll(a->w[i]); return -1; }

static int leaf(bs *m) {
  for (int D = 0; D < ndir; D++) {
    int okD = 0;
    for (int c = 0; c < ncr; c++) {
      int s = D * ncr + c;
      bs nz; memset(&nz, 0, sizeof nz);
      for (int l = 0; l < n; l++) for (int i = 0; i < W; i++) nz.w[i] |= NZ[s][l][assign_[l]].w[i];
      bs g; for (int i = 0; i < W; i++) g.w[i] = m[s].w[i] & nz.w[i];
      if (bs_nz(&g)) { okD = 1; sol_gamma[s] = bs_first(&g); }
      else sol_gamma[s] = bs_first(&m[s]);
    }
    if (!okD) return 0;
  }
  return 1;
}

static int rec(bs *m, int depth) {
  nodes++;
  if (node_limit && nodes > node_limit) { printf("TIMEOUT %lld\n", nodes); exit(0); }
  if (depth == n) return leaf(m);
  int best = -1, bestc = 1 << 30; int live[MAXF], nl = 0, bl[MAXF];
  for (int l = 0; l < n; l++) {
    if (assign_[l] >= 0) continue;
    nl = 0;
    for (int f = 0; f < nphi; f++) {
      if (depth == 0) {  /* symmetry: WLOG phi of the first label is (0..0,1..1) (coordinate
                            permutations and P-scalings of Phi coordinates; see bt_sym note) */
        int canon = 1, seen1 = 0;
        for (int i = 0; i < d; i++) { int v = phis[f][i]; if (v != 0 && v != 1) canon = 0; if (v == 1) seen1 = 1; else if (seen1) canon = 0; }
        if (!canon) continue;
      }
      int ok = 1;
      for (int s = 0; s < nslot; s++) if (!bs_and_nz(&m[s], &A[s][l][f])) { ok = 0; break; }
      if (ok) live[nl++] = f;
    }
    if (nl == 0) return 0;
    if (nl < bestc) { bestc = nl; best = l; memcpy(bl, live, sizeof(int) * nl); if (nl == 1) break; }
  }
  bs *nm = malloc(sizeof(bs) * nslot);
  for (int j = 0; j < bestc; j++) {
    int f = bl[j];
    for (int s = 0; s < nslot; s++) for (int i = 0; i < W; i++) nm[s].w[i] = m[s].w[i] & A[s][best][f].w[i];
    assign_[best] = f;
    if (rec(nm, depth + 1)) { free(nm); return 1; }
    assign_[best] = -1;
  }
  free(nm);
  return 0;
}

int main(int argc, char **argv) {
  if (argc > 1) node_limit = atoll(argv[1]);
  if (scanf("%d %d %d %d %d", &p, &kap, &k, &d, &n) != 5) return 1;
  for (int l = 0; l < n; l++) for (int i = 0; i < k; i++) if (scanf("%d", &lab[l][i]) != 1) return 1;
  memset(inS, 0, sizeof inS); nP = 0;
  for (int x = 1; x < p; x++) { long y = 1; for (int e = 0; e < kap; e++) y = y * x % p; if (!inS[y]) { inS[y] = 1; Pv[nP++] = (int)y; } }
  inS[0] = 1; nS = 0; for (int x = 0; x < p; x++) if (inS[x]) Sv[nS++] = x;
  int seen[64] = {0}; ncr = 0;
  for (int x = 1; x < p; x++) if (!seen[x]) { creps[ncr++] = x; for (int j = 0; j < nP; j++) seen[x * Pv[j] % p] = 1; }
  /* projective directions of F_p^d, first nonzero coordinate 1, in itertools.product order */
  ndir = 0; int tot = 1; for (int i = 0; i < d; i++) tot *= p;
  for (int t = 0; t < tot; t++) {
    int a[4], x = t; for (int i = d - 1; i >= 0; i--) { a[i] = x % p; x /= p; }
    int lead = -1; for (int i = 0; i < d; i++) if (a[i]) { lead = a[i]; break; }
    if (lead == 1) { memcpy(dirs[ndir++], a, sizeof a); }
  }
  nslot = ndir * ncr;
  for (int D = 0; D < ndir; D++) for (int c = 0; c < ncr; c++) {
    int s = D * ncr + c; slotD[s] = D; slotC[s] = c;
    for (int i = 0; i < d; i++) alpha[s][i] = creps[c] * dirs[D][i] % p;
    int unit = 0; for (int j = 0; j < d; j++) { int u = 1; for (int i = 0; i < d; i++) if (dirs[D][i] != (i == j)) u = 0; unit |= u; }
    fixed_[s] = (c == 0 && unit);
  }
  G = 1; for (int i = 0; i < k; i++) G *= p; W = (G + 63) / 64;
  if (W > MAXW || n > MAXL || nslot > MAXS) { fprintf(stderr, "too big\n"); return 2; }
  nphi = 1; for (int i = 0; i < d; i++) nphi *= nS;
  for (int f = 0; f < nphi; f++) { int x = f; for (int i = d - 1; i >= 0; i--) { phis[f][i] = Sv[x % nS]; x /= nS; } }
  for (int s = 0; s < nslot; s++) for (int l = 0; l < n; l++) for (int f = 0; f < nphi; f++) {
    int base = 0; for (int j = 0; j < d; j++) base += alpha[s][j] * phis[f][j]; base %= p;
    bs m, z; memset(&m, 0, sizeof m); memset(&z, 0, sizeof z);
    for (int g = 0; g < G; g++) {
      int x = g, gv[8]; for (int i = k - 1; i >= 0; i--) { gv[i] = x % p; x /= p; }
      int v = base; for (int i = 0; i < k; i++) v += gv[i] * lab[l][i]; v %= p;
      if (inS[v]) { m.w[g / 64] |= 1ULL << (g % 64); if (v) z.w[g / 64] |= 1ULL << (g % 64); }
    }
    A[s][l][f] = m; NZ[s][l][f] = z;
  }
  bs *m0 = malloc(sizeof(bs) * nslot);
  for (int s = 0; s < nslot; s++) {
    memset(&m0[s], 0, sizeof(bs));
    if (fixed_[s]) m0[s].w[0] = 1;
    else for (int g = 0; g < G; g++) m0[s].w[g / 64] |= 1ULL << (g % 64);
  }
  for (int l = 0; l < n; l++) assign_[l] = -1;
  int r = rec(m0, 0);
  if (r) {
    printf("SAT %lld\n", nodes);
    for (int l = 0; l < n; l++) printf("%d ", assign_[l]); printf("\n");
    for (int s = 0; s < nslot; s++) printf("%d ", sol_gamma[s]); printf("\n");
  } else printf("UNSAT %lld\n", nodes);
  return 0;
}
