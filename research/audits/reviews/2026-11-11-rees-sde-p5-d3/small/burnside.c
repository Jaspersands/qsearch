/* Burnside counts of GL_3(F_5)-orbits of SPANNING k-subsets (k = 3..10) of
 *   (V) the 124 nonzero vectors of F_5^3, and
 *   (Q) the 62 classes {v,-v} of nonzero vectors (-1 acts trivially on Q).
 * For each g in GL_3(F_5) (all 1,488,000, no conjugacy-class shortcut):
 *   fix_k(X) = [x^k] prod_{cycles c of g on X} (1 + x^{|c|}),
 *   spanning fixed = fix(all) - sum_{g-inv planes P} f2(P) - sum_{g-inv lines l} f1(l),
 *   f1(l) = fix(l\0), f2(P) = fix(P\0) - sum_{g-inv lines l in P} f1(l)
 * (a fixed non-spanning set spans a g-invariant line or plane).  Orbits = sum / |G|.
 * Build: clang -O2 -o burnside burnside.c */
#include <stdio.h>
#include <string.h>
#include <stdint.h>
typedef unsigned __int128 u128;
#define K 10
static int enc(const int *v) { return v[0] * 25 + v[1] * 5 + v[2]; }
static void dec(int x, int *v) { v[0] = x / 25; v[1] = (x / 5) % 5; v[2] = x % 5; }
static int neg(int x) { int v[3]; dec(x, v); for (int i = 0; i < 3; i++) v[i] = (5 - v[i]) % 5; return enc(v); }
static int cls[125], ncls; /* class id of each nonzero vector */
/* polynomial over a subset of points given by mask m (points are 0..npts-1) */
static void fixpoly(const int *perm, int npts, const unsigned char *inset, int64_t *out) {
  int64_t c[K + 1]; memset(c, 0, sizeof c); c[0] = 1;
  static unsigned char seen[128]; memset(seen, 0, sizeof seen);
  for (int s = 0; s < npts; s++) {
    if (!inset[s] || seen[s]) continue;
    int len = 0, x = s;
    do { seen[x] = 1; len++; x = perm[x]; } while (x != s);
    for (int d = K; d >= len; d--) c[d] += c[d - len];
  }
  memcpy(out, c, sizeof c);
}
int main(void) {
  for (int x = 1; x < 125; x++) cls[x] = -1;
  ncls = 0;
  for (int x = 1; x < 125; x++) if (cls[x] < 0) { cls[x] = cls[neg(x)] = ncls++; }
  /* lines (31 projective points) and planes (31 kernels), as vector masks */
  static unsigned char linev[31][125], planev[31][125]; int nl = 0, np = 0;
  static int lseen[125];
  for (int x = 1; x < 125; x++) {
    if (lseen[x]) continue;
    int v[3]; dec(x, v);
    for (int l = 1; l < 5; l++) { int w[3] = {v[0] * l % 5, v[1] * l % 5, v[2] * l % 5}; int y = enc(w); lseen[y] = 1; linev[nl][y] = 1; }
    for (int y = 1; y < 125; y++) { int u[3]; dec(y, u); if ((u[0] * v[0] + u[1] * v[1] + u[2] * v[2]) % 5 == 0) planev[np][y] = 1; }
    nl++; np++;
  }
  /* line l inside plane P */
  static int linplane[31][31];
  for (int a = 0; a < 31; a++) for (int b = 0; b < 31; b++) {
    int ok = 1; for (int y = 1; y < 125; y++) if (linev[a][y] && !planev[b][y]) ok = 0; linplane[a][b] = ok; }
  u128 totV[K + 1], totQ[K + 1]; memset(totV, 0, sizeof totV); memset(totQ, 0, sizeof totQ);
  long ng = 0;
  int m[9];
  for (int code = 0; code < 1953125; code++) {
    int t = code; for (int i = 0; i < 9; i++) { m[i] = t % 5; t /= 5; }
    int det = (m[0] * (m[4] * m[8] - m[5] * m[7]) - m[1] * (m[3] * m[8] - m[5] * m[6]) + m[2] * (m[3] * m[7] - m[4] * m[6])) % 5;
    if (det == 0) continue;
    ng++;
    int pv[124], pq[62]; /* perms on 0-based indices */
    for (int x = 1; x < 125; x++) {
      int v[3], w[3]; dec(x, v);
      for (int i = 0; i < 3; i++) w[i] = (m[3 * i] * v[0] + m[3 * i + 1] * v[1] + m[3 * i + 2] * v[2]) % 5;
      int y = enc(w); pv[x - 1] = y - 1; pq[cls[x]] = cls[y];
    }
    unsigned char inv_l[31], inv_p[31];
    for (int a = 0; a < 31; a++) {
      int ok = 1; for (int y = 1; y < 125 && ok; y++) if (linev[a][y] && !linev[a][pv[y - 1] + 1]) ok = 0; inv_l[a] = ok;
      ok = 1; for (int y = 1; y < 125 && ok; y++) if (planev[a][y] && !planev[a][pv[y - 1] + 1]) ok = 0; inv_p[a] = ok;
    }
    for (int mode = 0; mode < 2; mode++) {
      int npts = mode ? 62 : 124; const int *perm = mode ? pq : pv;
      unsigned char all[124]; memset(all, 1, sizeof all);
      int64_t c[K + 1], f1[31][K + 1], tmp[K + 1];
      fixpoly(perm, npts, all, c);
      unsigned char in[124];
      for (int a = 0; a < 31; a++) {
        if (!inv_l[a]) continue;
        memset(in, 0, sizeof in);
        for (int y = 1; y < 125; y++) if (linev[a][y]) in[mode ? cls[y] : y - 1] = 1;
        fixpoly(perm, npts, in, f1[a]); f1[a][0] = 0;
        for (int d = 0; d <= K; d++) c[d] -= f1[a][d];
      }
      for (int b = 0; b < 31; b++) {
        if (!inv_p[b]) continue;
        memset(in, 0, sizeof in);
        for (int y = 1; y < 125; y++) if (planev[b][y]) in[mode ? cls[y] : y - 1] = 1;
        fixpoly(perm, npts, in, tmp); tmp[0] = 0;
        for (int a = 0; a < 31; a++) if (inv_l[a] && linplane[a][b]) for (int d = 0; d <= K; d++) tmp[d] -= f1[a][d];
        for (int d = 0; d <= K; d++) c[d] -= tmp[d];
      }
      for (int d = 0; d <= K; d++) { if (mode) totQ[d] += (u128)c[d]; else totV[d] += (u128)c[d]; }
    }
  }
  printf("|GL_3(F_5)| = %ld\n", ng);
  for (int d = 3; d <= K; d++) {
    unsigned long long ov = (unsigned long long)(totV[d] / ng), oq = (unsigned long long)(totQ[d] / ng);
    printf("k=%2d  V-orbits %llu (rem %llu)   Q-orbits %llu (rem %llu)\n", d, ov,
           (unsigned long long)(totV[d] % ng), oq, (unsigned long long)(totQ[d] % ng));
  }
  return 0;
}
